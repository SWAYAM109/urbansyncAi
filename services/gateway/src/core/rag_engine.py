import os
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Configuration
SOP_PATH = "../../data/sops"
CHROMA_PATH = "../../data/chroma_db"  # Local folder to store the DB

class RAGEngine:
    def __init__(self):
        # Using a popular, lightweight local model (all-MiniLM-L6-v2)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.db = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embeddings)
        
    def ingest_sops(self):
        """Reads MD files, chunks them, and saves to Chroma DB."""
        if not os.path.exists(SOP_PATH):
            return f"Error: {SOP_PATH} does not exist."

        loader = DirectoryLoader(SOP_PATH, glob="*.md", loader_cls=UnstructuredMarkdownLoader)
        docs = loader.load()
        
        if not docs:
            return "No markdown files found to ingest."

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(docs)
        
        # Create and persist the database locally
        self.db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=CHROMA_PATH
        )
        return f"Successfully ingested {len(chunks)} chunks from {len(docs)} files into ChromaDB."

    def query_sop(self, query: str):
        """Searches for the most relevant SOP chunk."""
        search_results = self.db.similarity_search(query, k=2)
        return [res.page_content for res in search_results]

if __name__ == "__main__":
    rag = RAGEngine()
    print(rag.ingest_sops())
    print("\nTest Query Result:", rag.query_sop("What are the steps for a water leak?"))
