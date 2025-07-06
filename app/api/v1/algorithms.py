from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from supabase import Client

from app.core.database import get_supabase_client
from app.api.deps import get_current_active_user
from app.schemas.algorithm import (
    AlgorithmRequest, 
    AlgorithmResult, 
    AlgorithmHistoryItem,
    AlgorithmType
)
from app.services.algorithm_service import AlgorithmService

router = APIRouter()


@router.post("/process", response_model=AlgorithmResult)
async def process_algorithm(
    request: AlgorithmRequest,
    current_user: dict = Depends(get_current_active_user),
    supabase: Client = Depends(get_supabase_client)
):
    try:
        algorithm_service = AlgorithmService(supabase)
        result = algorithm_service.process_algorithm(
            algorithm_type=request.algorithm_type,
            input_data=request.input_data,
            user_id=current_user["id"]
        )
        return AlgorithmResult(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Algorithm processing failed: {str(e)}"
        )


@router.get("/history", response_model=List[AlgorithmHistoryItem])
async def get_algorithm_history(
    current_user: dict = Depends(get_current_active_user),
    supabase: Client = Depends(get_supabase_client),
    limit: int = Query(50, ge=1, le=100, description="Number of items to return"),
    algorithm_type: AlgorithmType = Query(None, description="Filter by algorithm type")
):
    try:
        algorithm_service = AlgorithmService(supabase)
        history = algorithm_service.get_algorithm_history(
            user_id=current_user["id"],
            limit=limit
        )
        
        # Filter by algorithm type if specified
        if algorithm_type:
            history = [item for item in history if item.get("algorithm_type") == algorithm_type]
        
        return [AlgorithmHistoryItem(**item) for item in history]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch history: {str(e)}"
        )


@router.get("/types")
async def get_algorithm_types():
    return {
        "types": [
            {
                "name": "fibonacci",
                "description": "Calculate Fibonacci numbers",
                "input_schema": {
                    "n": "integer (0-100) - The nth Fibonacci number to calculate"
                }
            },
            {
                "name": "prime_check",
                "description": "Check if a number is prime",
                "input_schema": {
                    "number": "integer (>=2) - The number to check for primality"
                }
            },
            {
                "name": "sorting",
                "description": "Sort an array of integers",
                "input_schema": {
                    "array": "array of integers (max 1000) - Array to sort",
                    "algorithm": "string (optional) - Sorting algorithm ('quicksort', 'mergesort')"
                }
            },
            {
                "name": "matrix_multiply",
                "description": "Multiply two matrices",
                "input_schema": {
                    "matrix_a": "2D array of integers - First matrix",
                    "matrix_b": "2D array of integers - Second matrix"
                }
            }
        ]
    }


@router.get("/stats")
async def get_algorithm_stats(
    current_user: dict = Depends(get_current_active_user),
    supabase: Client = Depends(get_supabase_client)
):
    try:
        # Get algorithm usage statistics for the current user
        response = supabase.table("algorithm_requests").select("algorithm_type, status").eq("user_id", current_user["id"]).execute()
        
        if not response.data:
            return {
                "total_requests": 0,
                "completed_requests": 0,
                "failed_requests": 0,
                "algorithm_usage": {}
            }
        
        requests = response.data
        total_requests = len(requests)
        completed_requests = len([r for r in requests if r["status"] == "completed"])
        failed_requests = len([r for r in requests if r["status"] == "failed"])
        
        # Count usage by algorithm type
        algorithm_usage = {}
        for request in requests:
            alg_type = request["algorithm_type"]
            if alg_type not in algorithm_usage:
                algorithm_usage[alg_type] = 0
            algorithm_usage[alg_type] += 1
        
        return {
            "total_requests": total_requests,
            "completed_requests": completed_requests,
            "failed_requests": failed_requests,
            "algorithm_usage": algorithm_usage
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch stats: {str(e)}"
        )