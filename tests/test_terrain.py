"""Tests for the terrain module."""

import numpy as np

from map_maker.terrain import (
    apply_biome_rules,
    generate_base_map_smooth,
    initialize_grid,
    smooth_grid,
)


class TestInitializeGrid:
    """Test the initialize_grid function."""

    def test_initialize_grid_basic_properties(self):
        """Test that grid has correct size and border properties."""
        size = 10
        grid = initialize_grid(size)

        # Check dimensions
        assert grid.shape == (size, size)

        # Check data type
        assert grid.dtype == int

        # Check that borders are water (0)
        assert np.all(grid[0, :] == 0)  # Top edge
        assert np.all(grid[-1, :] == 0)  # Bottom edge
        assert np.all(grid[:, 0] == 0)  # Left edge
        assert np.all(grid[:, -1] == 0)  # Right edge

    def test_initialize_grid_interior_values(self):
        """Test that interior contains valid terrain values."""
        size = 5
        grid = initialize_grid(size)

        # Get interior values (excluding borders)
        interior = grid[1:-1, 1:-1]

        # Check that all values are valid terrain types (0, 1, or 2)
        valid_values = {0, 1, 2}
        assert set(np.unique(interior)).issubset(valid_values)

    def test_initialize_grid_different_sizes(self):
        """Test that function works with different grid sizes."""
        for size in [3, 5, 20, 50]:
            grid = initialize_grid(size)
            assert grid.shape == (size, size)
            assert np.all(grid[0, :] == 0)  # Top border is water
            assert np.all(grid[-1, :] == 0)  # Bottom border is water

    def test_initialize_grid_randomness(self):
        """Test that multiple calls produce different results."""
        size = 10
        grid1 = initialize_grid(size)
        grid2 = initialize_grid(size)

        # Grids should be different (very high probability)
        assert not np.array_equal(grid1, grid2)


class TestSmoothGrid:
    """Test the smooth_grid function."""

    def test_smooth_grid_preserves_size(self):
        """Test that smoothing preserves grid dimensions."""
        original = np.array(
            [
                [0, 0, 0, 0, 0],
                [0, 1, 2, 1, 0],
                [0, 2, 1, 2, 0],
                [0, 1, 2, 1, 0],
                [0, 0, 0, 0, 0],
            ]
        )
        smoothed = smooth_grid(original)

        assert smoothed.shape == original.shape

    def test_smooth_grid_preserves_borders(self):
        """Test that smoothing doesn't change border cells."""
        original = np.array(
            [
                [0, 0, 0, 0, 0],
                [0, 1, 2, 1, 0],
                [0, 2, 1, 2, 0],
                [0, 1, 2, 1, 0],
                [0, 0, 0, 0, 0],
            ]
        )
        smoothed = smooth_grid(original)

        # Borders should remain unchanged
        assert np.array_equal(smoothed[0, :], original[0, :])  # Top
        assert np.array_equal(smoothed[-1, :], original[-1, :])  # Bottom
        assert np.array_equal(smoothed[:, 0], original[:, 0])  # Left
        assert np.array_equal(smoothed[:, -1], original[:, -1])  # Right

    def test_smooth_grid_majority_rule(self):
        """Test that smoothing applies majority rule correctly."""
        # Create a grid where center cell should change
        original = np.array(
            [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 2, 1, 0],  # Center is 2, surrounded by 1s
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
            ]
        )
        smoothed = smooth_grid(original)

        # Center should become 1 (majority of neighbors)
        assert smoothed[2, 2] == 1

    def test_smooth_grid_no_change_when_stable(self):
        """Test that stable configurations don't change much."""
        # Create a configuration where center has strong majority
        original = np.array(
            [
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
            ]
        )
        smoothed = smooth_grid(original)

        # All interior cells should remain unchanged (all neighbors are same)
        assert np.array_equal(smoothed[1:4, 1:4], original[1:4, 1:4])

    def test_smooth_grid_edge_effects(self):
        """Test smoothing behavior at edges between different terrain types."""
        # Create a pattern where corner grass cells are surrounded by more water
        original = np.array(
            [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
            ]
        )
        smoothed = smooth_grid(original)

        # Corner grass cells should change to water (have 5+ water neighbors)
        assert smoothed[1, 1] == 0  # Top-left corner
        assert smoothed[1, 3] == 0  # Top-right corner
        assert smoothed[3, 1] == 0  # Bottom-left corner
        assert smoothed[3, 3] == 0  # Bottom-right corner

        # Center should remain grass (surrounded by grass)
        assert smoothed[2, 2] == 1

    def test_smooth_grid_immutability(self):
        """Test that original grid is not modified."""
        original = np.array(
            [
                [0, 0, 0, 0, 0],
                [0, 1, 2, 1, 0],
                [0, 2, 1, 2, 0],
                [0, 1, 2, 1, 0],
                [0, 0, 0, 0, 0],
            ]
        )
        original_copy = original.copy()

        smooth_grid(original)

        # Original should be unchanged
        assert np.array_equal(original, original_copy)


