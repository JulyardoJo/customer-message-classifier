import os
from enum import Enum

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from pydantic import BaseModel, Field


class Category(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    ACCOUNT = "account"
    GENERAL = "general"


class CustomerClassification(BaseModel):
    category: Category = Field(
        description="The customer issue category."
    )
    urgency: int = Field(
        ge=1,
        le=5,
        description="Urgency level from 1 to 5."
    )
    summary: str = Field(
        description="A concise summary of the customer message."
    )


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


customer_message = """
Saya sudah melakukan pembayaran tetapi saldo saya belum bertambah.
"""


prompt = f"""
You are a customer support classifier.

Analyze the customer message below.

Customer message:
{customer_message}

Return the result with:
- category
- urgency
- summary

Rules:
- category must be billing, technical, account, or general
- urgency must be an integer between 1 and 5
- summary must be concise
"""


try:
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": CustomerClassification.model_json_schema(),
        },
    )

    result = CustomerClassification.model_validate_json(response.text)

except errors.APIError as error:
    print(f"Gemini API error: {error}")

except Exception as error:
    print(f"Unexpected error: {error}")

else:
    print(result.category.value)
    print(result.urgency)
    print(result.summary)
