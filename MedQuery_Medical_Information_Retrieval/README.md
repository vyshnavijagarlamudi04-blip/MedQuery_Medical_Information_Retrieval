# MedQuery – Medical Information Retrieval System

> **Subtitle:** *Hybrid Medical Document Retrieval and Semantic Ranking using BM25 and BERT*  
> **Course / Degree:** B.Tech Mini Project in Information Retrieval (IR)  
> **Architecture:** Lexical (BM25 / TF-IDF) + Dense Neural Semantic (Sentence-BERT `all-MiniLM-L6-v2`) + Linear Score Fusion & Re-ranking

---

## 1. Problem Statement

General search engines and large language model chatbots often struggle with clinical precision, hallucination, and lack of verifiable provenance when handling complex medical queries. Keyword-only retrieval systems (such as TF-IDF or standard BM25) frequently suffer from **vocabulary mismatch**—where user query terms (e.g., *"high blood pressure"*, *"sugar sickness"*) differ from clinical expressions (e.g., *"essential hypertension"*, *"type 2 diabetes mellitus"*). Conversely, purely dense semantic retrieval models can fail to capture exact medical acronyms, specific pathogen species (e.g., *Plasmodium falciparum*, *Streptococcus pneumoniae*), or specific pharmaceutical compounds (e.g., *Metformin*, *SGLT2 inhibitors*).

---

## 2. Objective

**MedQuery** is an end-to-end, domain-specific Medical Information Retrieval System that addresses vocabulary mismatch and lexical specificity by synthesizing **probabilistic keyword retrieval (BM25)** and **dense contextual transformer embeddings (Sentence-BERT)** into a unified **hybrid re-ranking pipeline**.

> **Important Scope Clarification:**  
> MedQuery is an **Information Retrieval (IR)** system designed to surface and rank relevant medical literature and educational passages. It is **NOT** a medical diagnostic system, clinical decision support software, or an autonomous triage bot.

---

## 3. Key Features

- **Domain-Specific Text Preprocessing & Cleaning:**
  - Preserves clinical terminology, hyphenated terms (e.g., *Type-2*, *COVID-19*, *Anti-TNF*), acronyms (*H1N1*, *B12*, *HbA1c*), and negations.
  - Safe stopword removal preventing erasure of critical descriptors like *acute*, *chronic*, *without*, *no*, *type*.
- **Passage-Level Document Chunking:**
  - Divides comprehensive medical literature into 3 distinct functional semantic passages:
    1. *Overview & Pathophysiology*
    2. *Clinical Symptoms & Etiology*
    3. *Treatment, Therapeutics & Prevention*
- **Dual-Channel Retrieval Algorithms:**
  - **TF-IDF Baseline:** Vector Space Model with sublinear term-frequency scaling and cosine similarity.
  - **BM25 Okapi:** Probabilistic term-matching with document length normalization ($k_1 = 1.5, b = 0.75$).
  - **Sentence-BERT Semantic Retrieval:** 384-dimensional dense embeddings (`all-MiniLM-L6-v2`) capturing deep conceptual semantic intent.
  - **Hybrid Fusion & Re-ranking:** Normalizes lexical BM25 and dense cosine scores, combining them via configurable linear weights ($\alpha \in [0, 1]$) to re-rank candidate pools into the final Top-$K$.
- **Empirical IR Evaluation Suite:**
  - Standard TREC / Manning IR benchmark on 35 manually validated ground-truth medical queries.
  - Computes **Precision@K**, **Recall@K**, **F1@K**, **Mean Average Precision (MAP)**, **Mean Reciprocal Rank (MRR)**, and **NDCG@K**.
  - Generates automated comparative performance tables and publication-grade bar charts (`results/evaluation_comparison.png`).
- **Interactive Multi-Method Comparison:**
  - Run identical queries simultaneously across TF-IDF, BM25, Semantic, and Hybrid to observe ranking variances in real time.
- **Dynamic Document Ingestion:**
  - Upload external **TXT**, **PDF**, or **CSV** clinical files with automated text extraction, chunking, and live incremental embedding updates.
- **Query History & Sub-Second Latency Logging:**
  - Tracks query timestamps, retrieval engine chosen, top results, and search execution time in milliseconds.

---

## 4. System Architecture

