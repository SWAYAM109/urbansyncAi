from src.core.rag_engine import RAGEngine

def run_seed():
    print("Starting SOP Ingestion...")
    engine = RAGEngine()
    result = engine.ingest_sops()
    print(result)

if __name__ == "__main__":
    run_seed()