# RAG Chatbot with Ollama and ChromaDB
This project is part of a series of small AI projects: AI Projects 3

A simple Retrieval-Augmented Generation (RAG) chatbot built with Python, Ollama, LangChain, and ChromaDB.


## Project Structure

```text
.
├── ask.py
├── ingest.py
├── docs/
│   └── fake_meeting_notes.txt
│   └── fake_meeting_notes2.txt
├── prompts/
│   └── prompt_retriever.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10+
- Ollama installed locally

### Ollama Models

Pull the required models or change the model in .env file:

```bash
ollama pull llama3.2:1b
ollama pull nomic-embed-text
```
