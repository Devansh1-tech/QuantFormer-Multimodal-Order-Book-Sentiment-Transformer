from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class BackendHealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    environment: str
    uptime: str
    uptime_seconds: int
    models: List[Dict[str, Any]]
    gpu: Dict[str, Any]
    system: Dict[str, Any]
    kafka: Dict[str, Any]
    timestamp: str
