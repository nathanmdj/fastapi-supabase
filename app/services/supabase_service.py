from typing import List, Dict, Any, Optional
from supabase import Client


class SupabaseService:
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
    
    def create_record(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.supabase.table(table).insert(data).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            raise Exception(f"Failed to create record: {str(e)}")
    
    def get_record(self, table: str, record_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.supabase.table(table).select("*").eq("id", record_id).single().execute()
            return response.data
        except Exception:
            return None
    
    def get_records(self, table: str, filters: Optional[Dict[str, Any]] = None, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            query = self.supabase.table(table).select("*")
            
            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)
            
            response = query.limit(limit).execute()
            return response.data or []
        except Exception as e:
            raise Exception(f"Failed to get records: {str(e)}")
    
    def update_record(self, table: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.supabase.table(table).update(data).eq("id", record_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            raise Exception(f"Failed to update record: {str(e)}")
    
    def delete_record(self, table: str, record_id: str) -> bool:
        try:
            self.supabase.table(table).delete().eq("id", record_id).execute()
            return True
        except Exception as e:
            raise Exception(f"Failed to delete record: {str(e)}")
    
    def execute_rpc(self, function_name: str, params: Dict[str, Any]) -> Any:
        try:
            response = self.supabase.rpc(function_name, params).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Failed to execute RPC: {str(e)}")