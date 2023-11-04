"""
This script reads PDF or plain text files and performs Named Entity Recognition (NER) using the Flair library.
It extracts named entities such as persons, organizations, and locations, filtered by a specified certainty level.
Results can be output to Excel or CSV files, or printed to the console.

Usage:
    python ner.py <pdf_files> [--certainty <certainty>] [--output-excel <output_excel>] [--output-csv <output_csv>]

Args:
    pdf_files: Paths to the PDF files to read and analyze for named entities.
    --certainty: (Optional) Minimum certainty for entities to be considered (default: 0.9).
    --output-excel: (Optional) Path to output Excel file.
    --output-csv: (Optional) Path to output CSV file.
    --verbose: (Optional) Print additional info during processing.

Examples:
    python ner.py document.pdf --cuda --certainty 0.8 --output-excel entities.xlsx --output-csv entities.csv

SPDX-License-Identifier: EUPL-1.2
"""
import argparse
import csv
import os
import re
import string
from typing import Dict, List, Tuple, Union
import fitz  # PyMuPDF
import torch
from flair.data import Sentence
from flair.models import SequenceTagger
import openpyxl
from openpyxl import Workbook
from tqdm import tqdm


def process_file(
    file_path: str, tagger: SequenceTagger, certainty: float, verbose: bool
) -> Dict[str, Dict[str, Union[str, int]]]:
    """
    Processes a file to extract entities, handling PDF or plain text files.

    Args:
        file_path (str): The path to the file to be processed.
        tagger (SequenceTagger): The SequenceTagger instance for entity recognition.
        certainty (float): The threshold for entity recognition certainty.
        verbose (bool): Flag for verbose output during processing.

    Returns:
        dict: A dictionary of entities extracted from the file, categorized by type.

    Raises:
        ValueError: If the file extension is not supported.
    """
    if file_path.lower().endswith(".pdf"):
        return get_entities_from_pdf(file_path, tagger, certainty, verbose)
    elif file_path.lower().endswith(".txt"):
        with open(file_path, "r") as file:
            text = file.read()
        return get_entities_from_text(text, tagger, certainty, verbose)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")


def is_meaningful_content(s: str, threshold: float = 0.2) -> bool:
    """
    Checks if the provided string contains meaningful content based on a character threshold.

    Args:
        s (str): The input string to check.
        threshold (float): The proportion of meaningful characters required (default is 0.2).

    Returns:
        bool: True if the string is considered meaningful, False otherwise.
    """
    cleaned_string = re.sub(r"\s", "", s)
    meaningful_chars = sum(
        1
        for char in cleaned_string
        if char in string.ascii_letters + string.digits + string.punctuation
    )
    proportion_meaningful = (
        meaningful_chars / len(cleaned_string) if cleaned_string else 0
    )
    return proportion_meaningful >= threshold


def process_entities(
    sentence: Sentence, tagger: SequenceTagger, certainty: float, verbose: bool
) -> Dict[str, Dict[str, Union[str, int]]]:
    """
    Processes named entities in a sentence using the Flair tagger.

    Args:
        sentence (Sentence): The sentence object from Flair to process.
        tagger (SequenceTagger): The Flair NER tagger model to use.
        certainty (float): The minimum score required to consider an entity.
        verbose (bool): Whether to print additional information.

    Returns:
        dict: The entities found in the sentence, with their counts and tags.
    """
    entity_info = {}
    try:
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
    except (RuntimeError, ValueError) as e:
        print(f"Error in NER tagging: {e}\n{sentence}")


def get_entities_from_pdf(
    pdf_file: str, tagger: SequenceTagger, certainty: float, verbose: bool
) -> Dict[str, Dict[str, Union[str, int]]]:
    """
    Extracts named entities from a PDF file using the Flair tagger.

    Args:
        pdf_file (str): The path to the PDF file to process.
        tagger (SequenceTagger): The Flair NER tagger model to use.
        certainty (float): The minimum score required to consider an entity (default is 0.9).
        verbose (bool): Enables verbose output.

    Returns:
        dict: The entities found in the PDF, with their counts and tags.
    """
    entities = {}
    try:
        with fitz.open(pdf_file) as doc:
            for page_num in tqdm(
                range(len(doc)),
                desc="Processing pages",
                unit="pages",
                disable=verbose,
                position=1,
            ):
                if verbose:
                    print(f"Page[{page_num}]")
                page = doc[page_num]
                text = page.get_text("text")
                if not text.strip() or not is_meaningful_content(text):
                    continue
                entities_page = process_entities(
                    Sentence(text), tagger, certainty, verbose
                )
                if entities_page:
                    for key, value in entities_page.items():
                        if key in entities:
                            entities[key]["count"] += value["count"]
                        else:
                            entities[key] = value
    except (MemoryError, RuntimeError) as e:
        print(f"Error processing PDF {pdf_file} page {page_num}: {e}")
    return entities


