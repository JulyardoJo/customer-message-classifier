# Customer Message Classifier

An AI-powered customer message classification system built with Python and the Google Gemini API.

This project demonstrates how to design a **prompt as an interface between software and an AI model**, generate structured output, validate AI-generated data, and integrate the result into a Python application.

## Overview

Customer support applications often need to transform unstructured customer messages into structured data that can be processed by software.

### Input

> Saya sudah melakukan pembayaran tetapi saldo saya belum bertambah.

### Output

```json
{
  "category": "billing",
  "urgency": 4,
  "summary": "Pembayaran sudah dilakukan namun saldo belum bertambah."
}
```

### Pipeline

```text
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
```

## Project Goals

This project was built to understand several fundamental AI Engineering concepts:

- Designing prompts as software interfaces
- Defining input, instruction, and output contracts
- Constraining LLM output
- Generating structured JSON responses
- Representing business rules as schemas
- Validating AI-generated data with Pydantic
- Handling external API failures
- Treating LLM output as untrusted external data

The goal is not simply to generate a correct answer, but to make AI output **structured, predictable, and usable by software**.

## Business Requirements

The classifier produces three fields.

### Category

The category must be one of:

- `billing`
- `technical`
- `account`
- `general`

### Urgency

The urgency must be an integer between `1` and `5`.

### Summary

The summary must be concise and represent the main issue described by the customer.

## Prompt as an Interface

A basic prompt such as:

```text
Analyze this customer message.
```

leaves too much room for interpretation.

This project instead uses a structured prompt contract containing:

```text
ROLE
  ↓
TASK
  ↓
INPUT
  ↓
OUTPUT REQUIREMENTS
  ↓
CONSTRAINTS
```

The prompt specifies:

- **Role** — what the AI is supposed to act as
- **Task** — what the AI must do
- **Input** — the customer message to analyze
- **Output** — the information the application expects
- **Constraints** — allowed values and limitations

The prompt therefore acts as an **instructional interface between the application and the AI model**.

## Structured Output

The application requests a structured JSON response instead of free-form text.

Expected structure:

```json
{
  "category": "billing",
  "urgency": 4,
  "summary": "Pembayaran sudah dilakukan namun saldo belum bertambah."
}
```

Structured output makes the AI response easier for application code to consume.

## Output Contract

The expected output is represented using Pydantic.

```python
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
```

This translates business requirements into explicit program constraints.

For example:

```text
Business Rule
     ↓
category must be one of four values
     ↓
Enum
```

And:

```text
Business Rule
     ↓
urgency must be between 1 and 5
     ↓
Field(ge=1, le=5)
```

## Validation

The response from Gemini is treated as external data and is not blindly trusted.

The application validates the response using:

```python
result = CustomerClassification.model_validate_json(
    response.text
)
```

The validation flow is:

```text
AI Response
     ↓
JSON
     ↓
Pydantic Validation
     ↓
CustomerClassification
     ↓
Application
```

This creates a boundary between probabilistic AI output and deterministic application logic.

## Error Handling

The Gemini API is an external dependency, so the application handles API errors explicitly.

```python
try:
    response = client.models.generate_content(...)
    result = CustomerClassification.model_validate_json(response.text)

except errors.APIError as error:
    print(f"Gemini API error: {error}")
```

The application was tested with both successful and failed API requests.

### Successful Request

```text
billing
4
Pembayaran sudah dilakukan namun saldo belum bertambah.
```

### Invalid API Credentials

```text
Gemini API error: 401 UNAUTHENTICATED
```

The second test demonstrates that an external API failure is handled without exposing an uncontrolled Python traceback.

## Prompt Experiment

This project compares two prompt approaches.

### Version A — Weak Prompt

```text
Analyze this customer message.
```

This provides very little information about the expected task and output format.

### Version B — Contract-Based Prompt

The second prompt explicitly defines:

- Role
- Task
- Input
- Output fields
- Allowed category values
- Urgency range
- Summary constraint

The experiment demonstrates an important AI Engineering principle:

> More explicit specifications can reduce ambiguity between application requirements and model interpretation.

The purpose of the experiment is not to find a universally "best" prompt, but to understand how prompt specifications influence model behavior and output consistency.

## Architecture

```text
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
```

## Project Structure

```text
customer-message-classifier/
│
├── .venv/
├── .env
├── .gitignore
├── README.md
├── main.py
└── requirements.txt
```

### File Responsibilities

| File | Responsibility |
|---|---|
| `main.py` | Application logic, prompt, Gemini request, schema, validation, and error handling |
| `.env` | Local API key configuration |
| `.gitignore` | Prevents secrets and virtual environment files from being committed |
| `requirements.txt` | Python dependencies |
| `README.md` | Project documentation |

> `.env` and `.venv/` are intentionally excluded from version control.

## Tech Stack

- Python
- Google Gemini API
- Google GenAI Python SDK
- Pydantic
- python-dotenv

## Requirements

Before running the project, make sure you have:

- Python 3.10 or higher
- A Gemini API key
- Git

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd customer-message-classifier
```

### 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
```

### 3. Activate the Virtual Environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Never commit the `.env` file to GitHub.

The `.gitignore` file is configured to exclude it from version control.

## Running the Application

Run:

```powershell
python main.py
```

Example output:

```text
billing
4
Pembayaran sudah dilakukan namun saldo belum bertambah.
```

## Key AI Engineering Insights

### 1. Prompt Is an Interface

A prompt in an AI application is not simply a question. It defines how the application communicates its requirements to the model.

A well-defined prompt can specify:

```text
Role
Task
Input
Output
Constraints
```

### 2. Prompt Is Not Validation

A prompt can instruct the model:

```text
urgency must be between 1 and 5
```

But the application should still validate the result.

```text
Prompt
  ↓
Model Guidance

Schema + Validation
  ↓
Application Safety
```

### 3. LLM Output Should Be Treated as External Data

The application should not assume:

```text
AI output = trusted data
```

Instead:

```text
AI Output
    ↓
Parse
    ↓
Validate
    ↓
Application
```

### 4. Business Rules Should Become Explicit Constraints

Instead of relying only on natural-language instructions:

```text
Choose an appropriate category.
```

the application explicitly defines:

```text
billing
technical
account
general
```

and enforces those values through a schema.

### 5. Reliability Requires Multiple Layers

Reliable AI applications should not depend on prompt quality alone.

A stronger architecture combines:

```text
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
  +
Evaluation
```

## Limitations

This project is intentionally designed as a learning project and is **not production-ready**.

Potential improvements include:

- Separating application logic into multiple modules
- Adding unit and integration tests
- Creating a larger evaluation dataset
- Measuring classification accuracy
- Adding structured logging
- Adding retry and backoff strategies
- Adding input validation
- Tracking model and prompt versions
- Adding observability and usage monitoring
- Building a REST API around the classifier

## Future Improvements

Possible next iterations:

```text
Current
   ↓
Single Python Script
   ↓
Modular Architecture
   ↓
Automated Tests
   ↓
Evaluation Dataset
   ↓
FastAPI
   ↓
Containerization
   ↓
Deployment
```

## Learning Outcome

The main lesson from this project is:

> **AI Engineering is not only about prompting an LLM. It is about designing the interface around the model so that probabilistic AI behavior can be integrated into structured, validated, testable, and maintainable software systems.**

This project represents an initial implementation of that principle using:

- Prompt contracts
- Structured output
- Schema validation
- Pydantic
- Error handling
- Python application logic
