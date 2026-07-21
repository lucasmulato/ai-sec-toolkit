from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional
from datetime import datetime

class VulnerabilitySeverity(Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass(frozen=True)
class ScanResult:
    scanner_id: str
    vulnerability_type: str
    severity: VulnerabilitySeverity
    payload: str
    raw_response: str
    is_vulnerable: bool
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class ScannerException(Exception):
    """Base exception for all toolkit scanners."""
    def __init__(self, message: str, retryable: bool = True):
        self.retryable = retryable
        super().__init__(message)