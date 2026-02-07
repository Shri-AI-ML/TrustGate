from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from config import NLI_MODEL_NAME, DEVICE

class NLIModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(NLI_MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(NLI_MODEL_NAME).to(DEVICE)

    def predict(self, premise, hypothesis):
        inputs = self.tokenizer(premise, hypothesis, return_tensors="pt", truncation=True).to(DEVICE)
        outputs = self.model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)

        labels = ["contradiction", "neutral", "entailment"]
        max_idx = torch.argmax(probs).item()

        return labels[max_idx], probs[0][max_idx].item()


_nli_instance = None

def get_nli_model():
    global _nli_instance
    if _nli_instance is None:
        _nli_instance = NLIModel()
    return _nli_instance
