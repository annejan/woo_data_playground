"""
Named Entity Recognition

This script reads a PDF file, performs Named Entity Recognition (NER) using Flair.
It extracts named entities, such as persons, organizations and locations, with a specified certainty level.
It can write the results to an Excel file, a CSV file, or just print them to the console.

Usage:
    python ner.py <pdf_file> [--cuda] [--certainty <certainty>] [--output-excel <output_excel>] [--output-csv <output_csv>]

Arguments:
    pdf/file: Path to the PDF file to read and analyze for named entities.
    --cuda: (Optional) Use CUDA for NER (if available).
    --certainty: (Optional) Minimum certainty for entities (default: 0.9).
    --output-excel: (Optional) Path to the output Excel file.
    --output-csv: (Optional) Path to the output CSV file.

Example:
    python ner.py document.pdf --cuda --certainty 0.8 --output-excel entities.xlsx --output-csv entities.csv
"""
import argparse
import csv
import os
import fitz  # PyMuPDF
import flair
import torch
from flair.data import Sentence
from flair.models import SequenceTagger
from openpyxl import Workbook


def get_entities_with_certainty(pdf_file, certainty, tagger):
    entity_info = {}
    doc = fitz.open(pdf_file)
    for page_num in range(len(doc)):
        page = doc[page_num]
        sentence = Sentence(page.get_text("text"))
        tagger.predict(sentence)
        for entity in sentence.get_spans("ner"):
            print(entity)
            label = entity.get_labels()[0]
            if label.score >= certainty and label.value != "MISC":
                entity_text = entity.text
                entity_tag = label.value
                if entity_text in entity_info:
                    entity_info[entity_text]["count"] += 1
                else:
                    entity_info[entity_text] = {"tag": entity_tag, "count": 1}
    return entity_info


def write_to_excel(sorted_entities, output_file):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Entities"
    sheet["A1"] = "Text"
    sheet["B1"] = "Tag"
    sheet["C1"] = "Count"
    for i, (entity_text, info) in enumerate(sorted_entities, start=2):
        sheet[f"A{i}"] = entity_text
        sheet[f"B{i}"] = info["tag"]
        sheet[f"C{i}"] = info["count"]
    workbook.save(output_file)


def write_to_csv(sorted_entities, output_file):
    with open(output_file, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Text", "Tag", "Count"])
        for entity_text, info in sorted_entities:
            writer.writerow([entity_text, info["tag"], info["count"]])


def main():
    parser = argparse.ArgumentParser(
        description="Read a PDF file and perform Named Entity Recognition (NER)."
    )
    parser.add_argument("pdf_file", help="Path to the PDF file to read.")
    parser.add_argument(
        "--cuda", action="store_true", help="Use CUDA for NER (if available)."
    )
    parser.add_argument(
        "--certainty",
        type=float,
        default=0.9,
        help="Minimum certainty for entities (default: 0.9).",
    )
    parser.add_argument(
        "--output-excel",
        required=False,
        help="Path to the output Excel file.",
    )
    parser.add_argument(
        "--output-csv",
        required=False,
        help="Path to the output CSV file.",
    )
    args = parser.parse_args()
    pdf_file_path = args.pdf_file
    if not os.path.isfile(pdf_file_path):
        print(f"Error: The specified PDF file '{pdf_file_path}' does not exist.")
        return

    if args.cuda:
        flair.device = torch.device("cuda")
    else:
        flair.device = torch.device("cpu")
    tagger = SequenceTagger.load("flair/ner-dutch-large")
    entity_info = get_entities_with_certainty(args.pdf_file, args.certainty, tagger)
    sorted_entities = sorted(
        entity_info.items(), key=lambda x: x[1]["count"], reverse=True
    )
    print(
        f"Entities with certainty >= {args.certainty} (Text, Tag, and Count per entity):"
    )
    for entity_text, info in sorted_entities:
        entity_tag = info["tag"]
        entity_count = info["count"]
        print(f"Text: {entity_text}, Tag: {entity_tag}, Count: {entity_count}")

    if args.output_excel:
        write_to_excel(sorted_entities, args.output_excel)
        print(f"Data has been written to {args.output_excel}")

    if args.output_csv:
        write_to_csv(sorted_entities, args.output_csv)
        print(f"Data has been written to {args.output_csv}")


if __name__ == "__main__":
    main()
