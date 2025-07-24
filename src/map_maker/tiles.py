"""Tile processing and conversion functions for the map maker."""

from pathlib import Path

import pandas as pd
from PIL import Image


def png_to_hex_grid(image_path: str | Path) -> list[list[str]]:
    """
    Convert a PNG image to a 2D grid of hex color values.

    Args:
        image_path: Path to the PNG image file

    Returns:
        2D list where each element is a hex color string (e.g., "#FF0000")

    Raises:
        FileNotFoundError: If the image file doesn't exist
        ValueError: If the image cannot be processed
    """
    image_file = Path(image_path)
    if not image_file.exists():
        msg = f"Image file not found: {image_path}"
        raise FileNotFoundError(msg)

    try:
        # Load the PNG file and convert to RGB
        img = Image.open(image_path).convert("RGB")

        # Get image dimensions
        width, height = img.size

        # Get pixel data as a flat list
        pixels = list(img.getdata())

        # Convert to 2D grid of hex values
        hex_grid = []
        for y in range(height):
            row = []
            for x in range(width):
                # Get RGB values for this pixel
                r, g, b = pixels[y * width + x]
                # Convert to hex color string
                hex_color = f"#{r:02X}{g:02X}{b:02X}"
                row.append(hex_color)
            hex_grid.append(row)

        return hex_grid

    except Exception as e:
        msg = f"Error processing image {image_path}: {e!s}"
        raise ValueError(msg) from e


def save_hex_grid_to_csv(hex_grid: list[list[str]], output_path: str | Path) -> None:
    """
    Save a hex color grid to a CSV file.

    Args:
        hex_grid: 2D list of hex color strings
        output_path: Path where the CSV file will be saved
    """
    # Create output directory if it doesn't exist
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Convert to DataFrame and save
    df = pd.DataFrame(hex_grid)
    df.to_csv(output_path, index=False, header=False)


def convert_png_to_hex_csv(image_path: str | Path, output_path: str | Path) -> None:
    """
    Convert a PNG image directly to a hex CSV file.

    This function combines png_to_hex_grid and save_hex_grid_to_csv for convenience.

    Args:
        image_path: Path to the input PNG image
        output_path: Path for the output CSV file
    """
    hex_grid = png_to_hex_grid(image_path)
    save_hex_grid_to_csv(hex_grid, output_path)
    input_name = Path(image_path).name
    output_name = Path(output_path).name
    print(f"Converted {input_name} to {output_name}")
