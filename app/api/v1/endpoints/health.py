from fastapi import APIRouter

router = APIRouter()

@router.get("/health", summary="Health Check", response_description="Checks if the API is operational.")
async def health_check():
    return {"status": "ok", "message": "API is healthy"}