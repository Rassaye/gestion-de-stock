from dotenv import dotenv_values
from motor.motor_asyncio import AsyncIOMotorClient

config = dotenv_values(".env")

# Load the MongoDB connection string from the environment variable MONGODB_URI

CONNECTION_STRING = "mongodb+srv://sekoukanfory1997:hFgFX9qKb1Eu1xc7@cluster0.xrjqhqr.mongodb.net/"

# Create a MongoDB client
client = AsyncIOMotorClient(CONNECTION_STRING)

db = client["stock"] 