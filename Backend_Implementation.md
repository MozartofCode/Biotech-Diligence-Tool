# Backend Implementation: Groq-Powered Multi-Agent Logic

## 1. The Pydantic Schema
Define the "Ground Truth" structure to ensure the LLM follows the scientific format.

```python
from pydantic import BaseModel
from typing import List, Optional

class ScientificAsset(BaseModel):
    drug_name: str
    molecule_type: str
    clinical_phase: str
    primary_toxicity_finding: str
    confidence_score: float
    conflicts_found: List[str]