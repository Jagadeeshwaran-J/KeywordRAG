import os

from chunker import Chunker
from keyword_search import KeywordSearcher
from llm_client import LLMClient
from pdf_loader import PDFLoader
from rag import RAG

PDF_PATH = r"/DATA/document.pdf"
OUTPUT_DIR = "output"
TEXT_FILE = "output/extracted_text.txt"
CHUNKS_FILE = "output/chunks.txt"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # PDF Loader
    pdf_loader = PDFLoader(PDF_PATH)
    print("\nReading PDF...")
    text = pdf_loader.extract_text()
    print("PDF text extracted.")
    pdf_loader.save_text(text, TEXT_FILE)

    # Chunker
    chunker = Chunker(chunk_size=500, overlap=100)

    print("\nCreating chunks...")
    chunks = chunker.create_chunks(text)
    print(f"Created {len(chunks)} chunks.")

    chunker.save_chunks(chunks, CHUNKS_FILE)

    # BM25
    print("\nCreating BM25 index...")
    searcher = KeywordSearcher(chunks)
    print("BM25 ready!")

    # LLM
    llm = LLMClient(
        base_url="http://localhost:1234/v1",
        model="LLM",
        api_key="EMPTY"
    )

    # RAG
    rag = RAG(searcher, llm)

    # Chat
    print("\n" + "=" * 70)
    print("KeywordRAG Chatbot")
    print("Type 'exit' to stop.")
    print("=" * 70)

    while True:
        query = input("\nYou: ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        if not query:
            continue

        print("\nSearching...")

        try:
            answer = rag.ask(query)

            print("\n" + "=" * 70)
            print("ANSWER")
            print("=" * 70)
            print(answer)

        except Exception as e:
            print("\nError:", e)


if __name__ == "__main__":
    main()