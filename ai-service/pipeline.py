from typing import Dict, List, Optional

# Support both package and module execution
try:
    from .config import settings
    from .llm import LLMClient
    from .trainer import append_training_example, predict_categories, model_ready
    from .data_collector import collector
except ImportError:
    from config import settings
    from llm import LLMClient
    from trainer import append_training_example, predict_categories, model_ready
    from data_collector import collector


async def analyze_text(text: str, force_llm: Optional[bool] = None, filename: Optional[str] = None, file_hash: Optional[str] = None) -> Dict:
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
    
    # Store training data using enhanced collector
    try:
        if risks:
            # Use new enhanced collector
            collector.collect(
                text=text,
                risks=risks,
                source_type="upload",
                filename=filename,
                file_hash=file_hash,
            )
            
            # Keep backward compatibility with old trainer format
            append_training_example(text, risks)
    except Exception as e:
        # Non-fatal logging; file system may be read-only in some environments
        print(f"Warning: Failed to store training data: {e}")
        pass
    
    return {"data": risks, "source": "llm"}