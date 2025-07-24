from pathlib import Path

# Import our new tiles module
from map_maker.tiles import convert_png_to_hex_csv


def main():
    """Convert all PNG files in pixel_image directory to hex CSV files."""
    # Get the main directory (parent of py_script)
    main_dir = Path(__file__).parent.parent

    pixel_image_dir = main_dir / "pixel_image"
    hex_grid_dir = main_dir / "hex_grid"

    # Use glob to find all PNG files in pixel_image directory
    png_files = list(pixel_image_dir.glob("*.png"))

    for image_path in png_files:
        # Create output path with same base name but .csv extension
        hex_csv_path = hex_grid_dir / f"{image_path.stem}.csv"

        # Use our new function to convert PNG to hex CSV
        convert_png_to_hex_csv(image_path, hex_csv_path)


if __name__ == "__main__":
    main()
