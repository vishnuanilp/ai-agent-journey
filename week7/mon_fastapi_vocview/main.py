from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, File, UploadFile
from models import BusinessRequest, BusinessResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import os
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()
sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"))
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://clinic-site.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.method} {request.url.path} took {duration:.3f}s")
    return response

@app.get("/")
def health_check():
    return {"status": "Vocview backend is running"}

@app.post("/message", response_model=BusinessResponse)
def handle_message(request: BusinessRequest):
    logger.info(f"Request received: {request.priority}")
    if request.business_type not in ["clinic", "shop", "hotel"]:
        raise HTTPException(status_code=400, detail="Unknown business type")
    return BusinessResponse(
        reply=f"Received your message: {request.message}",
        model_used="none-yet",
        confidence=1.0
    )

@app.get("/message/{customer_id}")
def get_messages(customer_id: int, priority: str = "all"):
    return {"customer_id": customer_id,
            "priority_filter": priority}


def get_pad():
    return "fresh order pad"

@app.get("/take-order")
def take_order(pad: str = Depends(get_pad)):
    return {"waiter_has": pad}

def send_email(customer_id: int):
    print(f"Sending confirmation email to customer {customer_id}...")

@app.get("/notify/{customer_id}")
def notify(customer_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, customer_id)
    return {"status": "reply sent, email will follow"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": len(contents)}

@app.get("/sentry-test")
def trigger_error():
    division_by_zero = 1 / 0