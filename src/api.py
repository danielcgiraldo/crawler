from dotenv import load_dotenv
from fastapi import FastAPI, Response
import json

from src.routes.og import get_og

load_dotenv()

app = FastAPI()

@app.get("/og")
async def og(url: str = None):
    if url is None:
        return Response(status_code=400, content="{\"details\": \"No URL provided\"}")
    status, data = get_og(url)
    if status == "success":
        return data
    else:
        return Response(status_code=400, content=json.dumps(data))