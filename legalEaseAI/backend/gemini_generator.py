import os

from dotenv import load_dotenv

load_dotenv()


class AIConfigurationError(Exception):
    pass


class AIGenerationError(Exception):
    pass


class GeminiDocumentGenerator:

    def __init__(self):

        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()

        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

        if not self.api_key:
            raise AIConfigurationError(
                "GEMINI_API_KEY is missing. "
                "Please add your API key to the .env file."
            )

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        effective_date,
        jurisdiction="Not specified",
        additional_instructions=""
    ):

        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)

            prompt = f"""
You are a professional AI legal document drafting assistant.

Generate a structured first-draft legal document.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE:
{effective_date}

JURISDICTION:
{jurisdiction}

TERMS AND CONDITIONS:
{terms}

ADDITIONAL INSTRUCTIONS:
{additional_instructions or "None"}

REQUIREMENTS:

1. Create a professional legal document.
2. Include a clear title.
3. Use numbered headings and subheadings.
4. Include an introduction.
5. Include all relevant clauses.
6. Include rights and responsibilities of parties.
7. Include payment and termination clauses when relevant.
8. Include confidentiality clauses when relevant.
9. Include signature sections.
10. Do not invent missing names, dates, amounts, or facts.
11. Mark missing information as [TO BE COMPLETED].
12. Include a section called Items for Legal Review.
13. Do not claim that the document is legally valid.
14. Use plain text without Markdown code fences.

Generate the complete document.
"""

            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=8192
                )
            )

            result = (response.text or "").strip()

            if not result:
                raise AIGenerationError(
                    "Gemini returned an empty response."
                )

            return result

        except (AIConfigurationError, AIGenerationError):
            raise

        except Exception as exc:
            raise AIGenerationError(
                f"Gemini API request failed: {exc}"
            ) from exc