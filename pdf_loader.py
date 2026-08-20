import pymupdf


class PDFLoader:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text(self):
        pdf = pymupdf.open(self.pdf_path)
        text = ""

        for page_number, page in enumerate(pdf, start=1):
            text += f"\n--- PAGE {page_number} ---\n"
            text += page.get_text()

        pdf.close()
        return text

    def save_text(self, text, output_file):
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(text)

        print(f"Text saved to: {output_file}")