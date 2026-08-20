import re

from rank_bm25 import BM25Okapi


class KeywordSearcher:
    def __init__(self, chunks):
        self.chunks = chunks
        self.tokenized_chunks = [self.tokenize(chunk) for chunk in chunks] # This converts every chunk into words.
        self.bm25 = BM25Okapi(self.tokenized_chunks) # This creates your BM25 search index.

    def tokenize(self, text): # This converts every chunk into words in lowercase.
        return re.findall(r"\b[a-zA-Z0-9_-]+\b", text.lower())

    def search(self, query, top_k=5):
        query_words = self.tokenize(query)
        scores = self.bm25.get_scores(query_words)

        ranked_chunks = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )

        results = []

        for chunk_id in ranked_chunks[:top_k]:
            chunk = self.chunks[chunk_id]
            chunk_words = set(self.tokenize(chunk))

            matched_words = [
                word for word in query_words
                if word in chunk_words
            ]

            results.append({
                "id": chunk_id,
                "score": float(scores[chunk_id]),
                "text": chunk,
                "matched": matched_words
            })

        return results

    def display_results(self, query, results):
        print("\n" + "=" * 70)
        print("KEYWORD SEARCH")
        print("=" * 70)
        print("\nQuery:", query)
        print("\nQuery keywords:", self.tokenize(query))

        for rank, result in enumerate(results, start=1):
            print("\n" + "=" * 70)
            print(f"Rank: {rank}")
            print(f"Chunk ID: {result['id']}")
            print(f"BM25 Score: {result['score']:.4f}")
            print(f"Matched keywords: {result['matched']}")
            print("\nChunk:")
            print(result["text"])