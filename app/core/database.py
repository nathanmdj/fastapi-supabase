from supabase import create_client, Client
from app.core.config import settings

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def get_supabase_client() -> Client:
    return supabase


def get_service_client() -> Client:
    if settings.SUPABASE_SERVICE_KEY:
        return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
    return supabase