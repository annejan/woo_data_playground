import argparse
import fitz  # PyMuPDF
from flair.data import Sentence
from flair.models import SequenceTagger
import torch

tagger = SequenceTagger.load("flair/ner-dutch-large")


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
    parser.add_argument("--cuda", action="store_true", help="Use CUDA for NER (if available).")
    args = parser.parse_args()

    if args.cuda:
        flair.device = torch.device('cuda')
    else:
        flair.device = torch.device('cpu')

    for line in read_pdf_line_by_line(args.pdf_file):
        sentence = Sentence(line)
        tagger.predict(sentence)
        for entity in sentence.get_spans("ner"):
            print(entity)
