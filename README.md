# 🛡️ TrustGate – AI Fact Verification & Citation System

An enterprise-grade AI-assisted Fact-Checking & Citation Engine designed to detect hallucinations in LLM-generated outputs using a hybrid Semantic + Numeric verification approach.

---

## 🚀 Overview

Large Language Models (LLMs) often generate responses that may contain factual inconsistencies or hallucinations.  

This system verifies LLM outputs against trusted source documents and provides:

- ✅ Claim-level verification  
- 📎 Source-backed citations  
- 🧠 Explanation reasoning  
- 📊 Trust score estimation  

The architecture is modular, explainable, and designed for enterprise AI compliance environments.

---

## 🧠 Core Architecture

LLM Output
↓
Claim Decomposition
↓
Hybrid Verification Engine
↓
Semantic Similarity (Embeddings)

Numeric Safeguard Layer
↓
Classification (Supported / Contradicted / Unverifiable)
↓
Trust Score Computation
↓
Streamlit Dashboard (UI)


---

## 🔬 Verification Methodology

### 1️⃣ Claim Extraction
The LLM output is decomposed into atomic factual claims.

### 2️⃣ Semantic Retrieval
Each claim is compared against document chunks using embedding-based cosine similarity.

### 3️⃣ Numeric Safeguard Layer
A deterministic numeric verification layer:
- Detects numeric contradictions
- Confirms numeric agreement
- Prevents silent hallucinated values

### 4️⃣ Hybrid Decision Logic

| Condition | Label |
|------------|--------|
| Numeric mismatch | ❌ Contradicted |
| Numeric agreement | ✅ Supported |
| High similarity (> 0.50) | ✅ Supported |
| Moderate similarity (0.35–0.50) | ⚠ Unverifiable |
| Low similarity | ⚠ Unverifiable |

### 5️⃣ Trust Score Calculation

Trust Score =
(Supported × 1.0 + Unverifiable × 0.4 + Contradicted × 0) / Total Claims



---

## 📊 Output Features

- Color-coded claim annotations  
- Expandable evidence snippets  
- Similarity scores  
- Reasoning explanations  
- Source page references  
- Overall Trust Score  

---

## 🏗️ Tech Stack

| Layer | Technology |
|--------|-------------|
| Backend API | FastAPI |
| Verification Engine | Python |
| Embeddings | Sentence Transformers |
| UI | Streamlit |
| Version Control | Git |

---

## 📂 Project Structure

api.py # FastAPI backend
dashboard.py # Streamlit UI
core/ # Chunking & claim extraction
models/ # Embedding model loader
utils/ # Numeric verification utilities
data/ # Sample test documents
requirements.txt
README.md


## 🎯 Example Use Case

Input LLM Output:

The patient is 45 years old.
The tumor size is 3 cm.
The patient has Stage III cancer.


## System Output:

Age → Supported

Tumor Size → Supported

Stage III → Unverifiable

Trust Score: 85%

## 🛡️ Enterprise Readiness

Modular architecture

Decoupled API and UI

Deterministic numeric safeguard

Explainable reasoning

Swagger documentation

Easily scalable with FAISS for large corpora

## 🔮 Future Improvements

FAISS-based large-scale retrieval

NLI-based contradiction detection

Multi-document knowledge base

PDF rendering with clickable citation anchors

Real-time streaming verification

## 👨‍💻 Author

AI Fact Verification System
Built for Enterprise AI Compliance & Hallucination Detection


