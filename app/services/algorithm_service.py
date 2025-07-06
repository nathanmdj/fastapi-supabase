from typing import Dict, Any, List
from datetime import datetime
from supabase import Client

from app.services.supabase_service import SupabaseService


class AlgorithmService:
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.db_service = SupabaseService(supabase_client)
    
    def process_algorithm(self, algorithm_type: str, input_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        try:
            # Log the algorithm request
            request_data = {
                "user_id": user_id,
                "algorithm_type": algorithm_type,
                "input_data": input_data,
                "status": "processing",
                "created_at": datetime.utcnow().isoformat(),
            }
            
            request_record = self.db_service.create_record("algorithm_requests", request_data)
            
            # Process based on algorithm type
            if algorithm_type == "fibonacci":
                result = self._fibonacci_algorithm(input_data)
            elif algorithm_type == "prime_check":
                result = self._prime_check_algorithm(input_data)
            elif algorithm_type == "sorting":
                result = self._sorting_algorithm(input_data)
            elif algorithm_type == "matrix_multiply":
                result = self._matrix_multiply_algorithm(input_data)
            else:
                raise ValueError(f"Unknown algorithm type: {algorithm_type}")
            
            # Update the request with results
            self.db_service.update_record("algorithm_requests", request_record["id"], {
                "result": result,
                "status": "completed",
                "completed_at": datetime.utcnow().isoformat()
            })
            
            return {
                "request_id": request_record["id"],
                "algorithm_type": algorithm_type,
                "result": result,
                "processing_time": "calculated",
                "status": "completed"
            }
            
        except Exception as e:
            # Update request with error
            if 'request_record' in locals():
                self.db_service.update_record("algorithm_requests", request_record["id"], {
                    "status": "failed",
                    "error": str(e),
                    "completed_at": datetime.utcnow().isoformat()
                })
            raise Exception(f"Algorithm processing failed: {str(e)}")
    
    def get_algorithm_history(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        return self.db_service.get_records(
            "algorithm_requests",
            filters={"user_id": user_id},
            limit=limit
        )
    
    def _fibonacci_algorithm(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        n = input_data.get("n", 10)
        if n < 0:
            raise ValueError("n must be non-negative")
        
        if n <= 1:
            return {"result": n, "sequence": [0] if n == 0 else [0, 1]}
        
        sequence = [0, 1]
        for i in range(2, n + 1):
            sequence.append(sequence[i-1] + sequence[i-2])
        
        return {"result": sequence[n], "sequence": sequence}
    
    def _prime_check_algorithm(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        number = input_data.get("number")
        if number is None:
            raise ValueError("number is required")
        
        if number < 2:
            return {"is_prime": False, "number": number}
        
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                return {"is_prime": False, "number": number, "divisor": i}
        
        return {"is_prime": True, "number": number}
    
    def _sorting_algorithm(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        array = input_data.get("array", [])
        algorithm = input_data.get("algorithm", "quicksort")
        
        if algorithm == "quicksort":
            sorted_array = self._quicksort(array.copy())
        elif algorithm == "mergesort":
            sorted_array = self._mergesort(array.copy())
        else:
            sorted_array = sorted(array)
        
        return {
            "original": array,
            "sorted": sorted_array,
            "algorithm": algorithm
        }
    
    def _matrix_multiply_algorithm(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        matrix_a = input_data.get("matrix_a", [])
        matrix_b = input_data.get("matrix_b", [])
        
        if not matrix_a or not matrix_b:
            raise ValueError("Both matrices are required")
        
        rows_a, cols_a = len(matrix_a), len(matrix_a[0])
        rows_b, cols_b = len(matrix_b), len(matrix_b[0])
        
        if cols_a != rows_b:
            raise ValueError("Matrix dimensions are incompatible for multiplication")
        
        result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
        
        for i in range(rows_a):
            for j in range(cols_b):
                for k in range(cols_a):
                    result[i][j] += matrix_a[i][k] * matrix_b[k][j]
        
        return {
            "matrix_a": matrix_a,
            "matrix_b": matrix_b,
            "result": result,
            "dimensions": f"{rows_a}x{cols_a} × {rows_b}x{cols_b} = {rows_a}x{cols_b}"
        }
    
    def _quicksort(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return self._quicksort(left) + middle + self._quicksort(right)
    
    def _mergesort(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = self._mergesort(arr[:mid])
        right = self._mergesort(arr[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result