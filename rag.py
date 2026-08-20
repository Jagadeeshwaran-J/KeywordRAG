class RAG:
    def __init__(self, searcher, llm):
        self.searcher = searcher
        self.llm = llm

    def create_prompt(self, query, results):
        context = ""

        for result in results:
            context += f"\n[CHUNK {result['id']}]\n"
            context += result["text"] + "\n"

        return f"""
You are a document question-answering assistant.

Answer the question using ONLY the document context below.

Rules:
1. Use only the provided context.
2. Do not use outside knowledge.
3. Do not make up information.
4. If the answer is not in the document, say:
"I could not find the answer in the document."

DOCUMENT CONTEXT:
-----------------
{context}
-----------------

USER QUESTION:
{query}

ANSWER:
"""

    def ask(self, query):
        results = self.searcher.search(query, top_k=5)

        self.searcher.display_results(query, results)

        prompt = self.create_prompt(query, results)

        print("\n" + "=" * 70)
        print("PROMPT SENT TO LLM")
        print("=" * 70)
        print(prompt)

        return self.llm.generate(prompt)