from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from qdrant_client import QdrantClient, AsyncQdrantClient, models
from sentence_transformers import SentenceTransformer
import time
import json
import uuid
import numpy as np
import base64
import time


app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods
    allow_headers=["*"],  # This allows all headers
)

encoder = SentenceTransformer("Alibaba-NLP/gte-large-en-v1.5", trust_remote_code=True)

import debugpy
debugpy.listen(("0.0.0.0", 5678))

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: str

class create_collection(BaseModel):
    collection_name: str

class get_similar_points(BaseModel):
    messages: str

class CreatePointWithPayload(BaseModel):
    chapter: str
    title: str
    problem: str
    question: str
    answer: str
    messages: str


@app.post("/create_collection")
async def create_collection(requests: create_collection):
    print(f"Creating Collection: {requests.collection_name}...")
    
    global_quantization_config = models.ProductQuantization(
        product=models.ProductQuantizationConfig(
            compression=models.CompressionRatio.X16, 
            always_ram=True))
    try:
        result = await db_client.create_collection(
            collection_name=f"{requests.collection_name}",
            vectors_config=models.VectorParams(size=encoder.get_sentence_embedding_dimension(), distance=models.Distance.COSINE),
            quantization_config = global_quantization_config
        )
        if result:
            print(f"Collection {requests.collection_name} Create Success")
            return "Success"
    except Exception as e:
        print(e)
        return e


@app.post('/get_similar_points')
async def get_similar_points(requests: get_similar_points):
    try:
        search_result = await db_client.search(
            collection_name="FIN7870",
            query_vector=encoder.encode(f"{requests.messages}").tolist(),
            limit=10,
        )
        result_list = []
        for result in search_result:
            result_list.append(json.dumps(result.payload))
        result_str = ' '.join(result_list)
        return result_str
    except Exception as e:
        print(e)
        return e

   
@app.post('/create_point_with_payload')
async def create_point_with_payload(requests: CreatePointWithPayload):
    print("Inserting Point...")
    random_uuid = uuid.uuid4()
    try:
        await db_client.upsert(
            collection_name="FIN7870",
            points=[
                models.PointStruct(
                    id=str(random_uuid),
                    payload={
                        "Chapter": requests.chapter,
                        "Title": requests.title,
                        "Problem": requests.problem,
                        "Question": requests.question,
                        "Answer": requests.answer,
                    },
                    vector=encoder.encode(f"{requests.messages}").tolist(),
                )
            ]
        )
        # print("Insert Success")
        return "Insert Success"
    except Exception as e:
        print(e)
        return e


if __name__ == "__main__":
    import uvicorn
    db_client = AsyncQdrantClient(host="vector-db", grpc_port=6334, prefer_grpc=True, timeout=7200)
    uvicorn.run(app, host="0.0.0.0", port=8000)
