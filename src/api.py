from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import json
from src.routes.mods import get_mod
from src.routes.og import get_og

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
async def mods(request: Request, id: str = None):
    # get user-agent from request
    user_agent = request.headers.get('User-Agent')

    if id is None:
        return Response(status_code=400, content="{\"details\": \"No ID provided\"}")
    return get_mod(id, user_agent)