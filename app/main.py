from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ScanResponse
from app.ai_service import analyze_image_pipeline

app = FastAPI(title="ReUse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@app.get("/")
def read_root():
    return {"message": "ReUse backend is running"}


@app.post("/scan", response_model=ScanResponse)
async def scan_object(image: UploadFile = File(...)):
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    image_bytes = await image.read()

    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty file.")

    if len(image_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Image too large.")

    try:
        result = analyze_image_pipeline(image_bytes, location="Brazil")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))