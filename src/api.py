from dotenv import load_dotenv
from fastapi import FastAPI, Response
import json
from routes.mods import get_mod
from routes.og import get_og
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"]
)

@app.get("/og")
async def og(url: str = None):
    if url is None:
        return Response(status_code=400, content="{\"details\": \"No URL provided\"}")
    status, data = get_og(url)
    if status == "success":
        return data
    else:
        return Response(status_code=400, content=json.dumps(data))
    
@app.get("/mods/{id}")
async def mods(id: str = None):
    if id is None:
        return Response(status_code=400, content="{\"details\": \"No ID provided\"}")
    return get_mod(id)