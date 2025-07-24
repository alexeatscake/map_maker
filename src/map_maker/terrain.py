"""Terrain generation functions for procedural map creation."""

from pathlib import Path

import numpy as np


def initialize_grid(size: int) -> np.ndarray:
    """
    Initialize a terrain grid with random water, grass, and forest distribution.

    Creates a grid where:
    - Borders are set to water (0) for natural boundaries
    - Interior is randomly filled with water (0), grass (1), or forest (2)
    - Grid starts as all grass, then interior gets random terrain types

    Args:
        size: Grid dimensions (creates size x size grid)

    Returns:
        2D numpy array with terrain values:
        - 0 = Water (blue)
        - 1 = Grass (green)
        - 2 = Forest (dark green)
    """
    # Start with all grass
    grid = np.ones((size, size), dtype=int)

    # Set borders to water for natural boundaries
    grid[0, :] = 0  # Top edge
    grid[-1, :] = 0  # Bottom edge
    grid[:, 0] = 0  # Left edge
    grid[:, -1] = 0  # Right edge

    # Randomly fill interior with water (0), grass (1), or forest (2)
    interior_vals = np.random.randint(0, 3, size=(size - 2, size - 2))
    grid[1:-1, 1:-1] = interior_vals

    return grid


def smooth_grid(grid: np.ndarray) -> np.ndarray:
    """
    Apply smoothing to reduce noise and create more natural terrain clusters.

    Uses a cellular automata-like approach where each cell adopts the most
    common terrain type among its 8 neighbors if that type appears 5+ times.
    This creates more cohesive terrain regions.

    Args:
        grid: Input terrain grid to smooth

    Returns:
        Smoothed copy of the input grid
    """
    smoothed_grid = grid.copy()

    # Process all interior cells (skip borders)
    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            # Get all 8 neighboring cells
            neighbors = [
                grid[i - 1, j - 1],  # Top-left
                grid[i - 1, j],  # Top
                grid[i - 1, j + 1],  # Top-right
                grid[i, j - 1],  # Left
                grid[i, j + 1],  # Right
                grid[i + 1, j - 1],  # Bottom-left
                grid[i + 1, j],  # Bottom
                grid[i + 1, j + 1],  # Bottom-right
            ]

            # Find the most common terrain type
            most_common = max(set(neighbors), key=neighbors.count)

            # If 5+ neighbors are the same type, adopt that type
            if neighbors.count(most_common) >= 5:
                smoothed_grid[i, j] = most_common

    return smoothed_grid


def apply_biome_rules(grid: np.ndarray) -> np.ndarray:
    """
    Apply realistic biome transition rules to the terrain.

    Prevents unrealistic terrain combinations by ensuring forest (2)
    never directly touches water (0). This creates more believable
    landscapes where grasslands act as transition zones.

    Args:
        grid: Input terrain grid to process

    Returns:
        Grid with biome rules applied (forest cells touching water become grass)
    """
    updated_grid = grid.copy()

    # Check all interior cells
    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            # If current cell is forest
            if grid[i, j] == 2:
                # Check all 8 neighbors
                neighbors = [
                    grid[i - 1, j - 1],  # Top-left
                    grid[i - 1, j],  # Top
                    grid[i - 1, j + 1],  # Top-right
                    grid[i, j - 1],  # Left
                    grid[i, j + 1],  # Right
                    grid[i + 1, j - 1],  # Bottom-left
                    grid[i + 1, j],  # Bottom
                    grid[i + 1, j + 1],  # Bottom-right
                ]

                # If any neighbor is water, convert forest to grass
                if 0 in neighbors:
                    updated_grid[i, j] = 1

    return updated_grid


def generate_base_map_smooth(
    size: int, output_path: str | Path, smoothing_iterations: int = 3
) -> np.ndarray:
    """
    Generate a base terrain map using cellular automata smoothing.

    Creates a procedural terrain map by:
    1. Initializing a random grid
    2. Applying smoothing to create terrain clusters
    3. Enforcing realistic biome transition rules
    4. Saving the result to a CSV file

    This specific implementation uses smoothing-based terrain generation.
    Future variants could use different algorithms (e.g., Perlin noise,
    Voronoi diagrams, etc.).

    Args:
        size: Grid dimensions (creates size x size grid)
        output_path: Where to save the generated map
        smoothing_iterations: Number of smoothing passes (default: 3)

    Returns:
        Final processed terrain grid
    """
    # Step 1: Initialize with random terrain
    grid = initialize_grid(size)

    # Step 2: Apply smoothing to create natural clusters
    for _ in range(smoothing_iterations):
        grid = smooth_grid(grid)

    # Step 3: Apply biome rules for realism
    grid = apply_biome_rules(grid)

    # Step 4: Save to file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(output_file, grid, fmt="%d", delimiter=",")

    print(f"Generated base map: {output_file}")
    return grid
