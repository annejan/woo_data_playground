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


def find_grid_lines_on_image(image, cutoff_fraction=0.6, min_distance=10):
    """
    Detects and refines grid line positions in both vertical and horizontal directions.
    """
    # gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(np.array(image), 50, 150)

    vertical_line_likelihood = estimate_line_likelihood(edges, axis="x")
    horizontal_line_likelihood = estimate_line_likelihood(edges, axis="y")

    vertical_cutoff = np.max(vertical_line_likelihood) * cutoff_fraction
    horizontal_cutoff = np.max(horizontal_line_likelihood) * cutoff_fraction

    vertical_lines = refine_lines(
        [
            x
            for x, likelihood in enumerate(vertical_line_likelihood)
            if likelihood >= vertical_cutoff
        ],
        min_distance,
    )
    horizontal_lines = refine_lines(
        [
            y
            for y, likelihood in enumerate(horizontal_line_likelihood)
            if likelihood >= horizontal_cutoff
        ],
        min_distance,
    )

    return vertical_lines, horizontal_lines
