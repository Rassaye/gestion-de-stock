from contextlib import asynccontextmanager
from fastapi import FastAPI

import routes.articles
import routes.auth
import routes.categories
import routes.user
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    print("Shutting down...")

    
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "PUT"],
    allow_headers=["*"],
)

app.include_router(routes.articles.router)
app.include_router(routes.categories.router)
app.include_router(routes.user.router)
app.include_router(routes.auth.router)

