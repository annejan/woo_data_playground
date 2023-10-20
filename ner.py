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
    --verbose: (Optional) print some more info while working.

Example:
    python ner.py document.pdf --cuda --certainty 0.8 --output-excel entities.xlsx --output-csv entities.csv

SPDX-License-Identifier: EUPL-1.2
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


def process_entities(sentence, tagger, certainty, verbose):
    """
    Process named entities in a given sentence using the Flair tagger.

    :param sentence: flair.data.Sentence, the sentence object to process.
    :param tagger: flair.models.SequenceTagger, the Flair NER tagger model.
    :param certainty: float, the minimum score required to consider an entity.
    :return: dict, entities found in the sentence, with their count and tag.
    """
    entity_info = {}
    tagger.predict(sentence)
    for entity in sentence.get_spans("ner"):
        if verbose:
            print(entity)
        label = entity.get_labels()[0]
        if label.score >= certainty and label.value != "MISC":
            entity_text = entity.text
            entity_tag = label.value
            entity_info[entity_text] = entity_info.get(
                entity_text, {"tag": entity_tag, "count": 0}
            )
            entity_info[entity_text]["count"] += 1
    return entity_info


def get_entities_from_pdf(pdf_file, tagger, certainty, verbose):
    """
    Extract named entities from a given PDF file using the Flair tagger.

    :param pdf_file: str, path to the PDF file to process.
    :param tagger: flair.models.SequenceTagger, the Flair NER tagger model.
    :param certainty: float, optional, the minimum score required to consider an entity. Default is 0.9.
    :param verbose: hush hush ..
    :return: dict, entities found in the PDF, with their count and tag.
    """
    entities = {}
    with fitz.open(pdf_file) as doc:
        for page_num in range(len(doc)):
            if verbose:
                print(f"Page[{page_num}]")
            page = doc[page_num]
            entities_page = process_entities(
                Sentence(page.get_text("text")), tagger, certainty, verbose
            )
            for key, value in entities_page.items():
                if key in entities:
                    entities[key]["count"] += value["count"]
                else:
                    entities[key] = value
    return entities


def write_to_excel(sorted_entities, output_file):
    """
    Write extracted entities to an Excel file.

    :param sorted_entities: list, entities sorted by a criteria (e.g., count).
                            Each item is a tuple where the first item is the entity text and the
                            second item is a dictionary with entity details (e.g., tag and count).
    :param output_file: str, path to the output Excel file.
    """
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
    """
    Write extracted entities to a CSV file.

    :param sorted_entities: list, entities sorted by a criteria (e.g., count).
                            Each item is a tuple where the first item is the entity text and the
                            second item is a dictionary with entity details (e.g., tag and count).
    :param output_file: str, path to the output CSV file.
    """
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
        "-c",
        type=float,
        default=0.9,
        help="Minimum certainty for entities (default: 0.9).",
    )
    parser.add_argument(
        "--output-excel",
        "-x",
        required=False,
        help="Path to the output Excel file.",
    )
    parser.add_argument(
        "--output-csv",
        "-o",
        required=False,
        help="Path to the output CSV file.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Run the script in verbose mode printing more messages.",
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

    model = "flair/ner-dutch-large"
    if args.verbose:
        print(f"Loading {model}")
    tagger = SequenceTagger.load(model)
    entities = get_entities_from_pdf(args.pdf_file, tagger, args.certainty, args.verbose)
    sorted_entities = sorted(
        entities.items(), key=lambda x: x[1]["count"], reverse=True
    )

    if args.output_excel:
        write_to_excel(sorted_entities, args.output_excel)
        if args.verbose:
            print(f"Data has been written to {args.output_excel}")

    if args.output_csv:
        write_to_csv(sorted_entities, args.output_csv)
        if args.verbose:
            print(f"Data has been written to {args.output_csv}")


if __name__ == "__main__":
    main()
