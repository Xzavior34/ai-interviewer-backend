# 🚀 AI Interview Screener (Backend)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-teal.svg)
![Architecture](https://img.shields.io/badge/Architecture-Microservice-orange)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Coverage](https://img.shields.io/badge/Tests-Passing-green)

A high-performance, asynchronous backend service designed to automate the technical screening process. This microservice accepts candidate answers, utilizes an LLM for semantic evaluation, and ranks candidates concurrently.

## 📖 Table of Contents
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Key Features](#-key-features)
- [Installation & Setup](#-installation--setup)
- [API Reference](#-api-reference)
- [Design Decisions (The "Why")](#-design-decisions)

---

## 🏗 System Architecture

The application follows a **Service-Layer Pattern** to decouple business logic from the HTTP transport layer.


graph LR
    A[Client] -->|POST JSON| B(FastAPI Router)
    B -->|Validate| C{Pydantic Models}
    C -->|Valid Data| D[Service Layer]
    D -->|Async Request| E[OpenAI GPT-3.5]
    E -->|JSON Response| D
    D -->|Result| A
--'
## project-structure

/ai-interviewer-backend
│
├── app/
│   ├── main.py            # Application Entry Point
│   ├── models.py          # Pydantic Schemas (Data Contracts)
│   ├── services.py        # Business Logic (LLM Integration)
│   └── config.py          # Environment Configuration
│
├── tests/                 # Pytest Suite
├── Dockerfile             # Containerization
├── requirements.txt       # Dependencies
└── README.md              # Documentation
## ✨ Key Features
​Strict Type Safety: Leverages Pydantic for rigorous request/response validation. Prevents "garbage in" data from reaching the logic layer.
​Deterministic AI Outputs: Utilizes OpenAI's response_format={"type": "json_object"} to guarantee the LLM returns parseable JSON, eliminating brittle regex parsing.
​High-Concurrency Ranking: The /rank-candidates endpoint uses asyncio.gather to process generic candidate batches in parallel.
​Result: Latency is bounded by the slowest single request (O(1)), rather than the sum of all requests (O(n)).
​Production Ready: Includes strict error handling, environment configuration via .env, and Docker containerization.
​## 🛠 Installation & Setup
​Prerequisites
​Python 3.9+
​Docker (Optional)
​OpenAI API Key

## Clone the repository:
git clone [https://github.com/YOUR_USERNAME/ai-interviewer-backend.git](https://github.com/YOUR_USERNAME/ai-interviewer-backend.git)
cd ai-interviewer-backend
## Set up Environment:
Create a .env file in the root directory:
OPENAI_API_KEY=sk-your-actual-api-key-here
## Install Dependencies:
pip install -r requirements.txt
## Run the Server:
uvicorn app.main:app --reload
Server will start at http://localhost:8000
## 🧠 Design Decisions
​1. Why FastAPI over Node.js?
​While Node.js is excellent for I/O-bound tasks, FastAPI was selected for:
​Data Integrity: The integration with Pydantic ensures that data contracts are enforced before code execution. In an AI API, valid data structure is critical.
​Native AI Ecosystem: Python is the native language of AI. If we need to expand to use LangChain, local HuggingFace models, or RAG, Python libraries are superior.
​Async Performance: Python's async/await syntax handles the latency of LLM API calls efficiently, similar to Node's Event Loop.
​2. Why GPT-3.5-Turbo + JSON Mode?
​Reliability: Generative models can be unpredictable. By enforcing json_object mode, we shift the burden of structuring data from the application logic to the model itself.
​Cost/Speed: For a screening task, GPT-4 is overkill. GPT-3.5-Turbo provides the optimal balance of reasoning capability and latency
## Running Tests
​We use pytest for unit testing.
pytest
