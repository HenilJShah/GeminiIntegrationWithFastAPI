from motor.motor_asyncio import AsyncIOMotorClient
from helper.helper import DBUri

# Initialize the MongoDB client using the URI specified in the DBUri class.
client = AsyncIOMotorClient(DBUri.MONGO_DB_URI)

# Reference to the 'sample_papers_db' database.
db = client.sample_papers_db

# Reference to the 'papers' collection within the 'sample_papers_db' database.
papers_collection = db.papers
