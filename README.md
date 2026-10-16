---
title: PaperQA
emoji: 📄
colorFrom: blue
colorTo: green
sdk: streamlit
app_file: app.py
pinned: false
---


# PaperQA - RAG System


A simple but complete RAG (Retrieval-Augmented Generation) system that answers questions from PDF documents.


## Features


* PDF text extraction (PyPDF2)
* Chunking & Embeddings (Sentence Transformers)
* Vector Search (FAISS)
* Local LLM (flan-t5-base) – no API key required!


## Tech Stack


* Streamlit (UI)
* PyPDF2 (PDF parsing)
* Sentence Transformers (embeddings) — **BAAI/bge-small-en-v1.5**
* FAISS (vector search)
* Transformers (LLM)


## Chunking Strategy


See `scripts/chunking_report.md` for the full comparison of chunk sizes (300, 500, 800) with overlap=2 sentences on the Attention Is All You Need paper.


**Default**: `chunk_size=500` with `overlap_sentences=2` was chosen as a reasonable balance between retrieval granularity and context preservation. The evaluation script measures retrieval similarity only; smaller chunks score higher due to less context dilution — this is a known bias in the metric, not evidence that smaller chunks give better final answers. No automatic "winner" was selected; 500 was kept as the default pending a human decision.


## Results


* Processed the Attention Is All You Need PDF (15 pages) → 128 chunks (at chunk_size=500)
* Tested Q&A pairs:
  - "What is the main contribution of the Attention Is All You Need paper?" → Correctly identified the transformer self-attention mechanism.
  - "How does multi-head attention work?" → Explained the projection matrices and scaled dot-product.
  - "What are the key innovations of the Transformer architecture?" → Listed attention, position-wise FFN, and layer normalization.


## Run Locally with Docker


```bash
docker build -t paperqa .
docker run -p 8501:8501 paperqa
```


Then open http://localhost:8501


## Deployment


**Primary live deployment**: Streamlit Community Cloud — https://project-5-paperapp-rag-system.streamlit.app/


**Docker**: Documented for local reproducibility only; not hosted publicly.


**Streamlit Community Cloud**: The app was first deployed on Hugging Face Spaces, then moved to Streamlit Community Cloud, where it is now live at https://project-5-paperapp-rag-system.streamlit.app/. It runs the lightweight `flan-t5-small` configuration to fit the free tier's ~1 GB memory limit.


The result is a lightweight, cost‑effective, and transparent RAG system that anyone can deploy for free.
