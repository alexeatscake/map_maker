# Map Maker

A Python-based procedural map generation tool that creates detailed terrain maps by combining small tile patterns into larger landscapes. The system uses a hierarchical approach, starting with a simple base map and expanding it using predefined terrain tile patterns.

## Features

- **Procedural terrain generation** with water, grass, and forest biomes
- **Tile-based map expansion** using 20x20 pixel terrain patterns
- **Automatic smoothing algorithms** to create realistic terrain transitions
- **PNG image output** for visual map representation
- **CSV data formats** for both intermediate processing and final output

## Project Structure

```text
map_maker/
├── py_script/           # Core Python scripts
│   ├── make_base_map.py    # Generates initial terrain grid
│   ├── make_big_hex.py     # Expands base map using tile patterns
│   ├── generate_hex.py     # Converts PNG tiles to CSV hex data
│   └── big_hex_to_image.py # Converts final CSV to PNG image
├── hex_grid/           # CSV files with hex color data (20x20 tiles)
├── pixel_image/        # PNG tile images (20x20 pixels)
├── made_maps/          # Generated output maps
└── pyproject.toml      # Project dependencies
```

## How It Works

The map generation process follows a 4-step pipeline:

### 1. Generate Base Map (`make_base_map.py`)

- Creates a 40x40 grid with three terrain types:
  - `0` = Water (blue)
  - `1` = Grass (green)
  - `2` = Forest (dark green)
- Applies smoothing algorithms to create natural-looking terrain clusters
- Prevents forest tiles from directly touching water (realistic biome boundaries)
- Outputs: `made_maps/base_map.csv`

### 2. Create Tile Key (`make_big_hex.py`)

- Processes the base map in 2x2 blocks to generate terrain transition keys
- Maps numeric terrain values to letters: `w`(water), `g`(grass), `f`(forest)
- Creates 4-character keys representing corner patterns (e.g., "gggg", "wgfg")
- Outputs: `made_maps/big_key.csv`

### 3. Expand Using Tile Patterns (`make_big_hex.py`)

- Loads pre-designed 20x20 terrain tiles from `hex_grid/` directory
- Each tile corresponds to a specific terrain transition pattern
- Replaces each key in the tile grid with its corresponding 20x20 pattern
- Creates a final detailed map (typically 780x780 pixels)
- Outputs: `made_maps/expanded_map.csv`

### 4. Generate Final Image (`big_hex_to_image.py`)

- Converts the CSV hex color data to a PNG image
- Each cell becomes a pixel with the specified hex color
- Outputs: `made_maps/expanded_map.png`

## Terrain Tile System

The project includes 29 pre-designed terrain tiles covering all possible 2x2 combinations:

- **Pure tiles**: `ffff`, `gggg`, `wwww` (single terrain type)
- **Transition tiles**: `wgfg`, `gwgg`, etc. (mixed terrain boundaries)
- Each tile exists in both PNG format (`pixel_image/`) and CSV hex format (`hex_grid/`)

## Dependencies

- **Python 3.12+**
- **pandas** (≥2.3.0) - Data manipulation and CSV handling
- **Pillow** (≥11.2.1) - Image processing and PNG generation
- **numpy** - Numerical operations for grid processing
- **matplotlib** (≥3.10.3) - Visualization support

## Usage

Run the complete map generation pipeline:

```bash
# 1. Generate base terrain grid
python py_script/make_base_map.py

# 2. Expand using tile patterns and create detailed map
python py_script/make_big_hex.py

# 3. Convert final map to PNG image
python py_script/big_hex_to_image.py
```

Or if you have new PNG tiles to convert to hex format:

```bash
python py_script/generate_hex.py
```

## Output

The final generated map will be saved as:

- `made_maps/expanded_map.csv` - Detailed hex color data
- `made_maps/expanded_map.png` - Visual PNG image

The resulting maps feature realistic terrain with smooth transitions between water bodies, grasslands, and forested areas.

## Installation

1. Clone the repository
2. Install dependencies: `pip install -e .`
3. Run the scripts in sequence as shown above

## Customization

- **Grid size**: Modify `GRID_SIZE` in `make_base_map.py` (default: 40x40)
- **Terrain types**: Add new terrain codes and corresponding tiles
- **Smoothing**: Adjust iteration count in the smoothing loop
- **Tile patterns**: Create new 20x20 PNG tiles and run `generate_hex.py` to convert them