class TestApplyBiomeRules:
    """Test the apply_biome_rules function."""

    def test_apply_biome_rules_forest_water_conversion(self):
        """Test that forest adjacent to water becomes grass."""
        original = np.array(
            [
                [0, 0, 0, 0, 0],
                [0, 2, 1, 1, 0],  # Forest next to water
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
            ]
        )
        processed = apply_biome_rules(original)

        # Forest at [1,1] should become grass because it touches water at [0,1]
        assert processed[1, 1] == 1

    def test_apply_biome_rules_preserves_valid_forest(self):
        """Test that forest not touching water remains forest."""
        original = np.array(
            [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 2, 1, 0],  # Forest surrounded by grass
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
            ]
        )
        processed = apply_biome_rules(original)

        # Forest should remain forest
        assert processed[2, 2] == 2

    def test_apply_biome_rules_preserves_other_terrain(self):
        """Test that water and grass are not affected by biome rules."""
        original = np.array(
            [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 0, 1, 0],  # Water in middle
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
            ]
        )
        processed = apply_biome_rules(original)

        # Water and grass should remain unchanged
        assert np.array_equal(processed, original)

    def test_apply_biome_rules_diagonal_adjacency(self):
        """Test that diagonal adjacency to water affects forest."""
        original = np.array(
            [
                [0, 1, 1, 1, 1],
                [1, 2, 1, 1, 1],  # Forest diagonally adjacent to water
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
            ]
        )
        processed = apply_biome_rules(original)

        # Forest should become grass due to diagonal water adjacency
        assert processed[1, 1] == 1

    def test_apply_biome_rules_immutability(self):
        """Test that original grid is not modified."""
        original = np.array(
            [
                [0, 0, 0, 0, 0],
                [0, 2, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
            ]
        )
        original_copy = original.copy()

        apply_biome_rules(original)

        # Original should be unchanged
        assert np.array_equal(original, original_copy)


class TestGenerateBaseMapSmooth:
    """Test the generate_base_map_smooth function."""

    def test_generate_base_map_smooth_creates_file(self, temp_dir):
        """Test that function creates output file."""
        output_path = temp_dir / "test_map.csv"
        size = 10

        result = generate_base_map_smooth(size, output_path)

        # File should exist
        assert output_path.exists()

        # Should return grid
        assert isinstance(result, np.ndarray)
        assert result.shape == (size, size)

    def test_generate_base_map_smooth_file_content(self, temp_dir):
        """Test that output file contains valid CSV data."""
        output_path = temp_dir / "test_map.csv"
        size = 5

        result = generate_base_map_smooth(size, output_path)

        # Load from file and compare
        loaded = np.loadtxt(output_path, delimiter=",", dtype=int)
        assert np.array_equal(result, loaded)

    def test_generate_base_map_smooth_creates_directories(self, temp_dir):
        """Test that function creates parent directories."""
        nested_path = temp_dir / "subdir" / "nested" / "map.csv"
        size = 5

        generate_base_map_smooth(size, nested_path)

        # File and directories should exist
        assert nested_path.exists()
        assert nested_path.parent.exists()

    def test_generate_base_map_smooth_different_iterations(self, temp_dir):
        """Test that different smoothing iterations produce different results."""
        output_path1 = temp_dir / "map1.csv"
        output_path2 = temp_dir / "map2.csv"
        size = 10

        # Use same seed for reproducibility in this test
        np.random.seed(42)
        result1 = generate_base_map_smooth(size, output_path1, smoothing_iterations=1)

        np.random.seed(42)
        result2 = generate_base_map_smooth(size, output_path2, smoothing_iterations=5)

        # Results should be different due to different smoothing
        assert not np.array_equal(result1, result2)

    def test_generate_base_map_smooth_validates_terrain_rules(self, temp_dir):
        """Test that generated map follows terrain rules."""
        output_path = temp_dir / "map.csv"
        size = 20

        result = generate_base_map_smooth(size, output_path)

        # Check that forest doesn't touch water
        for i in range(1, size - 1):
            for j in range(1, size - 1):
                if result[i, j] == 2:  # If forest
                    neighbors = [
                        result[i - 1, j - 1],
                        result[i - 1, j],
                        result[i - 1, j + 1],
                        result[i, j - 1],
                        result[i, j + 1],
                        result[i + 1, j - 1],
                        result[i + 1, j],
                        result[i + 1, j + 1],
                    ]
                    # Should not have water neighbors
                    assert 0 not in neighbors

    def test_generate_base_map_smooth_with_pathlib(self, temp_dir):
        """Test that function works with Path objects."""
        output_path = temp_dir / "pathlib_test.csv"
        size = 8

        result = generate_base_map_smooth(size, output_path)

        assert output_path.exists()
        assert result.shape == (size, size)

    def test_generate_base_map_smooth_with_string_path(self, temp_dir):
        """Test that function works with string paths."""
        output_path = temp_dir / "string_test.csv"
        size = 8

        result = generate_base_map_smooth(size, str(output_path))

        assert output_path.exists()
        assert result.shape == (size, size)
