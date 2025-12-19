from typing import Dict, List, Optional

# Support both package and module execution
try:
    from .config import settings
    from .llm import LLMClient
    from .trainer import append_training_example, predict_categories, model_ready
except ImportError:
    from config import settings
    from llm import LLMClient
    from trainer import append_training_example, predict_categories, model_ready


async def analyze_text(text: str, force_llm: Optional[bool] = None) -> Dict:
    """Hybrid analysis: use LLM initially; log data; gradually switch to local model.

    Returns a dict: {"data": [ {risk, category, context}, ... ], "source": "llm"|"model" }
    """
    use_llm = settings.use_llm if force_llm is None else bool(force_llm)

    # If local model is present and LLM is disabled, use model
    if model_ready() and not use_llm:
        cats = predict_categories(text)
        # Construct a minimal structured output from categories
        data = [
            {
                "risk": f"Potential {c} risk",
                "category": c,
                "context": "Predicted by local model based on text patterns.",
            }
            for c in cats
        ]
        return {"data": data, "source": "model"}

    # Otherwise, use LLM and record training example for future fine-tuning
    client = LLMClient()
    risks = await client.analyze_risks(text)
    try:
        if risks:
            append_training_example(text, risks)
    except Exception:
        # Non-fatal logging; file system may be read-only in some environments
        pass
    return {"data": risks, "source": "llm"}