
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os
import time
import traceback

# Load environment variables
load_dotenv("front.end/.env")

app = FastAPI(title="LegalEase AI")


# Document Request Model
class DocumentRequest(BaseModel):
    document_type: str
    party1: str
    party2: str
    terms: str
    effective_date: str


# Home Route
@app.get("/")
def home():
    return {
        "message": "LegalEase AI Backend Running"
    }


# Health Check
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# Generate Document
@app.post("/generate")
def generate_document(data: DocumentRequest):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key not configured. Check your .env file."
        )

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
You are a legal document drafting assistant.

Create a structured draft for a {data.document_type}.

First Party: {data.party1}
Second Party: {data.party2}
Terms: {data.terms}
Effective Date: {data.effective_date}

Include the following sections:

1. Document Title
2. Introduction
3. Parties Information
4. Terms and Conditions
5. Payment Details
6. Responsibilities of Both Parties
7. Termination Clause
8. Signature Sections

Instructions:
- Use clear and formal language.
- Use placeholders for missing information.
- Do not invent missing personal or legal details.
- Include a note that a qualified lawyer should review
  the draft before signing.
"""

        response = None

        for attempt in range(3):

            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                break

            except Exception as e:

                error_message = str(e)

                # 429 Quota Exceeded
                if (
                    "429" in error_message
                    or "RESOURCE_EXHAUSTED" in error_message
                ):
                    raise HTTPException(
                        status_code=429,
                        detail=(
                            "Gemini API free quota exceeded. "
                            "Please check your Google AI Studio usage "
                            "and try again after quota reset."
                        )
                    )

                # 503 Temporary Unavailable
                if (
                    "503" in error_message
                    or "UNAVAILABLE" in error_message
                ):

                    print(
                        f"Gemini busy. Retry attempt "
                        f"{attempt + 1}/3"
                    )

                    if attempt < 2:
                        time.sleep(5 * (attempt + 1))
                        continue

                    raise HTTPException(
                        status_code=503,
                        detail=(
                            "Gemini AI is temporarily busy. "
                            "Please try again later."
                        )
                    )

                # Other API Errors
                raise HTTPException(
                    status_code=500,
                    detail=f"Gemini API Error: {error_message}"
                )

        # Check Empty Response
        if response is None or not response.text:
            raise HTTPException(
                status_code=502,
                detail="Gemini returned an empty response."
            )

        return {
            "status": "success",
            "document": response.text
        }

    except HTTPException:
        raise

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )