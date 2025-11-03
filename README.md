# Chat-with-CSV

An AI-powered Retrieval-Augmented Generation (RAG) agent that lets you query any CSV file in natural language. Built with FastAPI, Streamlit, LangChain, Mistral embeddings, Pinecone vector store, and deployed on Render.

## Live Demo

> Because Render’s free tier sleeps inactive services, please start the backend first:
> **Backend (starts slowly on cold start):**
> [https://csv-rag-agent.onrender.com](https://csv-rag-agent.onrender.com)
>
> Then open the main UI:
> **Streamlit Frontend:**
> [https://chat-with-csv-vwig.onrender.com/](https://chat-with-csv-vwig.onrender.com/)

---


## Table of Contents

- [Features](#features)  
- [Architecture](#architecture)  
- [Tech Stack](#tech-stack)  
---

## Features

- **Two-step flow**: Upload your own CSV or use the sample dataset, then index it on Pinecone with a single click.  
- **Natural-language queries**: Ask any question about your data and get immediate, contextual answers.  
- **Fresh indexing**: Each new upload recreates the vector index so you always query only the current dataset.  
- **Data preview**: View a snippet of your CSV before indexing to confirm you’re working with the right file.  
- **Lightweight UI**: Interactive Streamlit frontend with sidebar navigation and chat-style query interface.

---

## Architecture

1. **Data Ingestion & Preprocessing**  
   - CSV is cleaned (whitespace trimming, type coercion, missing-value imputation) via Pandas before indexing.  
2. **Embedding & Vector Store**  
   - Uses MistralAIEmbeddings to generate semantic vectors.  
   - Stores vectors in Pinecone; index is dropped and recreated on each ingestion to avoid stale data.  
3. **Retrieval-QA Chain**  
   - LangChain’s `RetrievalQA` combines a Pinecone retriever with the Mistral LLM for answer generation.  
4. **API Layer**  
   - FastAPI exposes two endpoints: `/index` (for ingestion) and `/query` (for Q&A).  
5. **Frontend**  
   - Streamlit app orchestrates data loading and querying, providing a clean two-step user flow.  
6. **Deployment**  
   - Both back-end and front-end are containerized with Docker and deployed on Render.com.

---

## Tech Stack

| Layer              | Technology                          |
| ------------------ | ----------------------------------- |
| **Frameworks**     | FastAPI, Streamlit                  |
| **Orchestration**  | LangChain                           |
| **Embeddings**     | MistralAIEmbeddings (`mistral-embed`) |
| **LLM**            | ChatMistralAI                       |
| **Vector Store**   | Pinecone (Serverless)               |
| **Containerization** | Docker                             |
| **Deployment**     | Render.com                          |

---


