import requests
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
import os

DB_PATH = os.getenv("DB_PATH", "chroma_db")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
PROMPT_PATH = os.getenv("PROMPT_PATH", "prompts/prompt_retriever.txt")

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

def load_prompt() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as file:
        return file.read()
    
def get_relevant_docs(question: str, k: int = 4):
    return vector_db.similarity_search(question, k=k)
    
def build_context(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)

def build_prompt(question: str, context: str) -> str:
    prompt_template = load_prompt()
    return (
        prompt_template
        .replace("{{CONTEXT}}", context)
        .replace("{{QUESTION}}", question)
    )

def ask_ollama(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0},
        },
        timeout=300,
    )

    response.raise_for_status()
    return response.json().get("response", "")
    
def print_sources(docs) -> None:
    print("\nSources:")
    for i, doc in enumerate(docs, start=1):
        print(f"{i}. {doc}")


def main() -> None:
    question = input("Question: ")

    docs = get_relevant_docs(question)
    context = build_context(docs)
    prompt = build_prompt(question, context)
    answer = ask_ollama(prompt)

    print("\nAnswer:")
    print(answer)

    print_sources(docs)


if __name__ == "__main__":
    main()