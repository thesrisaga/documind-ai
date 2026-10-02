# DocuMind AI

## RAG-Based Intelligent Document Question Answering System

DocuMind AI is an intelligent document question-answering system built using Retrieval-Augmented Generation (RAG).

The system allows users to upload PDF documents and ask natural-language questions about their contents. Instead of sending the entire document directly to an LLM, DocuMind AI retrieves the most relevant passages using semantic search and provides them as context to the language model.

This helps produce answers that are grounded in the uploaded document and provides source page references for transparency.

---

## Project Overview

DocuMind AI follows a complete Retrieval-Augmented Generation pipeline:

**PDF → Text Extraction → Chunking → Embeddings → FAISS Retrieval → LLM Generation → Grounded Answer**

The system combines traditional document processing, semantic search, vector databases, and large language models into a single application.

---

## Key Features

- PDF document upload
- Automatic text extraction from PDF files
- Overlapping text chunking
- Semantic text embeddings
- FAISS vector similarity search
- Retrieval-Augmented Generation
- Groq LLM integration
- Context-grounded answers
- Source page references
- Multi-turn document conversation
- Retrieval evaluation
- Answer grounding evaluation
- Streamlit-based interface

---

## System Architecture

```text
                    ┌─────────────────┐
                    │   PDF Document  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Text Extraction │
                    │    PyMuPDF      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Chunking     │
                    │  800 characters │
                    │ 150 overlap     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Embeddings    │
                    │ MiniLM-L6-v2    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  FAISS Vector   │
                    │      Store      │
                    └────────┬────────┘
                             │
                 User Question
                             │
                             ▼
                    ┌─────────────────┐
                    │    Retriever    │
                    │ Top-K Chunks    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Groq LLM      │
                    │ Answer Generation│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Grounded Answer │
                    │ + Source Pages  │
                    └─────────────────┘


## Project Structure

```text
documind-ai/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   └── research_paper.pdf
│
├── src/
│   ├── ingestion/
│   │   └── pdf_loader.py
│   │
│   ├── preprocessing/
│   │   └── chunker.py
│   │
│   ├── embeddings/
│   │   └── embedding_model.py
│   │
│   ├── retrieval/
│   │   ├── vector_store.py
│   │   └── retriever.py
│   │
│   └── generation/
│       └── llm.py
│
├── tests/
│   ├── test_pdf.py
│   ├── test_chunker.py
│   ├── test_embeddings.py
│   ├── test_vector_store.py
│   ├── test_retriever.py
│   ├── test_rag.py
│   ├── test_evaluation.py
│   └── test_answer_evaluation.py
│
├── .gitignore
├── README.md
└── requirements.txt

## Main Components

- **PDF Ingestion** — Extracts text and page information from PDF documents.
- **Chunking** — Splits documents into overlapping text segments.
- **Embeddings** — Converts text chunks into numerical vector representations.
- **FAISS Retrieval** — Finds the most relevant document chunks for a user query.
- **LLM Generation** — Generates answers using retrieved document context.
- **Source Attribution** — Displays the document pages used to generate an answer.
- **Evaluation** — Tests retrieval quality and whether generated answers contain expected concepts.
- **Streamlit UI** — Provides an interactive interface for uploading documents and asking questions.

## Application Preview

<img width="951" height="440" alt="documind-home" src="https://github.com/user-attachments/assets/217a1429-1b42-42bc-9967-8e8e5380e03b" />
