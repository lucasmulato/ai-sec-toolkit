import json
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class AIModelCard(BaseModel):
    model_name: str
    version: str
    publisher: str
    description: Optional[str]
    license: str

class AIBOM(BaseModel):
    bom_format: str = "CycloneDX"
    spec_version: str = "1.6"
    serial_number: str
    version: int = 1
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    components: List[dict]

class AIBOMGenerator:
    """
    Gera o AI Bill of Materials (AI-BOM) no formato OWASP CycloneDX.
    Mitiga riscos de Supply Chain ao listar modelos, datasets e bibliotecas.
    """
    
    def generate_bom(self, models: List[AIModelCard], libs: List[str]) -> str:
        components = []
        
        # Adiciona Modelos como componentes de ML
        for m in models:
            components.append({
                "type": "machine-learning-model",
                "name": m.model_name,
                "version": m.version,
                "publisher": m.publisher,
                "evidence": {"licenses": [{"license": {"id": m.license}}]}
            })
            
        # Adiciona Bibliotecas Core
        for lib in libs:
            components.append({
                "type": "library",
                "name": lib.split("==")[0],
                "version": lib.split("==")[1] if "==" in lib else "unknown"
            })

        bom = AIBOM(
            serial_number=f"urn:uuid:{hash(str(components))}",
            components=components
        )
        
        return bom.model_dump_json(indent=2)