# LLMBox

LLMBox is a browser-based tool for comparing outputs from large language models (LLMs). It allows developers and researchers to analyze model responses using metrics like entropy, repetition, compression ratio, and Jaccard similarity. Built with a Svelte frontend and FastAPI backend, LLMBox connects to OpenRouter to access multiple free models.

---

## Features

- Select and compare multiple OpenRouter-supported LLMs
- Analyze token count, entropy, repetition score, compression ratio
- View token-level differences using color-coded diffing
- Automatically fetches only free models with endpoints
- Minimal setup required: Svelte + FastAPI + OpenRouter

---

## Technologies

- Frontend: Svelte, JavaScript
- Backend: FastAPI (Python)
- API Integration: OpenRouter.ai
- Diff Engine: `diff` JavaScript library

---

## Setup Instructions

### Prerequisites

- Node.js (v18 or newer)
- Python 3.10+
- Git

---

### 1. Clone the Repository

```
git clone https://github.com/yourusername/llmbox.git
cd llmbox
```

---

### 2. Backend Setup (FastAPI)

```
cd backend
python -m venv venv
```

Activate the virtual environment:

macOS/Linux:

```
source venv/bin/activate
```

Windows:

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Create a `.env` file:

```
OPENROUTER_API_KEY=sk-yourkeyhere
```

Run the backend server:

```
uvicorn main:app --reload
```

---

### 3. Frontend Setup (Svelte)

```
cd ../frontend
npm install
npm run dev
```

Visit:

```
http://localhost:5173
```

---

## Folder Structure

```
llmbox/
├── backend/
│   ├── main.py
│   ├── .env
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── package.json
└── README.md
```

---

## Contributing

1. Fork this repo
2. Create your feature branch:

```
git checkout -b feature-name
```

3. Commit your changes:

```
git commit -am "Add feature"
```

4. Push to your branch:

```
git push origin feature-name
```

5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

Special thanks to [OpenRouter.ai](https://openrouter.ai) for providing public access to a growing list of open language models.
