import json
from typing import List, Dict
import httpx

# Support both package and module execution
from core.config import settings

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
        """
        Analyze text for risks, with automatic fallback among providers.
        Flow: Try primary provider -> Fallback to Groq -> Fallback to next...
        """
        try:
            if self.provider == "gemini":
                return await self._gemini_generate(text)
            elif self.provider == "ollama":
                return await self._ollama_generate(text)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Primary LLM provider ({self.provider}) failed: {e}. Trying Groq fallback...")
            
        # Fallback to Groq if primary fails or is not gemini/ollama
        if settings.groq_api_key:
            try:
                return await self._groq_generate(text)
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Groq fallback also failed: {e}")
        
        raise RuntimeError("All LLM providers failed or were not configured.")

    async def _groq_generate(self, text: str) -> List[Dict]:
        """Generate analysis using Groq (fallback provider)."""
        from groq import Groq
        if not settings.groq_api_key:
            raise RuntimeError("GROQ_API_KEY not set.")
        
        client = Groq(api_key=settings.groq_api_key)
        
        # Groq currently doesn't have a native async library as direct as Gemini,
        # but the client supports sync calls. For a fallback in FastAPI, 
        # normally we'd want async, but Groq's official client has a GroqAsync class.
        from groq import AsyncGroq
        async_client = AsyncGroq(api_key=settings.groq_api_key)
        
        chat_completion = await async_client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{USER_INSTRUCTIONS}\n\nText:\n{text}"}
            ],
            model=settings.groq_model,
            response_format={"type": "json_object"}
        )
        content = chat_completion.choices[0].message.content
        return _parse_json_response(content)

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
    try:
        obj = json.loads(content)
        if isinstance(obj, dict) and "data" in obj and isinstance(obj["data"], list):
            return obj["data"]
    except Exception:
        pass
    import re
    m = re.search(r"\{.*\}", content, re.DOTALL)
    if m:
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, dict) and "data" in obj and isinstance(obj["data"], list):
                return obj["data"]
        except Exception:
            pass
    return []
