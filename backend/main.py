import os
import requests
from typing import Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://llmbox.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def fetch_valid_models() -> Dict[str, str]:
    """Fetch all free OpenRouter models with $0 input and output token cost."""
    try:
        api_key = os.getenv("OPENROUTER_API_KEY")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "LLMBox/0.1",
            "Accept": "application/json"
        }
        response = requests.get("https://openrouter.ai/api/v1/models", headers=headers)
        response.raise_for_status()

        raw_data = response.json().get("data", [])
        valid_models = {}

        for model in raw_data:
            model_id = model.get("id", "")
            pricing = model.get("pricing", {})
            input_price = pricing.get("usd_per_million_input_tokens", 999)
            output_price = pricing.get("usd_per_million_output_tokens", 999)

            if input_price == 0 and output_price == 0 and model.get("endpoints"):
                name = model.get("name", model_id)
                valid_models[name] = model_id + ":free"

        print(f"[✅] Loaded {len(valid_models)} free models:")
        for name in valid_models:
            print(f"  - {name}")

        return valid_models

    except Exception as e:
        print(f"[!] Failed to fetch models from OpenRouter: {e}")
        return {}

model_map = fetch_valid_models()
if not model_map:
    print("⚠️ No valid models found — using fallback.")
    model_map = {
        "llama-4-maverick": "meta-llama/llama-4-maverick:free",
        "mistral-small-3.1-24b-instruct": "mistralai/mistral-small-3.1-24b-instruct:free"
    }

class PromptRequest(BaseModel):
    prompt: str
    models: dict
    user_key: str

@app.get("/models")
def get_models():
    return JSONResponse(list(model_map.keys()))

@app.post("/compare")
def compare_models(data: PromptRequest):
    client = OpenAI(
        api_key=data.user_key,
        base_url="https://openrouter.ai/api/v1"
    )

    results = {}

    for model_key, enabled in data.models.items():
        if enabled and model_key in model_map:
            try:
                response = client.chat.completions.create(
                    model=model_map[model_key],
                    messages=[{"role": "user", "content": data.prompt}]
                )
                output = response.choices[0].message.content
                results[model_key] = output
            except Exception as e:
                results[model_key] = f"[Error: {str(e)}]"

    return {"results": results}
