from fastapi import FastAPI

import routes.articles
import routes.auth
import routes.categories
import routes.stores
import routes.user
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(routes.articles.router)
app.include_router(routes.stores.router)
app.include_router(routes.categories.router)
app.include_router(routes.user.router)
app.include_router(routes.auth.router)

