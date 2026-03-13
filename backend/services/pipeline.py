from typing import Dict, List, Optional

# Support both package and module execution
from core.config import settings
from services.llm import LLMClient
from services.trainer import append_training_example, predict_categories, model_ready
from services.data_collector import collector

async def analyze_text(text: str, force_llm: Optional[bool] = None, filename: Optional[str] = None, file_hash: Optional[str] = None) -> Dict:
    use_llm = settings.use_llm if force_llm is None else bool(force_llm)
    if model_ready() and not use_llm:
        cats = predict_categories(text)
        data = [
            {
                "risk": f"Potential {c} risk",
                "category": c,
                "context": "Predicted by local model based on text patterns.",
            }
            for c in cats
        ]
        return {"data": data, "source": "model"}
    client = LLMClient()
    risks = await client.analyze_risks(text)
    try:
        if risks:
            collector.collect(
                text=text,
                risks=risks,
                source_type="upload",
                filename=filename,
                file_hash=file_hash,
            )
            append_training_example(text, risks)
    except Exception as e:
        print(f"Warning: Failed to store training data: {e}")
        pass
    return {"data": risks, "source": "llm"}
