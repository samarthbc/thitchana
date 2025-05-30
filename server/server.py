from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = FastAPI()

# Allow all CORS origins (not secure for production!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# MongoDB client setup
client = MongoClient("mongodb+srv://user1:User1@cluster0.o4gvz5k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["wishes_db"]
collection = db["wishes"]

# Request model
class Sentence(BaseModel):
    text: str

@app.post("/wish")
async def add_sentence(sentence: Sentence):
    try:
        result = collection.insert_one({"text": sentence.text})
        return {"message": "Sentence stored", "id": str(result.inserted_id)}
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