def get_entities_from_text(
    text: str,
    tagger: SequenceTagger,
    certainty: float,
    verbose: bool,
    max_length: int = 1337,
) -> Dict[str, Dict[str, Union[str, int]]]:
    """
    Extracts named entities from text, splitting text into smaller segments if necessary.

    This function splits the input text into smaller parts if it exceeds `max_length`
    to ensure that the tagger processes manageable segments without losing word integrity.
    Each segment is processed separately to extract entities, taking care not to split
    words across segments.

    Args:
        text (str): Text to extract entities from.
        tagger (SequenceTagger): Flair NER tagger instance.
        certainty (float): Threshold for entity certainty.
        verbose (bool): Enables verbose output.
        max_length (int): Maximum segment length to process at once.

    Returns:
        dict: A dictionary where keys are entity types and values are dictionaries
        containing the entities and their positions in the original text.
    """
    if not text.strip() or not is_meaningful_content(text):
        return {}

    segments = []
    while text:
        if len(text) <= max_length:
            segments.append(text)
            break
        else:
            split_pos = text.rfind(" ", 0, max_length) + 1
            if (
                split_pos <= 0
            ):  # If no space is found, force split to avoid infinite loop
                split_pos = max_length
            segments.append(text[:split_pos])
            text = text[split_pos:]

    entities = {}
    offset = 0
    for segment in segments:
        segment_entities = process_entities(
            Sentence(segment), tagger, certainty, verbose
        )
        for entity_type, entity_info in segment_entities.items():
            for entity in entity_info:
                entity["start_pos"] += offset
                entity["end_pos"] += offset
            if entity_type in entities:
                entities[entity_type].extend(entity_info)
            else:
                entities[entity_type] = entity_info
        offset += len(segment)

    return entities


def write_to_excel(
    sorted_entities: List[Tuple[str, Dict[str, Union[str, int]]]], output_file: str
) -> None:
    """
    Writes extracted entities to an Excel file.

    Args:
        sorted_entities (list): Entities sorted by a criterion (e.g., count), each a tuple (entity_text, details).
        output_file (str): The path to the output Excel file.
    """
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Entities"
    sheet["A1"] = "Text"
    sheet["B1"] = "Tag"
    sheet["C1"] = "Count"
    try:
        for i, (entity_text, info) in enumerate(sorted_entities, start=2):
            sheet[f"A{i}"] = entity_text
            sheet[f"B{i}"] = info["tag"]
            sheet[f"C{i}"] = info["count"]
        workbook.save(output_file)
    except (PermissionError, openpyxl.utils.exceptions.IllegalCharacterError) as e:
        print(f"Error writing to Excel: {e}")


def write_to_csv(
    sorted_entities: List[Tuple[str, Dict[str, Union[str, int]]]], output_file: str
) -> None:
    """
    Writes extracted entities to a CSV file.

    Args:
        sorted_entities (list): Entities sorted by a criterion (e.g., count), each a tuple (entity_text, details).
        output_file (str): The path to the output CSV file.
    """
    try:
        with open(output_file, mode="w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Text", "Tag", "Count"])
            for entity_text, info in sorted_entities:
                writer.writerow([entity_text, info["tag"], info["count"]])
    except (PermissionError, csv.Error) as e:
        print(f"Error writing to CSV: {e}")


def main() -> None:
    """The main function that parses arguments and initiates the processing of files for NER"""
    parser = argparse.ArgumentParser(
        description="Read a PDF file and perform Named Entity Recognition (NER)."
    )
    parser.add_argument(
        "files", nargs="+", help="Paths to the PDF or TXT files to read."
    )
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
        action="store_true",
        help="Output Excel file(s).",
    )
    parser.add_argument(
        "--output-csv",
        "-o",
        action="store_true",
        help="Output CSV file(s).",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Run the script in verbose mode printing more messages.",
    )

    args = parser.parse_args()

    if not 0 <= args.certainty <= 1:
        print("Error: Certainty should be between 0 and 1.")
        return

    for file_path in args.files:
        if not os.path.isfile(file_path):
            print(f"Error: The specified file '{file_path}' does not exist.")
            return
        if not (
            file_path.lower().endswith(".pdf") or file_path.lower().endswith(".txt")
        ):
            print(f"Error: File '{file_path}' is not a valid PDF or TXT.")
            return

    if torch.cuda.is_available():
        if args.verbose:
            print("CUDA is available!")
        torch.device("cuda")
    else:
        if args.verbose:
            print("CUDA is not available. Using CPU...")
        torch.device("cpu")

    model = "flair/ner-dutch-large"
    try:
        if args.verbose:
            print(f"Loading {model}")
        tagger = SequenceTagger.load(model)
    except (FileNotFoundError, torch.serialization.pickle.UnpicklingError) as e:
        print(f"Error loading the NER model: {e}")
        return
    try:
        for file_path in tqdm(
            args.files,
            desc="Processing files",
            unit="file",
            disable=args.verbose,
            position=0,
        ):
            if args.verbose:
                print(f"Processing {file_path}")
            entities = process_file(file_path, tagger, args.certainty, args.verbose)
            sorted_entities = sorted(
                entities.items(), key=lambda x: x[1]["count"], reverse=True
            )

            # Create a unique output name based on the PDF file name
            if args.output_excel:
                output_excel = f"{os.path.splitext(file_path)[0]}.ner.xlsx"
                write_to_excel(sorted_entities, output_excel)
                if args.verbose:
                    print(f"Data for {file_path} has been written to {output_excel}")

            if args.output_csv:
                output_csv = f"{os.path.splitext(file_path)[0]}.ner.csv"
                write_to_csv(sorted_entities, output_csv)
                if args.verbose:
                    print(f"Data for {file_path} has been written to {output_csv}")

            if not args.output_csv and not args.output_excel:
                for entity in sorted_entities:
                    print(entity)
    except RuntimeError as e:
        print(f"Error processing PDF: {e}")


if __name__ == "__main__":
    main()
