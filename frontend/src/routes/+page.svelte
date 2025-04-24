<script>
	import { onMount } from 'svelte';
	import { diffWords } from 'diff';

	let apiKey = "";
	let prompt = "";
	let isLoading = false;
	let error = "";
	let results = {};
	let models = {};

	onMount(async () => {
		try {
			const res = await fetch("http://llmbox.onrender.com/models");
			const modelList = await res.json();
			const updatedModels = Object.fromEntries(modelList.map(m => [m, false]));
			models = { ...updatedModels };
		} catch (e) {
			error = "Failed to fetch models from backend.";
			console.error(e);
		}
	});

	function tokenCount(text) {
		if (!text || typeof text !== 'string') return 0;
		return text.trim().split(/\s+/).length;
	}

	function entropy(text) {
		const words = text.trim().toLowerCase().split(/\s+/);
		const total = words.length;
		if (total === 0) return 0;
		const freq = {};
		for (const word of words) {
			freq[word] = (freq[word] || 0) + 1;
		}
		let score = 0;
		for (const count of Object.values(freq)) {
			const p = count / total;
			score -= p * Math.log2(p);
		}
		return score.toFixed(3);
	}

	function compressionRatio(text) {
		const original = text.length;
		const compressed = new TextEncoder().encode(text).reduce((acc, b) => acc + (b === 32 ? 1 : 2), 0);
		return (original / compressed).toFixed(2);
	}

	function repetitionScore(text) {
		const words = text.toLowerCase().split(/\s+/);
		const freq = {};
		let max = 0;
		for (const word of words) {
			if (!word) continue;
			freq[word] = (freq[word] || 0) + 1;
			if (freq[word] > max) max = freq[word];
		}
		return max;
	}

	function outputLengthClass(count) {
		if (count < 50) return "Short";
		if (count < 150) return "Medium";
		return "Long";
	}

	function jaccardSim(a, b) {
		const setA = new Set(a.trim().split(/\s+/));
		const setB = new Set(b.trim().split(/\s+/));
		const intersection = new Set([...setA].filter(x => setB.has(x)));
		const union = new Set([...setA, ...setB]);
		return (intersection.size / union.size).toFixed(2);
	}

	function formatDiff(diff) {
		return diff
			.map(part => {
				if (part.added) return `<span class="diff-add">${part.value}</span>`;
				if (part.removed) return `<span class="diff-remove">${part.value}</span>`;
				return `<span>${part.value}</span>`;
			})
			.join('');
	}

	async function handleCompare() {
		isLoading = true;
		error = "";
		results = {};
		try {
			const response = await fetch("http://llmbox.onrender.com/compare", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ prompt, models, user_key: apiKey })
			});
			if (!response.ok) throw new Error("Server error. Check your API key or model status.");
			const data = await response.json();
			results = data.results;
		} catch (err) {
			error = err.message;
		} finally {
			isLoading = false;
		}
	}
</script>

<style>
	main { max-width: 1000px; margin: auto; padding: 2rem; font-family: system-ui, sans-serif; }
	label { display: block; margin: 0.25rem 0; }
	.model-list { columns: 2; max-width: 800px; }
	.card {
		background: #f9f9f9;
		padding: 1rem;
		border-radius: 5px;
		margin-bottom: 1rem;
	}
	table {
		width: 100%;
		border-collapse: collapse;
		margin: 1rem 0;
	}
	th, td {
		border: 1px solid #ccc;
		padding: 0.5rem;
		text-align: center;
	}
	th {
		background: #eee;
	}
	.short { background: #cce5ff; }
	.medium { background: #d4edda; }
	.long { background: #f8d7da; }
	.diff-add { background: #c6f6d5; }
	.diff-remove { background: #feb2b2; text-decoration: line-through; }
</style>

<main>
	<h1>🧠 LLMBox</h1>
	<p>Compare LLM outputs with side-by-side differences and meaningful output metrics.</p>

	<hr />

	<label>🔑 OpenRouter API Key</label>
	<input type="text" bind:value={apiKey} placeholder="sk-..." style="width: 100%; padding: 0.5rem; margin-bottom: 1rem;" />

	<label>📝 Prompt</label>
	<textarea bind:value={prompt} rows="4" placeholder="Enter your prompt here..." style="width: 100%; padding: 0.5rem;"></textarea>

	<h3 style="margin-top: 1rem;">🤖 Choose Models:</h3>

	{#if Object.keys(models).length > 0}
		<div class="model-list">
			{#each Object.keys(models) as model}
				<label>
					<input type="checkbox" bind:checked={models[model]} />
					{model}
				</label>
			{/each}
		</div>
	{:else}
		<p>📡 Loading models...</p>
	{/if}

	<button on:click={handleCompare} style="margin-top: 1rem; padding: 0.5rem 1.5rem;">Compare</button>

	{#if isLoading}
		<p>Loading model outputs...</p>
	{:else if error}
		<p style="color: red;">{error}</p>
	{:else if Object.keys(results).length > 0}
		<h2>📊 Output Metrics Comparison</h2>
		<table>
			<thead>
				<tr>
					<th>Model</th>
					<th>Token Count</th>
					<th>Entropy</th>
					<th>Repetition</th>
					<th>Compression</th>
					<th>Length</th>
				</tr>
			</thead>
			<tbody>
				{#each Object.entries(results) as [model, output]}
					<tr class={outputLengthClass(tokenCount(output)).toLowerCase()}>
						<td>{model}</td>
						<td>{tokenCount(output)}</td>
						<td>{entropy(output)}</td>
						<td>{repetitionScore(output)}</td>
						<td>{compressionRatio(output)}</td>
						<td>{outputLengthClass(tokenCount(output))}</td>
					</tr>
				{/each}
			</tbody>
		</table>

		<h2>📤 Model Outputs</h2>
		{#each Object.entries(results) as [model, output]}
			<div class="card">
				<h3>{model}</h3>
				<pre>{output}</pre>
			</div>
		{/each}

		<h2>🧾 Output Differences</h2>
		{#each Object.entries(results) as [modelA, dataA], i}
			{#each Object.entries(results).slice(i + 1) as [modelB, dataB]}
				<div class="card">
					<h3>{modelA} vs {modelB}</h3>
					<p><strong>Jaccard similarity:</strong> {jaccardSim(dataA, dataB)}</p>
					<pre>{@html formatDiff(diffWords(dataA, dataB))}</pre>
				</div>
			{/each}
		{/each}
	{/if}
</main>
