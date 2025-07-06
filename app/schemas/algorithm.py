from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class AlgorithmType(str, Enum):
    FIBONACCI = "fibonacci"
    PRIME_CHECK = "prime_check"
    SORTING = "sorting"
    MATRIX_MULTIPLY = "matrix_multiply"


class AlgorithmStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AlgorithmRequest(BaseModel):
    algorithm_type: AlgorithmType
    input_data: Dict[str, Any]
    
    class Config:
        json_schema_extra = {
            "example": {
                "algorithm_type": "fibonacci",
                "input_data": {"n": 10}
            }
        }


class FibonacciInput(BaseModel):
    n: int = Field(..., ge=0, le=100, description="Fibonacci number to calculate")


class PrimeCheckInput(BaseModel):
    number: int = Field(..., ge=2, description="Number to check for primality")


class SortingInput(BaseModel):
    array: List[int] = Field(..., max_length=1000, description="Array of integers to sort")
    algorithm: str = Field("quicksort", description="Sorting algorithm to use")


class MatrixMultiplyInput(BaseModel):
    matrix_a: List[List[int]] = Field(..., description="First matrix")
    matrix_b: List[List[int]] = Field(..., description="Second matrix")


class AlgorithmResult(BaseModel):
    request_id: str
    algorithm_type: AlgorithmType
    result: Dict[str, Any]
    processing_time: Optional[str] = None
    status: AlgorithmStatus
    
    class Config:
        from_attributes = True


class AlgorithmHistoryItem(BaseModel):
    id: str
    user_id: str
    algorithm_type: AlgorithmType
    input_data: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    status: AlgorithmStatus
    error: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AlgorithmHistory(BaseModel):
    items: List[AlgorithmHistoryItem]
    total: int
    page: int
    per_page: int