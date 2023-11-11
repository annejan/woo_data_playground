"""
Grid Line Detector

This module, 'grid_line_detector', is designed to detect grid lines in images, identifying both
vertical and horizontal lines that may represent boundaries in tabular data. It is especially
useful for images derived from PDF files or similar documents.

Functions:
    estimate_line_likelihood(processed_image, axis='x'): Estimates the likelihood of each coordinate
                                                         being a grid line in a given image along the
                                                         specified axis ('x' for vertical, 'y' for horizontal).

    refine_lines(lines, min_distance=10): Refines detected lines by merging those that are within
                                          a specified minimum distance of each other.

    find_grid_lines_on_image(image, cutoff_fraction=0.6): Detects and refines grid line positions
                                                          in both vertical and horizontal directions
                                                          based on a specified likelihood cutoff.

Usage example:
    image = [Your Image Data]
    vertical_lines, horizontal_lines = find_grid_lines_on_image(image)
"""
import cv2
import numpy as np


def estimate_line_likelihood(processed_image, axis="x"):
    """
    Estimate the likelihood of each coordinate being a grid line along a given axis.
    """
    axis_index = 1 if axis == "x" else 0
    length = processed_image.shape[axis_index]
    line_likelihood = np.zeros(length)

    for i in range(length):
        line_pixels = processed_image[:, i] if axis == "x" else processed_image[i, :]
        line_likelihood[i] = (
            np.sum(line_pixels != 0) / processed_image.shape[1 - axis_index]
        )

    if np.max(line_likelihood) != 0:
        line_likelihood /= np.max(line_likelihood)

    return line_likelihood


def refine_lines(lines, min_distance=10):
    """
    Refine detected lines by merging those within a minimum distance of each other.
    """
    refined = []
    current_group = []

    for line in sorted(lines):
        if not current_group or line - current_group[-1] > min_distance:
            if current_group:
                refined.append(int(np.mean(current_group)))
            current_group = [line]
        else:
            current_group.append(line)

    if current_group:
        refined.append(int(np.mean(current_group)))

    return refined


def find_grid_lines_on_image(
    image, cutoff_fraction=0.6, min_distance=10, max_columns=None, max_rows=None
):
    """
    Detects and refines grid line positions in both vertical and horizontal directions
    based on a specified maximum number of columns (max_columns) and rows (max_rows) to keep.
    """
    image_array = np.array(image)
    edges = cv2.Canny(image_array, 50, 150)

    vertical_line_likelihood = estimate_line_likelihood(edges, axis="x")
    horizontal_line_likelihood = estimate_line_likelihood(edges, axis="y")

    vertical_cutoff = np.max(vertical_line_likelihood) * cutoff_fraction
    horizontal_cutoff = np.max(horizontal_line_likelihood) * cutoff_fraction

    # Select lines based on likelihood scores and apply the likelihood cutoff
    vertical_lines = [
        x
        for x, likelihood in enumerate(vertical_line_likelihood)
        if likelihood >= vertical_cutoff
    ]
    horizontal_lines = [
        y
        for y, likelihood in enumerate(horizontal_line_likelihood)
        if likelihood >= horizontal_cutoff
    ]

    # Sort the selected lines based on likelihood scores in descending order
    vertical_lines.sort(key=lambda x: vertical_line_likelihood[x], reverse=True)
    horizontal_lines.sort(key=lambda x: horizontal_line_likelihood[x], reverse=True)

    vertical_refined = refine_lines(
        [
            x
            for x, likelihood in enumerate(vertical_line_likelihood)
            if likelihood >= vertical_cutoff
        ],
        min_distance,
    )
    horizontal_refined = refine_lines(
        [
            y
            for y, likelihood in enumerate(horizontal_line_likelihood)
            if likelihood >= horizontal_cutoff
        ],
        min_distance,
    )

    # Take the top max_columns and max_rows lines if specified
    if max_columns is not None:
        vertical_lines = vertical_refined[:max_columns]
    if max_rows is not None:
        horizontal_lines = horizontal_refined[:max_rows]

    return vertical_lines, horizontal_lines
