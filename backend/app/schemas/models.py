from pydantic import BaseModel
from typing import List, Dict, Any

class BackendModelsResponse(BaseModel):
    total_models: int
    loaded_models: int
    models: List[Dict[str, Any]]
    timestamp: str
