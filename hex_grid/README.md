# Hex Grid Directory

This directory contains CSV files with hex color data for terrain tiles.

## File Format

Each CSV file represents a 20x20 grid of hex color values that correspond to specific terrain transition patterns.

## Naming Convention

Files are named based on terrain combinations using the pattern `[terrain_code][variant].csv`:

- `f` = Forest
- `g` = Grass
- `w` = Water

Examples:

- `ffff1.csv` - Pure forest tile
- `gggg1.csv` - Pure grass tile
- `wwww1.csv` - Pure water tile
- `wgfg1.csv` - Mixed terrain transition tile

## Generation

These files are generated from PNG images in the `pixel_image/` directory using the `generate_hex.py` script. The contents are ignored by git to keep the repository clean.
