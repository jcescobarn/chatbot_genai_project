from core.chroma_client import chroma_client
from core.loader import load_file
from core.splitter import split_text
from core.embedder import Embedder
from models.openai_client import openai_client
from uuid import uuid4
from datetime import datetime
from pathlib import Path
from typing import Optional


class RAGEngine:
    def __init__(self, k: int = 3):
        self.k = k  
        self.embedder = Embedder()

    def retrieve_context(self, query: str) -> str:
        results = chroma_client.query(query_text=query, n_results=self.k)
        documents = results.get("documents", [[]])[0]

        print("\n🔎 RAG Context:")
        for doc in documents:
            print(doc[:200], "...") 

        return "\n".join(documents) if documents else "No relevant documents found."


    def build_prompt(self, query: str, context: str) -> str:
        return f"Context:\n{context}\n\nQuestion:\n{query}"

    def answer(self, query: str) -> str:
        context = self.retrieve_context(query)
        prompt = self.build_prompt(query, context)
        return openai_client.generate(prompt)

    def ingest_document(self, file_path: str, source_name: Optional[str] = None) -> int:
        text = load_file(file_path)
        chunks = split_text(text)
        embeddings = self.embedder.embed(chunks)

        docs = [
            {
                "id": str(uuid4()),
                "document": chunk,
                "embedding": embedding,
                "metadata": {
                    "source": source_name or Path(file_path).name,
                    "ingested_at": datetime.utcnow().isoformat()
                }
            }
            for chunk, embedding in zip(chunks, embeddings)
        ]

        chroma_client.upsert(docs)
        return len(docs)


rag_engine = RAGEngine()
