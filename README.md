🧠 Internal Document Q&A System – PoC

This project is a **Proof-of-Concept (PoC)** Question-Answering system that allows users to ask natural language questions and receive grounded answers extracted from a curated set of internal company documents.

---

## 🧩 Problem Interpretation

The client faces a major productivity issue: employees waste significant time manually searching through product specs, HR policies, and internal reports. The client wants to evaluate if modern AI can be used to **automatically answer internal questions based only on specific documents**, before scaling into a full solution.

---

## 💡 Proposed Solution & Rationale

We propose a document-based Q&A system built using **LangChain**, **Hybrid Retrieval (Keyword + Semantic)**, and **Azure OpenAI (GPT-4o)** for answer generation.

### Key Components

- **Document Loader**  
  Loads `.txt` files from a directory and splits them into chunks using LangChain's `RecursiveCharacterTextSplitter`.
- **Hybrid Retriever - Proposed Solution & Rationale**
I implemented a Hybrid Retrieval-Augmented Generation (RAG) system that combines sparse retrieval (BM25 keyword search) with dense retrieval (semantic search using HuggingFace embeddings + FAISS).
# Why Hybrid RAG?
Hybrid RAG leverages the strengths of both sparse and dense retrieval to build a more accurate and adaptable Q&A system:

| Retrieval Type | Strengths | Weaknesses |
|----------------|-----------|------------|
| **Keyword-based (BM25)** | Excellent for matching explicit terms, acronyms, and structured terminology. | Struggles with paraphrased queries and synonyms. |
| **Semantic (Dense)** | Captures the *meaning* behind questions and content (even if exact terms don't match). | May overlook precise keyword matches or domain-specific phrasing. |

By combining both, we create a robust system capable of:

- Retrieving content with high lexical precision (via BM25).

- Capturing semantic context and intent (via embeddings).

This approach ensures:

- Better recall and precision across varied document styles (e.g., formal policies vs. casual internal notes).

- Improved user satisfaction, especially when users phrase questions in natural language.

“Hybrid RAG combines both sparse and dense retrieval techniques to provide a broader and more adaptable retrieval capability. By leveraging both keyword-based and semantic retrieval, Hybrid RAG achieves a higher level of precision and versatility, making it well-suited for environments that require understanding both explicit terms and nuanced meanings.”

## 🛠 Setup Instructions

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```
### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3 Environment Variables
Create a .env file and add your Azure OpenAI credentials:

```bash
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=version
```

### 4 Prepare Documents 
Place your .txt files in folder, e.g.:
```
project/
|
├── documents/
|    ├── file1.txt
|    ├── file2.txt
```
### 5 Run the App
``` bash
streamlit run app.py
```
