from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "healthy", "service": "pet_shop"}

@router.get("/ready")
async def readiness_check():
    return {"status": "ready", "service": "pet_shop"}