```
                       ┌─────────────────────────────────────┐
                       │   Curated Medical Dataset (105)     │
                       └──────────────────┬──────────────────┘
                                          │
                                          ▼
                       ┌─────────────────────────────────────┐
                       │  Text Cleaning & Normalization      │
                       └──────────────────┬──────────────────┘
                                          │
                                          ▼
                       ┌─────────────────────────────────────┐
                       │   Document Chunking (315 Passages)  │
                       └──────────┬───────────────────────┬──┘
                                  │                       │
                                  ▼                       ▼
            ┌───────────────────────────┐   ┌───────────────────────────┐
            │   BM25 / TF-IDF Index     │   │  SBERT Dense Embeddings   │
            │   (Inverted Vocabulary)   │   │  (all-MiniLM-L6-v2, 384D) │
            └─────────────┬─────────────┘   └─────────────┬─────────────┘
                          │                               │
                          └───────────────┬───────────────┘
                                          │
                                          ▼
                               ┌─────────────────────┐
                               │     User Query      │
                               └──────────┬──────────┘
                                          │
                                          ▼
              ┌───────────────────────────┴───────────────────────────┐
              │                                                       │
              ▼                                                       ▼
  ┌───────────────────────┐                               ┌───────────────────────┐
  │   BM25 Retrieval      │                               │   Semantic Retrieval  │
  │   (Score: BM25Okapi)  │                               │   (Cosine Similarity) │
  └───────────┬───────────┘                               └───────────┬───────────┘
              │                                                       │
              └───────────────────────────┬───────────────────────────┘
                                          │
                                          ▼
                       ┌─────────────────────────────────────┐
                       │  Min-Max Score Normalization        │
                       └──────────────────┬──────────────────┘
                                          │
                                          ▼
                       ┌─────────────────────────────────────┐
                       │  Linear Fusion & Candidate Re-Rank  │
                       │  Score = α·NormBM25 + (1-α)·Cosine   │
                       └──────────────────┬──────────────────┘
                                          │
                                          ▼
                       ┌─────────────────────────────────────┐
                       │         Top-K Ranked Results        │
                       │         (Sub-Second Latency)        │
                       └──────────────────┬──────────────────┘
                                          │
                                          ▼
                       ┌─────────────────────────────────────┐
                       │      IR Evaluation Benchmark        │
                       │     (P@K, R@K, F1, MAP, MRR, NDCG)  │
                       └─────────────────────────────────────┘
```

---

## 5. Technology Stack

### Backend & Information Retrieval
- **Python 3.10+**
- **FastAPI:** High-performance asynchronous REST API framework
- **Uvicorn:** ASGI web server
- **Sentence-Transformers:** Neural embeddings via `all-MiniLM-L6-v2`
- **PyTorch:** Tensor operations and GPU/CPU inference
- **rank-bm25:** Probabilistic BM25Okapi implementation
- **scikit-learn:** TF-IDF vectorizer and cosine similarity calculation
- **NLTK:** Sentence tokenizer and text normalization
- **pypdf:** Secure PDF text extraction
- **pandas & numpy:** Corpus manipulation and matrix algebra
- **matplotlib:** Benchmark chart visualization

### Frontend
- **React 19 & Vite 8:** Modern, lightning-fast UI bundling
- **Tailwind CSS v4:** Healthcare-tailored responsive design system
- **Lucide React:** Medical, search, and data visualization icons

---

## 6. Dataset Description

The curated local dataset resides in `data/medical_documents.csv` and contains **105 structured educational medical documents** sourced from verified public health resources (NIH MedlinePlus, WHO Guidelines, CDC, and NHS).

### Schema:
| Column | Description |
|---|---|
| `document_id` | Unique primary key (e.g., `DOC_001`, `DOC_002`) |
| `title` | Formal clinical condition overview title |
| `category` | Medical specialty (Cardiovascular, Endocrinology, Respiratory, etc.) |
| `disease` | Primary pathology or condition |
| `symptoms` | Characteristic clinical signs and manifestations |
| `causes` | Etiology, pathophysiology, and risk factors |
| `treatment` | First-line therapeutics, pharmaceuticals, and surgical options |
| `prevention` | Lifestyle modifications, immunizations, and risk reduction |
| `content` | Comprehensive educational discussion |
| `source` | Medical citation authority (e.g., WHO Guidelines, CDC, Mayo Clinic) |

### Covered Pathologies (Sample):
- **Endocrinology:** Type 1 & Type 2 Diabetes, Gestational Diabetes, DKA, Hypoglycemia, Hashimoto's, Graves' Disease, Cushing's, Obesity.
- **Cardiovascular:** Essential Hypertension, Secondary Hypertension, Hypertensive Crisis, Coronary Artery Disease, Congestive Heart Failure, Atrial Fibrillation, Infective Endocarditis, Aortic Stenosis, DVT.
- **Respiratory:** Asthma, Exercise-Induced Bronchospasm, Community-Acquired Pneumonia, Aspiration Pneumonia, COPD, Pulmonary Embolism, Sleep Apnea, Pulmonary Fibrosis.
- **Infectious Diseases:** Common Cold, Seasonal Influenza, Dengue Fever, Severe Dengue/DSS, Malaria, Cerebral Malaria, Tuberculosis, MDR-TB, COVID-19, Long COVID, Bacterial Meningitis, Rabies, Tetanus, Lyme Disease, Sepsis.
- **Gastroenterology:** Acute/Chronic Gastritis, Peptic Ulcers, GERD, Food Poisoning, Botulism, Celiac Disease, Crohn's Disease, Ulcerative Colitis, IBS, Acute Pancreatitis, Cholecystitis.
- **Nephrology & Hepatology:** Chronic Kidney Disease, Acute Kidney Injury, Kidney Stones, Nephrotic Syndrome, MASLD/NAFLD, Cirrhosis, Hepatitis B, Hepatitis C.

