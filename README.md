# Customer Message Classifier

A simple AI-powered customer message classification system built with Python and Gemini API.

## Overview

This project demonstrates how to design a prompt as a structured interface between software and an AI model.

The system receives a customer message and asks Gemini to classify it into a structured format.

```text
Customer Message
       ↓
Prompt Contract
       ↓
Gemini
       ↓
Structured JSON
       ↓
Pydantic Validation
       ↓
Python Object

Features
Customer message classification
Prompt contract design
Structured JSON output
Category validation using Enum
Urgency validation from 1 to 5
Pydantic-based output validation
Gemini API error handling
Classification Rules
Category
Allowed values:

billing
technical
account
general
Urgency
Must be an integer between:

1 - 5

Summary
A concise summary of the customer message.

Example
Input
Saya sudah melakukan pembayaran tetapi saldo saya belum bertambah.

Output
{
  "category": "billing",
  "urgency": 4,
  "summary": "Pembayaran sudah dilakukan namun saldo belum bertambah."
}

Tech Stack
Python
Gemini API
Pydantic
python-dotenv
Project Structure
customer-message-classifier/
│
├── .venv/
├── .env
├── .gitignore
├── README.md
├── main.py
└── requirements.txt

Setup
1. Clone the repository
git clone <repository-url>
cd customer-message-classifier

2. Create virtual environment
ctivate virtual environment
Windows PowerShell:

.venv\Scripts\Activate.ps1

4. Install dependencies
pip install -r requirements.txt

5. Configure API key
Create a .env file:

GEMINI_API_KEY=your_api_key_here

6. Run
python main.py

Learning Goals
This project was built to understand:

Prompt as an interface
Input contract
Instruction contract
Output contract
Constraints
Structured AI output
AI response validation
Error handling when integrating an LLM into a Python application
