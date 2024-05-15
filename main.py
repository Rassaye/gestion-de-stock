from fastapi import FastAPI

import routes.articles
import routes.categories
import routes.stores



app = FastAPI()

app.include_router(routes.articles.router)
app.include_router(routes.stores.router)
app.include_router(routes.categories.router)

