# ⚖️ Legal Aid Provider

<p align="center">
  <b>Empowering Indian Citizens with Accessible, Accurate, and Plain-Language Legal Information</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/FastAPI-0.110+-009688.svg" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Ollama-llama3.2-orange.svg" alt="Ollama" />
  <img src="https://img.shields.io/badge/FAISS-Vector%20Search-green.svg" alt="FAISS" />
  <img src="https://img.shields.io/badge/License-MIT-purple.svg" alt="License" />
</p>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Legal Datasets Covered](#-legal-datasets-covered)
- [Technology Stack](#-technology-stack)
- [Directory Structure](#-directory-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [1. Ollama Setup](#1-ollama-setup)
  - [2. Backend Setup](#2-backend-setup)
  - [3. Database Configuration](#3-database-configuration)
  - [4. Frontend Setup](#4-frontend-setup)
- [RAG Pipeline & Embeddings](#-rag-pipeline--embeddings)
- [API Endpoints](#-api-endpoints)
- [Environment Configuration](#-environment-configuration)
- [Security & Privacy](#-security--privacy)
- [Disclaimer](#-disclaimer)

---

## 🏛️ Overview

**Legal Aid Provider** is an intelligent legal assistant tailored specifically to the Indian legal system. Most Indian citizens struggle to understand their legal rights, navigate complex legal statutes, or draft formal notices. This project bridges that gap by combining:

1. **Retrieval-Augmented Generation (RAG)** grounded in official Indian legal statutes (BNS, BNSS, Constitution of India, and major Acts).
2. **Local, Privacy-Preserving LLM Inference** via Ollama (`llama3.2`), preventing confidential user queries from leaking to external cloud APIs.
3. **Multilingual & Voice Support** with 8 Indian languages and speech recognition.
4. **User Authentication & History Storage** allowing citizens to revisit prior guidance securely.

---

## ✨ Key Features

- **Grounded Legal Knowledge (RAG)**: Fast vector search through thousands of indexed statutory provisions using FAISS and `sentence-transformers/all-MiniLM-L6-v2`.
- **Hallucination Prevention**: Strict system prompts instruct the LLM to only answer based on retrieved context and explicitly declare when statutory provisions do not provide sufficient information.
- **Multilingual Support**: Real-time prompt switching for English, Hindi (हिंदी), Tamil (தமிழ்), Telugu (తెలుగు), Bengali (বাংলা), Marathi (मराठी), Gujarati (ગુજરાતી), and Kannada (ಕನ್ನಡ).
- **Speech Recognition & Text-to-Speech**: Integrated browser Web Speech API for voice questions and spoken legal responses.
- **Topic Quick-Selectors**: Dedicated domain lenses for:
  - 🛒 *Consumer Rights* (Consumer Protection Act 2019, E-commerce rules)
  - 🏠 *Property & Rent* (Transfer of Property Act, Rent Control, RERA)
  - 💼 *Employment & Labour* (Industrial Disputes, POSH, Minimum Wages)
  - 👨‍👩‍👧 *Family & Marriage* (Personal laws, PWDVA 2005, Section 125 CrPC)
  - 🚔 *Criminal & FIR* (BNS 2023, BNSS 2023, Zero FIR, Bail provisions)
  - 📄 *RTI & Public Services* (RTI Act 2005, appeals, PIO timelines)
- **User Authentication & Session Management**:
  - Secure bcrypt password hashing and JWT token authorization.
  - Forgot password / reset password workflow with expiring tokens and Gmail SMTP email delivery.
  - Persistent conversation history with auto-save and deletion capabilities.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    User([Citizen / User]) -->|Voice / Text Query| Frontend[Frontend UI HTML5 / CSS3 / Vanilla JS]
    Frontend -->|REST API /api/chat| FastAPI[FastAPI Backend]

    subgraph RAG Pipeline
        FastAPI --> Embed[Sentence Transformer all-MiniLM-L6-v2]
        Embed --> FAISS[FAISS Vector Store legal_faiss.index]
        FAISS --> RelCheck{Relevance Threshold Check >= 0.50}
        RelCheck -->|Relevant| Context[Build Structured Legal Context]
        RelCheck -->|Insufficient| Fallback[Safe Fallback Notification]
    end

    Context --> Ollama[Local Ollama llama3.2]
    Ollama -->|Structured Legal Advice| FastAPI
    FastAPI -->|JSON Response with Legal Citations| Frontend
    Frontend -->|Render Markdown & Voice Readout| User

    subgraph Storage
        FastAPI --> DB[(MySQL / SQLite Database)]
        DB --> Users[Users Table]
        DB --> Convos[Conversations Table]
    end
```

---

## 📚 Legal Datasets Covered

The knowledge base compiles structured legal data into unified datasets located in the `Data/` directory:

- **Bharatiya Nyaya Sanhita (BNS), 2023**: Modernized criminal penal code.
- **Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023**: Procedural criminal code replacing the CrPC.
- **Constitution of India**: Complete articles, preamble, schedules, and appendices.
- **Prevention of Corruption Act, 1988 (PCA)**.
- Additional Acts covering consumer protection, property rights, tenancy, and RTI.

---

## 🛠️ Technology Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/), [SQLAlchemy](https://www.sqlalchemy.org/), [Pydantic](https://docs.pydantic.dev/)
- **Database**: MySQL / MariaDB (via PyMySQL) or SQLite
- **Security**: Passlib (Bcrypt), Python-Jose (JWT), Python-Multipart
- **Embeddings & Vector Search**: [Sentence-Transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`), [FAISS](https://github.com/facebookresearch/faiss) (`faiss-cpu`), NumPy
- **LLM Engine**: [Ollama](https://ollama.com/) running `llama3.2`
- **Frontend**: Vanilla JavaScript (ES6+), Modern Semantic HTML5, Custom Responsive CSS (Dark Gold/Navy design system), Web Speech API
- **Email Service**: Python `smtplib` via Gmail SMTP SSL

---

## 📂 Directory Structure

```text
Aid Provider/
├── Data/                                    # Raw and processed legal datasets
│   ├── Acts/                                # Specific statute datasets (PCA, etc.)
│   ├── Bharatiya Nyay Sanhita/              # BNS legal corpus & JSON chunks
│   ├── Bhartiya Nyay Suraksha Sanhita/      # BNSS legal corpus & schedules
│   ├── Indian Constitution/                 # Constitution articles, schedules, PDF
│   ├── unified_legal_dataset.jsonl          # Unified dataset
│   └── unified_legal_dataset_cleaned.jsonl  # Cleaned dataset used for FAISS index
├── Frontend/                                # Responsive web client
│   ├── index.html                           # Landing page
│   ├── chat.html                            # Core AI legal chat interface
│   ├── about.html                           # Mission and statutory coverage page
│   ├── login.html                           # Authentication (Sign in / Sign up)
│   ├── forgot-password.html                 # Request password reset link
│   ├── reset-password.html                  # Change password with token
│   ├── script.js                            # Chat logic, speech API, system prompts
│   ├── auth.js                              # Client auth helper & token manager
│   ├── history.js                           # Conversation drawer and auto-save
│   ├── animations.js                        # Particle canvas and typewriter effects
│   └── style.css                            # Complete CSS design system
├── backend/                                 # FastAPI application
│   ├── models/                              # SQLAlchemy database models
│   │   ├── user.py                          # User account model
│   │   └── conversation.py                  # Conversation history model
│   ├── rag/                                 # RAG services and search
│   │   ├── index/                           # FAISS index and metadata storage
│   │   ├── embedding_service.py             # SentenceTransformer embedding logic
│   │   ├── search.py                        # FAISS similarity search
│   │   ├── rag_service.py                   # Context builder & relevance filter
│   │   ├── loader.py                        # Dataset normalization scripts
│   │   └── build_faiss_index.py             # Script to generate FAISS index
│   ├── routes/                              # API routing endpoints
│   │   ├── auth.py                          # Signup, login, password reset
│   │   ├── chat.py                          # RAG + LLM chat endpoint
│   │   └── history.py                       # Conversation management endpoints
│   ├── services/                            # External services
│   │   └── llm_service.py                   # Ollama HTTP client
│   ├── utils/                               # Helper utilities
│   │   └── email.py                         # SMTP password reset email dispatcher
│   ├── database.py                          # Database session setup
│   ├── main.py                              # FastAPI entry point & CORS
│   ├── requirements.txt                     # Python package dependencies
│   └── .env.example                         # Environment configuration template
├── .env.example                             # Root environment configuration template
├── .gitignore                               # Git ignore rules
└── README.md                                # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **MySQL / MariaDB** (or SQLite)
- **[Ollama](https://ollama.com/)** installed locally

---

### 1. Ollama Setup

1. Download and install Ollama from [ollama.com](https://ollama.com/).
2. Pull the default model:
   ```bash
   ollama run llama3.2
   ```
3. Ensure the Ollama server is running on `http://localhost:11434`.

---

### 2. Backend Setup

1. Open your terminal and navigate to the `backend/` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your `.env` file:
   ```bash
   # Copy the example environment template
   cp .env.example .env
   ```
5. Edit `backend/.env` with your database credentials and settings (see [Environment Configuration](#-environment-configuration)).

---

### 3. Database Configuration

Create your database in MySQL:

```sql
CREATE DATABASE legalaid CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Update `DATABASE_URL` in `backend/.env` to point to your database:
```env
DATABASE_URL=mysql+pymysql://root:your_password@127.0.0.1:3307/legalaid
```

Run the backend server. Tables are created automatically on first run:
```bash
uvicorn main:app --reload --port 8000
```

Verify backend health at: [http://localhost:8000/](http://localhost:8000/)

---

### 4. Frontend Setup

You can serve the `Frontend/` folder using any static HTTP server or VS Code Live Server:

```bash
# Using Python's built-in HTTP server:
cd Frontend
python -m http.server 3000
```

Open your browser at: [http://127.0.0.1:3000](http://127.0.0.1:3000)

---

## 🔍 RAG Pipeline & Embeddings

The RAG pipeline works as follows:

1. **Ingestion & Normalization**: Legal provisions from `Data/` are parsed, cleaned of placeholder artifacts, and normalized in `unified_legal_dataset_cleaned.jsonl`.
2. **Embedding**: `backend/rag/build_index.py` converts provisions into 384-dimensional dense vectors using `all-MiniLM-L6-v2`.
3. **Indexing**: `backend/rag/build_faiss_index.py` stores normalized vectors in `legal_faiss.index` using Inner Product (cosine similarity).
4. **Retrieval**: When a citizen asks a question, `search_legal_provisions()` retrieves top-$k$ matches ($k=5$).
5. **Relevance Gating**: If the top similarity score is below `0.50`, the assistant safely informs the citizen that reliable statutory provisions were not found rather than fabricating an answer.

To rebuild the vector index at any time:
```bash
python backend/rag/build_index.py
python backend/rag/build_faiss_index.py
```

---

## 📡 API Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/` | Backend health check | No |
| `POST` | `/api/auth/signup` | Register a new user | No |
| `POST` | `/api/auth/login` | Login and receive JWT access token | No |
| `POST` | `/api/auth/forgot-password` | Request password reset email | No |
| `POST` | `/api/auth/reset-password` | Reset password using reset token | No |
| `POST` | `/api/chat` | Send question, retrieve context & stream LLM answer | No |
| `GET` | `/api/history/` | List user conversation sessions | **Yes** (Bearer) |
| `GET` | `/api/history/{id}` | Retrieve specific conversation messages | **Yes** (Bearer) |
| `POST` | `/api/history/save` | Create or update a conversation session | **Yes** (Bearer) |
| `DELETE` | `/api/history/{id}` | Delete a conversation session | **Yes** (Bearer) |

---

## 🔐 Environment Configuration

Create a `.env` file inside `backend/` based on `backend/.env.example`:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://root:your_password@127.0.0.1:3307/legalaid

# JWT Authentication
SECRET_KEY=generate_a_secure_random_hex_string

# Email Dispatch (Gmail SMTP for password resets)
MAIL_EMAIL=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password

# Ollama LLM Service
OLLAMA_URL=http://localhost:11434/api/chat
OLLAMA_MODEL=llama3.2

# Frontend URL (Used in reset links)
FRONTEND_URL=http://127.0.0.1:3000

# Optional External API
ANTHROPIC_API_KEY=your_key_here
```

---

## 🛡️ Security & Privacy

- **No Data Leakage**: By default, inference is routed to local Ollama. Private citizen disputes are never sent to third-party proprietary LLMs unless explicitly reconfigured.
- **Password Protection**: Passwords are saved exclusively as salted bcrypt hashes.
- **Git Safety**: Secrets, SQLite files, installer binaries (`OllamaSetup.exe`), and virtual environments are strictly blocked by `.gitignore`.

---

## ⚠️ Disclaimer

> **IMPORTANT**: Legal Aid Provider provides general legal information for educational and self-help purposes based on Indian statutes. **It does not provide formal legal advice, represent individuals, or create an attorney-client relationship.** For court representation, formal litigation, or critical legal emergencies, always consult a licensed advocate registered with the Bar Council of India.
