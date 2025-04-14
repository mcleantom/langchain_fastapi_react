from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import asyncio
import sys
import contextlib
from app.db.engine import session_manager
from app.api.v1 import router


if sys.platform == 'win32':
    # Set the policy to prevent "Event loop is closed" error on Windows - https://github.com/encode/httpx/issues/914
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


load_dotenv()


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if session_manager._engine is not None:
        await session_manager.close()


app = FastAPI(lifespan=lifespan, title="LangchainAPI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
