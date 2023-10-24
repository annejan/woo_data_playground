import cv2
import re
import pytesseract
from pdf2image import convert_from_path
import numpy as np


def are_near(box1, box2, threshold):
    """
    Check if two bounding boxes are near each other based on a threshold.
    """
    x1, y1, w1, h1, _ = box1
    x2, y2, w2, h2, _ = box2

    # Check horizontal and vertical distances between boxes
    horizontal_dist = min(abs(x1 + w1 - x2), abs(x2 + w2 - x1))
    vertical_dist = min(abs(y1 + h1 - y2), abs(y2 + h2 - y1))

    return horizontal_dist <= threshold or vertical_dist <= threshold


def group_bounding_boxes(boxes):
    """
    Given a list of boxes, where each box is represented as a tuple (x, y, w, h),
    return a single bounding box that encompasses all of them.
    """
    min_x = min([box[0] for box in boxes])
    min_y = min([box[1] for box in boxes])
    max_x = max([box[0] + box[2] for box in boxes])
    max_y = max([box[1] + box[3] for box in boxes])

    return min_x, min_y, max_x - min_x, max_y - min_y


def group_nearby_boxes(boxes, threshold=10):
    """
    Group nearby bounding boxes and return grouped boxes.
    """
    grouped = []
    used = set()

    for i, box1 in enumerate(boxes):
        if i in used:
            continue
        current_group = [box1]
        for j, box2 in enumerate(boxes):
            if j != i and j not in used and are_near(box1, box2, threshold):
                current_group.append(box2)
                used.add(j)
        grouped_box = group_bounding_boxes(current_group)
        grouped.append(grouped_box)

    return grouped


def determine_position(x, y, w, h, img_width, img_height):
    mid_x, mid_y = x + w / 2, y + h / 2

    if mid_x <= img_width / 3:
        h_side = "left"
    elif mid_x <= 2 * img_width / 3:
        h_side = "center"
    else:
        h_side = "right"

    if mid_y <= img_height / 3:
        v_side = "top"
    elif mid_y <= 2 * img_height / 3:
        v_side = "middle"
    else:
        v_side = "bottom"

    return f"{v_side} {h_side}"


def find_id_on_pdf(pdf_path, minimum, maximum):
    images = convert_from_path(pdf_path)
    pattern = re.compile(r"\d+[A-Za-z]*")
    custom_config = r"--oem 3 --psm 6 -l nld -c tessedit_char_whitelist=' 0123456789abcdefghijklmnopqrstuvwxyz'"
    found_boxes = []
    for idx, img in enumerate(images):
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        img_height, img_width = img.shape[0], img.shape[1]

        boxes = pytesseract.image_to_data(
            img, output_type=pytesseract.Output.DICT, config=custom_config
        )

        for i in range(len(boxes["level"])):
            text = boxes["text"][i]
            if pattern.match(text):
                numeric_part = re.match(r"\d+", text)
                if minimum and int(numeric_part.group()) < minimum:
                    continue
                if maximum and int(numeric_part.group()) > maximum:
                    continue
                # Each box is defined by (x, y, w, h)
                x, y, w, h = (
                    boxes["left"][i],
                    boxes["top"][i],
                    boxes["width"][i],
                    boxes["height"][i],
                )

                position = determine_position(x, y, w, h, img_width, img_height)
                print(
                    f"ID '{boxes['text'][i]}' found on page {idx + 1} of PDF at position: {position} with "
                    f"bounding box: ({x}, {y}, {x + w}, {y + h})"
                )
                found_boxes.append({x, y, w, h, text})

    return found_boxes


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Find document ID on PDF pages.")
    parser.add_argument("pdf_path", help="Path to the PDF file.")
    parser.add_argument(
        "--minimum",
        "--min",
        type=int,
        required=False,
        help="Minimum expected documentID",
    )
    parser.add_argument(
        "--maximum",
        "--max",
        type=int,
        required=False,
        help="Maximum expected documentID",
    )

    args = parser.parse_args()
    found = find_id_on_pdf(args.pdf_path, args.minimum, args.maximum)
    grouped_boxes = group_nearby_boxes(found, threshold=100)
    print(grouped_boxes)
