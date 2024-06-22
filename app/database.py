from dotenv import dotenv_values
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from model.articles import Article
from model.categories import Categorie
from model.stores import Store
from model.users import User

config = dotenv_values(".env")


async def init_db():
    # Load the MongoDB connection string from the environment variable MONGODB_URI

    CONNECTION_STRING = "mongodb+srv://sekoukanfory1997:hFgFX9qKb1Eu1xc7@cluster0.xrjqhqr.mongodb.net/"

    # Create a MongoDB client
    client = AsyncIOMotorClient(CONNECTION_STRING)
    
    await init_beanie(database=client.stock, document_models=[Article, Categorie, Store, User])