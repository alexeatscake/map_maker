"""Pytest configuration and fixtures for the map_maker tests."""

import tempfile
from pathlib import Path

import pytest
from PIL import Image


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def sample_png_file(temp_dir):
    """Create a small sample PNG file for testing."""
    # Create a simple 3x3 image with known colors
    img = Image.new("RGB", (3, 3))
    pixels = [
        (255, 0, 0),  # Red
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (255, 255, 255),  # White
        (128, 128, 128),  # Gray
        (0, 0, 0),  # Black
    ]
    img.putdata(pixels)

    png_path = temp_dir / "test_image.png"
    img.save(png_path)
    return png_path


@pytest.fixture
def expected_hex_grid():
    """Expected hex color grid for the sample PNG."""
    return [
        ["#FF0000", "#00FF00", "#0000FF"],
        ["#FFFF00", "#FF00FF", "#00FFFF"],
        ["#FFFFFF", "#808080", "#000000"],
    ]
