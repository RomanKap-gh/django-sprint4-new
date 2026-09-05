from functools import cache

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

import core.constants as constants


@cache
def load_model():

    tokenizer = AutoTokenizer.from_pretrained(constants.MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        constants.MODEL_NAME
    )

    model.eval()

    return tokenizer, model


def get_toxicity_score(text: str) -> float:
    """Вернуть итоговую оценку токсичности от 0 до 1."""
    tokenizer, model = load_model()

    inputs = tokenizer(
        text,
        return_tensors='pt',
        truncation=True,
        padding=True,
    )

    with torch.inference_mode():
        logits = model(**inputs).logits[0]
        probabilities = torch.sigmoid(logits).cpu()

    non_toxic_probability = probabilities[0].item()
    dangerous_probability = probabilities[-1].item()

    return (
        1
        - non_toxic_probability
        * (1 - dangerous_probability)
    )


def is_toxic(text: str) -> bool:
    """Определить, считается ли текст токсичным."""
    return get_toxicity_score(text) >= constants.TOXICITY_THRESHOLD
