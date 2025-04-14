from fastapi import APIRouter
from .auth_router import router as auth_router
from .chat_router import router as chat_router


router = APIRouter()
router.include_router(auth_router)
router.include_router(chat_router)
