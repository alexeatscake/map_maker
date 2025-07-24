"""Tests for the tiles module."""

import pandas as pd
import pytest

from map_maker.tiles import (
    convert_png_to_hex_csv,
    png_to_hex_grid,
    save_hex_grid_to_csv,
)


class TestPngToHexGrid:
    """Test the png_to_hex_grid function."""

    def test_png_to_hex_grid_with_sample_image(
        self, sample_png_file, expected_hex_grid
    ):
        """Test conversion of a PNG to hex grid with known values."""
        result = png_to_hex_grid(sample_png_file)
        assert result == expected_hex_grid

    def test_png_to_hex_grid_with_path_object(self, sample_png_file, expected_hex_grid):
        """Test that function accepts Path objects."""
        result = png_to_hex_grid(sample_png_file)  # sample_png_file is already a Path
        assert result == expected_hex_grid

    def test_png_to_hex_grid_with_string_path(self, sample_png_file, expected_hex_grid):
        """Test that function accepts string paths."""
        result = png_to_hex_grid(str(sample_png_file))
        assert result == expected_hex_grid

    def test_png_to_hex_grid_file_not_found(self, temp_dir):
        """Test that FileNotFoundError is raised for non-existent files."""
        non_existent_file = temp_dir / "does_not_exist.png"
        with pytest.raises(FileNotFoundError, match="Image file not found"):
            png_to_hex_grid(non_existent_file)

    def test_png_to_hex_grid_invalid_file(self, temp_dir):
        """Test that ValueError is raised for invalid image files."""
        # Create a text file with .png extension
        invalid_file = temp_dir / "invalid.png"
        invalid_file.write_text("This is not an image")

        with pytest.raises(ValueError, match="Error processing image"):
            png_to_hex_grid(invalid_file)


class TestSaveHexGridToCsv:
    """Test the save_hex_grid_to_csv function."""

    def test_save_hex_grid_to_csv(self, temp_dir, expected_hex_grid):
        """Test saving hex grid to CSV file."""
        output_file = temp_dir / "test_output.csv"
        save_hex_grid_to_csv(expected_hex_grid, output_file)

        # Verify file was created
        assert output_file.exists()

        # Verify content
        df = pd.read_csv(output_file, header=None)
        saved_grid = df.values.tolist()
        assert saved_grid == expected_hex_grid

    def test_save_hex_grid_creates_directory(self, temp_dir, expected_hex_grid):
        """Test that function creates parent directories if they don't exist."""
        nested_dir = temp_dir / "subdir" / "nested"
        output_file = nested_dir / "test.csv"

        save_hex_grid_to_csv(expected_hex_grid, output_file)

        assert output_file.exists()
        assert nested_dir.exists()

    def test_save_hex_grid_with_string_path(self, temp_dir, expected_hex_grid):
        """Test that function accepts string paths."""
        output_file = temp_dir / "test_string.csv"
        save_hex_grid_to_csv(expected_hex_grid, str(output_file))

        assert output_file.exists()


class TestConvertPngToHexCsv:
    """Test the convert_png_to_hex_csv function."""

    def test_convert_png_to_hex_csv_integration(
        self, sample_png_file, temp_dir, expected_hex_grid
    ):
        """Test the complete conversion from PNG to CSV."""
        output_file = temp_dir / "converted.csv"

        convert_png_to_hex_csv(sample_png_file, output_file)

        # Verify file was created
        assert output_file.exists()

        # Verify content matches expected
        df = pd.read_csv(output_file, header=None)
        saved_grid = df.values.tolist()
        assert saved_grid == expected_hex_grid

    def test_convert_png_to_hex_csv_with_string_paths(
        self, sample_png_file, temp_dir, expected_hex_grid
    ):
        """Test conversion with string paths."""
        output_file = temp_dir / "converted_string.csv"

        convert_png_to_hex_csv(str(sample_png_file), str(output_file))

        assert output_file.exists()

        # Verify content
        df = pd.read_csv(output_file, header=None)
        saved_grid = df.values.tolist()
        assert saved_grid == expected_hex_grid

    def test_convert_png_to_hex_csv_prints_message(
        self, sample_png_file, temp_dir, capsys
    ):
        """Test that conversion prints a success message."""
        output_file = temp_dir / "converted_print.csv"

        convert_png_to_hex_csv(sample_png_file, output_file)

        captured = capsys.readouterr()
        assert "Converted test_image.png to converted_print.csv" in captured.out
