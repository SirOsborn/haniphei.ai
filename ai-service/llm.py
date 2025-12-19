import json
from typing import List, Dict
import httpx

# Support both package and module execution
try:
    from .config import settings
except ImportError:
    from config import settings


SYSTEM_PROMPT = (
    "You are an AI assistant that extracts project risks. "
    "Return a JSON object with a 'data' list. Each item must have: "
    "'risk' (short phrase), 'category' (one of Financial, Schedule, Technical, Legal, Operational, Compliance, Other), "
    "and 'context' (supporting sentence)."
)

USER_INSTRUCTIONS = (
    "Analyze the following text for project risks and return strictly valid JSON. "
    "Avoid extra commentary."
)


class LLMClient:
    def __init__(self):
        self.provider = settings.llm_provider

    async def analyze_risks(self, text: str) -> List[Dict]:
        if self.provider == "gemini":
            return await self._gemini_generate(text)
        elif self.provider == "ollama":
            return await self._ollama_generate(text)
        else:
            raise ValueError(f"Unsupported LLM_PROVIDER: {self.provider}. Use 'gemini' or 'ollama'.")

    async def _gemini_generate(self, text: str) -> List[Dict]:
        import google.generativeai as genai

        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY not set. Get one free at https://aistudio.google.com/app/apikey")

        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            system_instruction=SYSTEM_PROMPT,
        )
        prompt = f"{USER_INSTRUCTIONS}\n\nText:\n{text}\n\nReturn JSON only."
        response = await model.generate_content_async(prompt)
        content = response.text
        return _parse_json_response(content)

    async def _ollama_generate(self, text: str) -> List[Dict]:
        prompt = (
            f"{SYSTEM_PROMPT}\n\n{USER_INSTRUCTIONS}\n\nText:\n{text}\n\nReturn JSON only."
        )
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(
                f"{settings.ollama_url}/api/generate",
                json={"model": settings.ollama_model, "prompt": prompt, "stream": False},
            )
            r.raise_for_status()
            data = r.json()
            content = data.get("response", "{}")
            return _parse_json_response(content)


def _parse_json_response(content: str) -> List[Dict]:
    """Try to parse a JSON object containing {'data': [...]} from the model response."""
    try:
        obj = json.loads(content)
        if isinstance(obj, dict) and "data" in obj and isinstance(obj["data"], list):
            return obj["data"]
    except Exception:
        pass

    # Try to recover by extracting JSON substring
    import re
    m = re.search(r"\{.*\}", content, re.DOTALL)
    if m:
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, dict) and "data" in obj and isinstance(obj["data"], list):
                return obj["data"]
        except Exception:
            pass

    # If recovery fails, return empty list
    return []