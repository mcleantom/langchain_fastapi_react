from fastapi import APIRouter
from .auth_router import router as auth_router
from .chat_router import router as chat_router
from .user_router import router as user_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(chat_router)
router.include_router(user_router)