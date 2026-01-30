import re
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class VectorHealth:
    is_safe: bool
    risk_score: float
    flags: List[str]

class VectorGuard:
    def __init__(self):
        # Patterns that indicate attempts to hijack the vector search
        self.injection_signatures = [
            r"ignore previous instructions",
            r"system override",
            r"\[inst\]",  # Common instruction tokens
            r"priority: high",
            r"base64:"    # Obfuscation indicator
        ]
        # Detect "Invisible Text" (common in poisoning) e.g., zero-width spaces
        self.steganography_chars = set(['\u200b', '\u200c', '\u200d', '\ufeff'])

    def inspect_document(self, content: str) -> VectorHealth:
        flags = []
        score = 0.0

        # 1. Check for Command Injection signatures
        for pattern in self.injection_signatures:
            if re.search(pattern, content, re.IGNORECASE):
                flags.append(f"INJECTION_RISK: {pattern}")
                score += 0.4

        # 2. Check for Steganography (Invisible characters)
        steg_count = sum(1 for char in content if char in self.steganography_chars)
        if steg_count > 0:
            flags.append(f"STEGANOGRAPHY: {steg_count} hidden chars found")
            score += 0.5

        # 3. Density Check (High repetition often messes up embeddings)
        if len(content) > 0:
            words = content.split()
            unique_ratio = len(set(words)) / len(words)
            if unique_ratio < 0.1: # Less than 10% unique words
                flags.append("LOW_ENTROPY: Repetitive content (DoS risk)")
                score += 0.2

        return VectorHealth(
            is_safe=score < 0.5,
            risk_score=min(score, 1.0),
            flags=flags
        )
