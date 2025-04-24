<script>
	import { onMount } from 'svelte';
	import { diffWords } from 'diff';

	let apiKey = "";
	let prompt = "";
	let isLoading = false;
	let error = "";
	let results = {};
	let models = {};
	let userSignedIn = false;
	let userName = "";

	onMount(async () => {
		const checkAuth = async () => {
			if (typeof window !== 'undefined' && window.Clerk) {
				await window.Clerk.load();

				if (window.Clerk.user) {
					userSignedIn = true;
					userName = window.Clerk.user.fullName || window.Clerk.user.username;
				} else {
					window.Clerk.redirectToSignIn({ redirectUrl: "/" });
				}
			}
		};

		await checkAuth();

		try {
			const res = await fetch("https://llmbox.onrender.com/models");
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
			const response = await fetch("https://llmbox.onrender.com/compare", {
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

	function signOut() {
		if (window.Clerk) {
			window.Clerk.signOut().then(() => window.location.href = "/");
		}
	}
</script>

<main>
	{#if userSignedIn}
		<p>Welcome, {userName} | <button on:click={signOut}>Sign Out</button></p>
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
			<!-- Metric table and result output would follow here -->
		{/if}
	{:else}
		<p>Authenticating with Clerk...</p>
	{/if}
</main>