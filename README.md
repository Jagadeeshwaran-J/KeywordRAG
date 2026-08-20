# KeywordRAG

KeywordRAG is a PDF question-answering chatbot that uses keyword-based BM25
retrieval. It extracts text from a PDF, splits the text into overlapping
chunks, retrieves the most relevant chunks for each question, and sends those
chunks to an OpenAI-compatible LLM server.

## Requirements

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)
- An OpenAI-compatible LLM server

This project does not require an embedding model server, Qdrant, or Docker.

## Setup

Clone the project and open its folder:

```powershell
git clone https://github.com/Jagadeeshwaran-J/KeywordRAG.git
cd KeywordRAG
```

Create and activate a virtual environment, then install the dependencies:

```powershell
uv venv --python 312
.venv\Scripts\activate
uv sync
```

Put your PDF in the `DATA` folder. The default file is:

```text
DATA/Document.pdf
```

If your PDF has a different name or location, update `PDF_PATH` in
`main.py`.

The chatbot uses the following default LLM settings:

```text
Base URL: http://localhost:1234/v1
Model: Vishva007/Qwen3.5-9B-W4A16-AutoRound
API key: EMPTY
```

Update the `base_url`, `model`, and `api_key` values in `main.py` if your
LLM server uses different settings. The server must expose the OpenAI chat
completions API.

## Run

Start the chatbot:

```powershell
uv run main.py
```

Ask questions about your PDF:

```text
You: What is this document?
```

Type `exit` to stop the chatbot.

## Project structure

```text
KeywordRAG/
├── DATA/
│   └── Document.pdf              # PDF file used as the knowledge source
├── output/
│   ├── extracted_text.txt        # Extracted PDF text
│   └── chunks.txt                # Text chunks used for BM25 search
├── chunker.py                    # Splits extracted text into chunks
├── keyword_search.py             # BM25 keyword retrieval
├── llm_client.py                # OpenAI-compatible LLM client
├── main.py                       # Application entry point
├── pdf_loader.py                # Extracts text from PDF files
├── rag.py                        # Builds prompts and generates answers
├── pyproject.toml                # Project metadata and dependencies
├── requirements.txt              # Python dependency list
└── README.md                     # Project documentation
```

## Output files

When the chatbot starts, it creates the `output` folder and writes:

- `output/extracted_text.txt` - text extracted from the PDF
- `output/chunks.txt` - the overlapping text chunks used for BM25 search

For each question, the terminal displays the retrieved chunks, BM25 scores,
matched keywords, the prompt sent to the LLM, and the generated answer.

## How it works

1. `PDFLoader` extracts text from each PDF page.
2. `Chunker` creates 500-word chunks with 100 words of overlap.
3. `KeywordSearcher` builds a BM25 index and retrieves the top five chunks.
4. `RAG` adds the retrieved chunks to a document-grounded prompt.
5. `LLMClient` sends the prompt to the configured LLM server.
