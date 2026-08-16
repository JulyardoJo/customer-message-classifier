Tentu. Untuk portfolio, README sebaiknya tidak hanya menjelaskan cara menjalankan project, tetapi juga menunjukkan bahwa Anda memahami problem, architecture, design decision, dan AI engineering concept di baliknya.

Ganti seluruh isi README.md Anda dengan versi berikut:

# Customer Message Classifier

An AI-powered customer message classification system built with Python and the Gemini API.

This project demonstrates how to design a **prompt as an interface between software and an AI model**, enforce structured output, validate AI-generated data, and safely integrate the result into a Python application.

---

## Overview

Customer support applications often need to transform unstructured customer messages into structured data that can be processed by software.

For example:

```text
"I already made a payment, but my balance has not increased."


The system transforms the message into:

{
  "category": "billing",
  "urgency": 4,
  "summary": "Payment was completed but the balance has not increased."
}


The overall pipeline is:

Customer Message
       ↓
Prompt Contract
       ↓
Gemini API
       ↓
Structured JSON
       ↓
Pydantic Validation
       ↓
Python Object
       ↓
Application Logic

Project Goals

This project was built to understand several fundamental AI Engineering concepts:

Designing prompts as software interfaces
Separating input, instruction, and output contracts
Constraining LLM output
Using structured JSON responses
Representing business rules as schemas
Validating AI-generated data with Pydantic
Handling external API failures
Treating LLM output as untrusted external data

The goal is not simply to generate a correct answer, but to make the AI output structured, predictable, and usable by software.

Business Requirements

The classifier produces three fields:

Category

The category must be one of:

billing
technical
account
general

Urgency

The urgency level must be an integer between:

1 - 5

Summary

The summary must be concise and represent the main issue described by the customer.

Prompt as an Interface

A basic prompt such as:

Analyze this customer message.


leaves too much room for interpretation.

This project instead uses a structured prompt contract containing:

ROLE
  ↓
TASK
  ↓
INPUT
  ↓
OUTPUT REQUIREMENTS
  ↓
CONSTRAINTS


Conceptually:

You are a customer support classifier.

Analyze the customer message.

Customer message:
...

Return:
- category
- urgency
- summary

Rules:
- category must be billing, technical, account, or general
- urgency must be between 1 and 5
- summary must be concise


The prompt therefore acts as an instructional interface between the application and the AI model.

Structured Output

The application requests JSON instead of free-form text.

Expected structure:

{
  "category": "billing",
  "urgency": 4,
  "summary": "Payment was completed but the balance has not increased."
}


This makes the model output easier for application code to consume.

Output Contract

The output contract is represented using Pydantic.

class Category(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    ACCOUNT = "account"
    GENERAL = "general"


class CustomerClassification(BaseModel):
    category: Category
    urgency: int = Field(
        ge=1,
        le=5
    )
    summary: str


This translates business requirements into explicit program constraints.

For example:

Business Rule
     ↓
category must be one of four values
     ↓
Enum


and:

Business Rule
     ↓
urgency must be 1–5
     ↓
Field(ge=1, le=5)

Validation

The response from Gemini is treated as external data and is not blindly trusted.

The application validates the response using:

result = CustomerClassification.model_validate_json(
    response.text
)


The process becomes:

AI Response
     ↓
JSON
     ↓
Pydantic Validation
     ↓
CustomerClassification
     ↓
Application


This provides a boundary between probabilistic AI output and deterministic application logic.

Error Handling

The Gemini API is an external dependency, so the application handles API errors explicitly.

try:
    response = client.models.generate_content(...)
    result = CustomerClassification.model_validate_json(response.text)

except errors.APIError as error:
    print(f"Gemini API error: {error}")


The project was tested with both:

Successful API request
billing
4
Payment was completed but the balance has not increased.

Invalid API credentials
Gemini API error: 401 UNAUTHENTICATED


The second test demonstrates that an external API failure is handled without exposing an uncontrolled Python traceback to the user.

Prompt Experiment

The project also compares two prompt approaches.

Prompt A — Weak
Analyze this customer message.


This allows the model to interpret the task more freely and may produce output that does not match the application's expected structure.

Prompt B — Contract-Based

The second prompt explicitly defines:

Role
Task
Input
Output fields
Allowed category values
Urgency range
Summary constraint

The experiment demonstrates an important AI Engineering principle:

More explicit specifications can reduce ambiguity between the application's requirements and the model's interpretation.

Architecture
┌──────────────────────────┐
│ Customer Message         │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Prompt Contract          │
│                          │
│ Role                     │
│ Task                     │
│ Input                    │
│ Output Requirements      │
│ Constraints              │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Gemini API               │
│ gemini-3.1-flash-lite    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Structured JSON          │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Pydantic Validation      │
│                          │
│ Enum                     │
│ Type Validation          │
│ Range Constraints        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Python Object            │
│ CustomerClassification   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Application Logic        │
└──────────────────────────┘

Project Structure
customer-message-classifier/
│
├── .venv/
├── .env
├── .gitignore
├── README.md
├── main.py
└── requirements.txt

File Responsibilities
File	Responsibility
main.py	Application logic, prompt, Gemini request, schema, validation, and error handling
.env	Local API key configuration
.gitignore	Prevents secrets and virtual environment files from being committed
requirements.txt	Python dependencies
README.md	Project documentation

.env and .venv/ are intentionally excluded from version control.

Tech Stack
Python
Google Gemini API
Google GenAI Python SDK
Pydantic
python-dotenv
Requirements

Before running the project, make sure you have:

Python 3.10+
A Gemini API key
Git
Installation
1. Clone the repository
git clone <repository-url>
cd customer-message-classifier

2. Create a virtual environment

Windows PowerShell:

python -m venv .venv

3. Activate the virtual environment
.venv\Scripts\Activate.ps1

4. Install dependencies
pip install -r requirements.txt

Environment Configuration

Create a .env file in the project root:

GEMINI_API_KEY=your_api_key_here


Never commit the .env file to GitHub.

The .gitignore file already excludes it from version control.

Running the Application

Run:

python main.py


Example output:

billing
4
Payment was completed but the balance has not increased.

Key AI Engineering Insights

This project demonstrates several important principles.

1. Prompt ≠ Validation

A prompt can instruct the model:

urgency must be between 1 and 5


but application code should still validate the result.

2. LLM Output Should Be Treated as External Data

The application should not assume:

AI output = trusted data


Instead:

AI output
    ↓
Parse
    ↓
Validate
    ↓
Application

3. Business Rules Should Become Explicit Constraints

Instead of relying entirely on natural-language instructions:

"Choose an appropriate category."


the application defines:

billing
technical
account
general


and enforces those values through a schema.

4. Reliability Requires Multiple Layers

A reliable AI application should not depend on prompt quality alone.

A stronger architecture combines:

Prompt
  +
Structured Output
  +
Schema
  +
Validation
  +
Error Handling
  +
Testing

Limitations

This project is intentionally designed as a learning project and is not production-ready.

Potential improvements include:

Separating application logic into multiple modules
Adding unit and integration tests
Creating a larger evaluation dataset
Measuring classification accuracy
Adding structured logging
Adding retry and backoff strategies
Adding input validation
Tracking model and prompt versions
Adding observability and usage monitoring
Building a REST API around the classifier
Future Improvements

Possible next iterations:

Current
   ↓
Single Python script
   ↓
Refactor into modules
   ↓
Add automated tests
   ↓
Add evaluation dataset
   ↓
Add FastAPI
   ↓
Containerize
   ↓
Deploy

Learning Outcome

The main lesson from this project is:

AI Engineering is not only about prompting an LLM. It is about designing the interface around the model so that probabilistic AI behavior can be integrated into reliable software systems.

This project represents an initial implementation of that principle using prompt contracts, structured output, schema validation, and Python.

Jangan commit dulu. Kirim hasil git status kepada saya, lalu kita lakukan Step berikutnya: review GitHub repository sebelum push.
