from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum


class AlgorithmStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AlgorithmRequest:
    def __init__(
        self,
        id: str,
        user_id: str,
        algorithm_type: str,
        input_data: Dict[str, Any],
        status: AlgorithmStatus = AlgorithmStatus.PENDING,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        created_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.algorithm_type = algorithm_type
        self.input_data = input_data
        self.status = status
        self.result = result
        self.error = error
        self.created_at = created_at or datetime.utcnow()
        self.completed_at = completed_at
    
    def mark_processing(self):
        self.status = AlgorithmStatus.PROCESSING
    
    def mark_completed(self, result: Dict[str, Any]):
        self.status = AlgorithmStatus.COMPLETED
        self.result = result
        self.completed_at = datetime.utcnow()
    
    def mark_failed(self, error: str):
        self.status = AlgorithmStatus.FAILED
        self.error = error
        self.completed_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "algorithm_type": self.algorithm_type,
            "input_data": self.input_data,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }