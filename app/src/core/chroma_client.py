from chromadb import HttpClient
from chromadb.config import Settings
from typing import Dict, Any, List
from datetime import datetime

class ChromaClient:
    def __init__(self):
        self.host = "chromadb" 
        self.port = 8000
        self.tenant = "default_tenant"
        self.database = "default_database"
        self.settings = Settings(anonymized_telemetry=False)

        try:
            self.client = HttpClient(
                host=self.host,
                port=self.port,
                ssl=False,
                settings=self.settings,
                tenant=self.tenant,
                database=self.database,
            )

            self.collection = self.client.get_or_create_collection(name="documents")

        except Exception as e:
            raise RuntimeError(
                f"No se pudo conectar a ChromaDB con tenant '{self.tenant}' y database '{self.database}'. "
                f"Verifica que existan antes de iniciar la aplicación.\nDetalles: {str(e)}"
            )

    def upsert(self, docs: List[Dict[str, Any]]) -> None:
        for doc in docs:
            doc["metadata"]["ingested_at"] = datetime.utcnow().isoformat()

        self.collection.upsert(
            ids=[doc["id"] for doc in docs],
            documents=[doc["document"] for doc in docs],
            embeddings=[doc["embedding"] for doc in docs],
            metadatas=[doc["metadata"] for doc in docs],
        )

    def query(self, query_text: str, n_results: int = 3) -> Dict[str, Any]:
        return self.collection.query(query_texts=[query_text], n_results=n_results)

    def get_all_documents(self) -> Dict[str, Any]:
        return self.collection.get(include=["ids", "documents", "metadatas"])

    def list_collections_and_docs(self):
        for coll in self.client.list_collections():
            print(f"- {coll.name} ({coll.metadata})")
            docs = coll.get(include=["ids", "documents", "metadatas"])
            print(docs)

    def get_client(self) -> HttpClient:
        return self.client

chroma_client = ChromaClient()
