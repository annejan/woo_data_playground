import argparse
import fitz  # PyMuPDF
from flair.data import Sentence
from flair.models import SequenceTagger

tagger = SequenceTagger.load("flair/ner-multi")


def read_pdf_line_by_line(pdf_file):
    doc = fitz.open(pdf_file)

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")

        for line in text.splitlines():
            yield line


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read a PDF file line by line and perform Named Entity Recognition (NER)."
    )
    parser.add_argument("pdf_file", help="Path to the PDF file to read.")
    args = parser.parse_args()

    for line in read_pdf_line_by_line(args.pdf_file):
        sentence = Sentence(line)
        tagger.predict(sentence)
        for entity in sentence.get_spans("ner"):
            print(entity)
