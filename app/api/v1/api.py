from fastapi import APIRouter
from app.api.v1.endpoints import auth, resume

router = APIRouter()
router.include_router(auth.router)
router.include_router(resume.router)