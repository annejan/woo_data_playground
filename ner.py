import argparse
import fitz  # PyMuPDF
import flair
import torch
from flair.data import Sentence
from flair.models import SequenceTagger


def get_entities_with_certainty(pdf_file, certainty):
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


if __name__ == "__main__":
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
    args = parser.parse_args()
    if args.cuda:
        flair.device = torch.device("cuda")
    else:
        flair.device = torch.device("cpu")
    tagger = SequenceTagger.load("flair/ner-multi")
    entity_info = get_entities_with_certainty(args.pdf_file, args.certainty)
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
