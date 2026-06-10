# Document Intelligence System

A production-grade AI system built on Google Cloud Platform.

## What it does
- Upload any PDF document.
- Ask questions about it in plain English (typing or voice).
- Get precise answers powered by Gemini AI.

## Tech Stack
- Cloud Storage — PDF storage.
- Pub/Sub — Automatic notifications.
- Cloud Run — Serverless Python backend.
- Document AI — OCR text extraction.
- ChromaDB — Vector database.
- Sentence Transformers — Text embeddings.
- Gemini 2.5 Flash — AI question answering.
- Speech to Text — Voice input (coming soon).
- Text to Speech — Voice output (coming soon).
- Cloud Build — CI/CD automation.

## Architecture
PDF Upload → Cloud Storage → Pub/Sub → Cloud Run → Document AI → ChromaDB → Gemini → Answer

## Setup
1. Clone the repository.
2. Create GCP project.
3. Enable required APIs.
4. Deploy to Cloud Run.
