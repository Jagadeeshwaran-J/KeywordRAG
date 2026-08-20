class Chunker:
    def __init__(self, chunk_size=500, overlap=100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def create_chunks(self, text):
        words = text.split()
        chunks = []

        start = 0
        while start < len(words):
            end = start + self.chunk_size
            chunks.append(" ".join(words[start:end]))
            start += self.chunk_size - self.overlap

        return chunks

    def save_chunks(self, chunks, output_file):
        with open(output_file, "w", encoding="utf-8") as file:
            file.writelines(f"\n{'=' * 70}\n"
                    f"CHUNK {index}\n"
                    f"{'=' * 70}\n\n"
                    f"{chunk}\n" for index, chunk in enumerate(chunks))

        print(f"Chunks saved to: {output_file}")