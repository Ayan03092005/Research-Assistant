# Smart Research Assistant (R-Agents)

A **GenAI-powered Smart Research Assistant** designed to automate the **end-to-end academic research workflow** — from literature discovery to LaTeX-ready paper generation — within a single unified platform.

---

## 🚀 Overview

The exponential growth of academic publications has made manual research workflows time-consuming and error-prone. **Smart Research Assistant (R-Agents)** addresses this challenge by combining **Generative AI, scholarly APIs, and a modular full-stack architecture** to assist students, researchers, reviewers, and faculty.

The system automates:
- Literature surveys
- Research gap identification
- Methodology drafting
- Citation validation
- Multilingual translation
- Persona-based summarization
- Interdisciplinary synthesis
- LaTeX report generation

All features operate inside a **single, scalable, and ethical research ecosystem**.

---

## ✨ Key Features

- 📚 **Literature Survey Generator** – Fetches and synthesizes papers from Semantic Scholar, OpenAlex, CrossRef, and Unpaywall
- 🔍 **Research Gap Finder** – Identifies underexplored areas and limitations
- 🧪 **Methodology Builder** – Generates structured experimental or procedural sections
- 📖 **Citation Validator** – DOI-based reference verification with APA/IEEE formatting
- 👤 **Persona-Based Summarizer** – Tailors summaries for students, reviewers, or faculty
- 🌍 **Multilingual Translator** – Cross-language paper translation and summarization
- 🔗 **Cross-Domain Synthesizer** – Connects insights across unrelated research fields
- ⚠️ **Contradiction Analyzer** – Detects claim–evidence inconsistencies
- 📊 **Benchmark Explorer** – Suggests datasets, metrics, and evaluation standards
- 🧾 **LaTeX Generator** – Produces publication-ready `.tex` files
- 🎙️ **Voice/Text I/O** – Speech input and TTS output for accessibility

---

## 🧠 Tech Stack

### Frontend
- React
- Tailwind CSS

### Backend
- FastAPI (Async, Modular)
- Python 3.10+

### Database
- PostgreSQL
- SQLAlchemy ORM

### AI / LLM Layer
- OpenAI GPT-4o
- Google Gemini 1.5 Pro
- Switchable LLM orchestration (`llm_utils.py`)

### External APIs
- Semantic Scholar
- OpenAlex
- CrossRef
- Unpaywall

---

## 🏗️ System Architecture

### 1️⃣ High-Level Architecture

```
┌────────────────────┐
│   React Frontend   │
│ (Tailwind UI)      │
└─────────▲──────────┘
          │ REST APIs
┌─────────┴──────────┐
│   FastAPI Backend  │
│ (Async Modules)    │
└─────────▲──────────┘
          │
┌─────────┴──────────┐
│   LLM Orchestrator │◄── GPT-4o / Gemini
│   (llm_utils.py)   │
└─────────▲──────────┘
          │
┌─────────┴──────────┐
│ Scholarly APIs     │
│ (SS, OpenAlex,     │
│  CrossRef, etc.)   │
└────────────────────┘
          │
┌────────────────────┐
│ PostgreSQL Database│
└────────────────────┘
```

---

### 2️⃣ Layered Architecture

```
[ UI Layer ]
React + Tailwind CSS

[ Application Layer ]
FastAPI Routes (Modular Services)

[ AI / LLM Layer ]
Prompt Templates + Model Switching

[ Data Layer ]
PostgreSQL + ORM

[ File Layer ]
PDF Uploads | .tex Exports | Audio
```

---

### 3️⃣ Module-Level Architecture

Each research feature is implemented as an **independent module**:

```
/api
 ├── literature
 ├── gap_analysis
 ├── methodology
 ├── citation_validator
 ├── translator
 ├── persona_summary
 ├── cross_domain
 ├── contradiction
 ├── latex_generator
 └── benchmarks
```

This ensures:
- Scalability
- Maintainability
- Parallel execution

---

## 🗂️ Database Design (ER Overview)

```
User ──┬── Project ──┬── GeneratedOutputs
       │             └── Citations
       └── Roles
```

- Secure JWT-based authentication
- Hashed passwords
- Role-based access (Student / Researcher / Reviewer / Faculty)

---

## 🔄 Data Flow

```
User Input (Text / PDF / Voice)
        ↓
Preprocessing & Cleaning
        ↓
Scholarly Retrieval APIs
        ↓
LLM Synthesis & Validation
        ↓
Database Storage
        ↓
LaTeX / Text / Audio Output
```

---

## 🧪 Non-Functional Properties

- ⚡ Asynchronous processing
- 🔐 Secure API key handling via `.env`
- 📦 Portable (Local / Cloud / Docker-ready)
- 📈 Horizontally scalable
- ♻️ Easily extensible modules

---

## ⚖️ Ethical & Legal Compliance

- Uses **open-access research only**
- No training on user data
- Verifiable citations
- Responsible AI usage

---

## 🛠️ Installation (Local)

```bash
git clone https://github.com/your-username/smart-research-assistant.git
cd smart-research-assistant

pip install -r requirements.txt

# Set environment variables
cp .env.example .env

uvicorn main:app --reload
```

---

## 📌 Future Enhancements

- Dockerized deployment
- PDF citation highlighting
- Collaborative research spaces
- Offline LLM support
- Plagiarism similarity checks

---

## 👥 Team

**Research Minds**
- Ayan Chattopadhyay
- Arkapravo Mandal
- Atreyee Das
- Deboparna Das

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and feel free to fork or contribute!

