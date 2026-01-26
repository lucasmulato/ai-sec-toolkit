import re
import spacy
import asyncio
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class PIIDetected:
    type: str
    value: str
    stage: str

class PIIScanner:
    def __init__(self, model_name: str = "en_core_web_sm"):
        self.regex_patterns = {
            "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
            "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
            "API_KEY": r"sk-[a-zA-Z0-9]{32,}"
        }
        try:
            self.nlp = spacy.load(model_name)
        except:
            print(f"[!] Warning: spaCy model '{model_name}' not found. NER stage may fail.")
            self.nlp = None

    async def scan(self, text: str) -> Dict[str, Any]:
        results = []
        
        # Stage 1: Regex
        for label, pattern in self.regex_patterns.items():
            for match in re.findall(pattern, text):
                results.append(vars(PIIDetected(label, match, "REGEX")))
        
        # Stage 2: NER
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ["PERSON", "ORG", "GPE"]:
                    results.append(vars(PIIDetected(ent.label_, ent.text, "NER")))

        # Stage 3: Placeholder for LLM Semantic Check
        # (This would call your reasoner model)
        
        return {"detections": results, "count": len(results)}