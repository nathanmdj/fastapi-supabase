from typing import Dict, Any, List
import json
from datetime import datetime
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


def serialize_datetime(dt: datetime) -> str:
    return dt.isoformat()


def deserialize_datetime(dt_str: str) -> datetime:
    return datetime.fromisoformat(dt_str)


def validate_json(data: str) -> bool:
    try:
        json.loads(data)
        return True
    except json.JSONDecodeError:
        return False


def sanitize_dict(data: Dict[str, Any], allowed_keys: List[str]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if k in allowed_keys}


def paginate_results(items: List[Any], page: int, per_page: int) -> Dict[str, Any]:
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        "items": items[start:end],
        "total": len(items),
        "page": page,
        "per_page": per_page,
        "total_pages": (len(items) + per_page - 1) // per_page
    }


def format_error_response(error: str, details: Dict[str, Any] = None) -> Dict[str, Any]:
    response = {
        "error": error,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if details:
        response["details"] = details
    
    return response


def validate_matrix(matrix: List[List[int]]) -> bool:
    if not matrix or not matrix[0]:
        return False
    
    rows = len(matrix)
    cols = len(matrix[0])
    
    for row in matrix:
        if len(row) != cols:
            return False
    
    return True


def calculate_processing_time(start_time: datetime, end_time: datetime) -> str:
    duration = end_time - start_time
    total_seconds = duration.total_seconds()
    
    if total_seconds < 1:
        return f"{int(total_seconds * 1000)}ms"
    else:
        return f"{total_seconds:.2f}s"