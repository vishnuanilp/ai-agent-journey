from fastapi import FastAPI
import logging
import time
from router import route
from models import BusinessRequest

from dotenv import load_dotenv
import sentry_sdk
import os

load_dotenv()
sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"status": "Vocview backend is running"}

@app.post("/message")
async def message(request: BusinessRequest):
    answer = await route(request.message)
    return {"answer": answer}



@app.middleware("http")
async def add_timing(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info(f"{request.method} {request.url.path} took {duration:.2f}s")
    return response