---

## 7. Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Node.js v18+ and npm

### Step 1: Clone or Navigate to the Workspace
Open Windows PowerShell:
```powershell
cd c:\Users\bathu\Desktop\MedQuery_Medical_Information_Retrieval
```

### Step 2: Set Up Python Virtual Environment (Recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 3: Install Frontend Dependencies
```powershell
cd frontend
npm install
cd ..
```

---

## 8. Index Building

To process the dataset, generate chunks, fit BM25/TF-IDF models, and compute SBERT dense embeddings:
```powershell
python scripts/build_index.py
```
*Note: Embeddings are persistently cached in `indexes/sbert_embeddings.npy` and load in milliseconds on subsequent runs.*

---

## 9. Running the Application

### Option A: Complete Web App via FastAPI (Single Command)
The built React UI is integrated directly into the FastAPI server. Run:
```powershell
uvicorn backend.main:app --reload --port 8000
```
- **Web Dashboard:** [http://127.0.0.1:8000/app](http://127.0.0.1:8000/app) or [http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard)
- **Interactive Swagger API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **API Root:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Option B: Separate Development Servers (FastAPI + Vite)
In Terminal 1 (Backend):
```powershell
uvicorn backend.main:app --reload --port 8000
```

In Terminal 2 (Frontend):
```powershell
cd frontend
npm run dev
```
Access the Vite dev server at: [http://localhost:5173](http://localhost:5173)

---

## 10. Information Retrieval Evaluation

Run the formal IR benchmark against the 35 ground-truth evaluation queries:
```powershell
python scripts/evaluate.py
```

### Empirical Results Summary:
| Retrieval Method | Precision@5 | Recall@5 | F1@5 | Precision@10 | Recall@10 | F1@10 | MAP | MRR | NDCG@5 |
|---|---|---|---|---|---|---|---|---|---|
| **TF-IDF Baseline** | 0.3029 | 0.8905 | 0.4425 | 0.1657 | 0.9571 | 0.2788 | 0.8837 | 0.9857 | 0.9008 |
| **BM25 Okapi** | 0.3143 | 0.9238 | 0.4599 | 0.1657 | 0.9571 | 0.2788 | 0.8660 | 0.9714 | 0.9015 |
| **SBERT Semantic** | **0.3429** | **0.9857** | **0.4986** | **0.1714** | **0.9857** | **0.2883** | **0.9463** | **0.9857** | **0.9671** |
| **Hybrid (BM25+BERT)** | 0.3314 | 0.9571 | 0.4823 | 0.1686 | 0.9714 | 0.2835 | 0.9184 | **0.9857** | 0.9433 |

*Output visualization chart saved to:* `results/evaluation_comparison.png`.

---

## 11. Automated Testing

Execute the comprehensive 32-test unit and integration test suite:
```powershell
pytest tests/ -v
```

### Test Coverage Includes:
1. Empty query handling (graceful fallback)
2. Very short query resolution (e.g., *"flu"*)
3. Extended multi-sentence clinical queries
4. Unknown medical terminology
5. Queries with phonetic/spelling variations
6. Disease name queries
7. Symptom-based queries
8. Therapeutics and treatment queries
9. Preventive healthcare queries
10. Category filtering
11. Dynamic PDF parsing and ingestion
12. Duplicate document deduplication
13. Invalid file extension rejection
14. Non-matching query boundaries
15. Top-K ranking variance
16. Hybrid fusion weight interpolation

---

## 12. Sample Demonstration Queries

Clickable directly from the Web Interface:
1. *"What are common symptoms of diabetes?"*
2. *"What causes hypertension?"*
3. *"What are common asthma triggers?"*
4. *"How can dengue be prevented?"*
5. *"What are symptoms of anemia?"*
6. *"What causes migraine?"*
7. *"What are the symptoms of pneumonia?"*
8. *"How is food poisoning prevented?"*

---

## 13. Limitations & Future Enhancements

### Current Limitations:
- The SBERT model (`all-MiniLM-L6-v2`) is a general-domain sentence transformer; while highly performant, it is not fine-tuned on PubMed specifically.
- The document collection is currently capped at 105 core conditions.

### Future Enhancements:
- **BioBERT / PubMedBERT:** Integrating specialized biomedical weights (e.g., `pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb`).
- **Dense Passage Retrieval (DPR) with FAISS:** Scaling to multi-million document PubMed abstracts with GPU-accelerated nearest-neighbor search.
- **Cross-Encoder Re-Ranking:** Incorporating a heavy cross-encoder (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) as a second-stage re-ranker.

---

## 14. Medical Safety Disclaimer

> **DISCLAIMER:**  
> **MedQuery** is an educational and academic information retrieval prototype developed for B.Tech Information Retrieval course demonstration. It searches and ranks documents from its curated collection. It does **not** generate clinical medical diagnoses, offer medical advice, or formulate patient-specific treatment regimens. Consult a licensed healthcare provider for clinical medical inquiries.
