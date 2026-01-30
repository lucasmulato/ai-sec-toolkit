import spacy
from typing import Dict

class ContextualRedactor:
    def __init__(self, model_name="en_core_web_sm"):
        try:
            self.nlp = spacy.load(model_name)
        except:
            spacy.cli.download(model_name)
            self.nlp = spacy.load(model_name)
        
        # Memory to keep consistency within a single session
        self.entity_map: Dict[str, str] = {}
        self.counts: Dict[str, int] = {"PERSON": 0, "ORG": 0, "GPE": 0, "DATE": 0}

    def redact(self, text: str) -> str:
        doc = self.nlp(text)
        redacted_text = text
        
        # Sort entities by length (descending) to avoid partial replacement issues
        entities = sorted(doc.ents, key=lambda e: len(e.text), reverse=True)
        
        for ent in entities:
            if ent.label_ in self.counts:
                # Check if we've seen this specific entity value before
                if ent.text not in self.entity_map:
                    self.counts[ent.label_] += 1
                    placeholder = f"[{ent.label_}_{self.counts[ent.label_]}]"
                    self.entity_map[ent.text] = placeholder
                
                # Replace in the text
                placeholder = self.entity_map[ent.text]
                redacted_text = redacted_text.replace(ent.text, placeholder)
                
        return redacted_text

    def reset_memory(self):
        """Clear the session memory for a new document."""
        self.entity_map = {}
        self.counts = {k: 0 for k in self.counts}
