from fastapi import FastAPI
import logging
import time
import os
from router import route
from models import BusinessRequest
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from streaming import stream_tokens
from db import get_owner_id, save_question, save_answer
from dotenv import load_dotenv
import sentry_sdk

load_dotenv()
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("ENVIRONMENT", "development"),
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_timing(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info(f"{request.method} {request.url.path} took {duration:.2f}s")
    return response


@app.get("/")
async def home():
    return {"status": "Vocview backend is running"}


@app.post("/message")
async def message(request: BusinessRequest):
    answer = await route(request.message)
    return {"answer": answer}


@app.get("/stream")
async def stream(message: str, business_type: str = "salon"):
    owner_id = await get_owner_id()
    row_id = await save_question(owner_id, message, business_type)

    async def event_stream():
        collected = []
        try:
            async for piece in stream_tokens(message):
                collected.append(piece)
                yield f"data: {piece}\n\n"
            yield "event: done\ndata: ok\n\n"
        except Exception as e:
            logger.exception("stream failed")
            sentry_sdk.capture_exception(e)
            yield "event: error\ndata: Sorry, something went wrong.\n\n"
        finally:
            if collected:
                await save_answer(row_id, "".join(collected))

    return StreamingResponse(event_stream(), media_type="text/event-stream")