# LLMBox 

LLMBox is a web-based tool designed to help developers, researchers, and AI enthusiasts evaluate and compare the behavior of large language models (LLMs) side by side. It focuses on providing practical, interpretable metrics that give insight into how LLMs generate language—and how their outputs differ.

---

## What LLMBox Does

When given a single prompt, LLMBox sends it to multiple LLMs available for free through the OpenRouter platform. It returns their responses along with a side-by-side breakdown of key linguistic and structural properties.

LLMBox allows you to:

- Compare how different models interpret and respond to the same prompt
- Visualize word-by-word differences between outputs
- Understand underlying language structure using statistical measures

---

## Why These Metrics Matter

Understanding LLM behavior isn't just about which one sounds better—it's about understanding **why** they behave differently. LLMBox introduces multiple analytical metrics:

### 1. **Token Count**
   Indicates the length of a model's response. Helps reveal verbosity or conciseness.

### 2. **Entropy**
   A measure of randomness or diversity in word choice. Higher entropy often means more variation, while lower entropy suggests more repetition or formulaic structure.

### 3. **Repetition Score**
   Detects how often words or phrases are reused. Useful for identifying models that loop or repeat themselves unnecessarily.

### 4. **Compression Ratio**
   Measures how compressible the output is, giving insight into information density. More compressible text may be more predictable or redundant.

### 5. **Jaccard Similarity**
   Compares responses pairwise to quantify overlap in vocabulary. Great for measuring how "alike" two model responses are.

---

## Who It's For

- **AI Researchers** exploring model behavior
- **Developers** benchmarking model output fidelity
- **Educators** demonstrating language model variance
- **Anyone** curious about how different AI models think

---

## How to Use It

1. Paste your **OpenRouter API key** (you can get one at [openrouter.ai](https://openrouter.ai))
2. Type a **prompt** in the text box
3. Select **models** you'd like to compare
4. Click **Compare**

LLMBox will display:
- Each model’s output
- Metrics for each output
- Highlighted diff comparisons between every pair of models

---

## Privacy & Usage

All processing happens live in your browser using a local connection to your API key. Your data is **never stored** and **never shared**. You control which models are used and what prompt is sent.

---

LLMBox is open-source and built to support transparency and experimentation in AI.
