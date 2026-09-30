from fastapi import APIRouter

router = APIRouter()

@router.post("/generate")
def generate_document():
    return {
        "document": "LegalEase AI document generation endpoint is working!"
    }
