from typing import (Dict,
                    Tuple,
                    List)

import math
import numpy as np
import pandas as pd

from alcor.services.simulations.magnitudes import (estimate_at,
                                                   estimated_interest_value,
                                                   calculate_index,
                                                   extrapolating_by_grid,
                                                   get_min_metallicity_index,
                                                   generate_spectral_types,
                                                   extrapolate_interest_value,
                                                   interpolate_interest_value,
                                                   estimate_color,
                                                   estimate_by_mass,
                                                   assign_estimated_values)


def test_estimate_at(float_value: float,
                     same_values_grid: Tuple[np.ndarray, np.ndarray],
                     grid: Tuple[np.ndarray, np.ndarray],
                     max_slope: float,
                     max_term: float,
                     min_slope: float,
                     min_term: float) -> None:
    same_values_grid_x_array, same_values_grid_y_array = same_values_grid
    grid_x_array, grid_y_array = grid

    estimated_value = estimate_at(float_value,
                                  x=same_values_grid_x_array,
                                  y=same_values_grid_y_array)
    other_estimated_value = estimate_at(float_value,
                                        x=grid_x_array,
                                        y=grid_y_array)

    assert math.isclose(same_values_grid_y_array[0], estimated_value)
    assert other_estimated_value < max_slope * float_value + max_term
    assert other_estimated_value > min_slope * float_value + min_term


def test_estimated_interest_value(
        cooling_time: float,
        grid_and_index: Tuple[np.ndarray, np.ndarray, int]) -> None:
    cooling_time_grid, interest_parameter_grid, row_index = grid_and_index
    value = estimated_interest_value(
            cooling_time=cooling_time,
            cooling_time_grid=cooling_time_grid,
            interest_parameter_grid=interest_parameter_grid,
            row_index=row_index)

    assert isinstance(value, float)
    assert math.isfinite(value)


def test_calculate_index(float_value: float,
                         x_array: np.ndarray) -> None:
    index = calculate_index(float_value,
                            grid=x_array)

    assert isinstance(index, int)
    assert index == -2 or 0 <= index <= x_array.size - 1


def test_extrapolating_by_grid(cooling_time: float,
                               x_array: np.ndarray) -> None:
    result = extrapolating_by_grid(cooling_time,
                                   cooling_time_grid=x_array)

    assert isinstance(result, bool)
    assert math.isfinite(result)


def test_get_min_metallicity_index(metallicity: float,
                                   grid_metallicities: List[float]) -> None:
    metallicity_index = get_min_metallicity_index(
            metallicity,
            grid_metallicities=grid_metallicities)

    assert isinstance(metallicity_index, int)
    assert (metallicity_index == -2 or
            0 <= metallicity_index <= len(grid_metallicities) - 1)


def test_generate_spectral_types(db_to_da_fraction: float,
                                 size: int) -> None:
    spectral_types = generate_spectral_types(
            db_to_da_fraction=db_to_da_fraction,
            size=size)

    assert isinstance(spectral_types, np.ndarray)
    assert spectral_types.size == size


def test_extrapolate_interest_value(
        mass: float,
        cooling_time: float,
        greater_mass_grid: Tuple[np.ndarray, np.ndarray],
        lesser_mass_grid: Tuple[np.ndarray, np.ndarray],
        min_and_max_mass: Tuple[float, float],
        min_row_index: int,
        max_row_index: int) -> None:
    greater_mass_cooling_time_grid, greater_mass_interest_parameter_grid = (
        greater_mass_grid)
    lesser_mass_cooling_time_grid, lesser_mass_interest_parameter_grid = (
        lesser_mass_grid)
    min_mass = min_and_max_mass[0]
    max_mass = min_and_max_mass[1] + 1.

    value = extrapolate_interest_value(
            mass=mass,
            cooling_time=cooling_time,
            greater_mass_cooling_time_grid=greater_mass_cooling_time_grid,
            greater_mass_interest_parameter_grid=(
                greater_mass_interest_parameter_grid),
            lesser_mass_cooling_time_grid=lesser_mass_cooling_time_grid,
            lesser_mass_interest_parameter_grid=(
                lesser_mass_interest_parameter_grid),
            min_mass=min_mass,
            max_mass=max_mass,
            min_row_index=min_row_index,
            max_row_index=max_row_index)

    assert isinstance(value, float)
    assert math.isfinite(value)


def test_interpolate_interest_value(
        mass: float,
        cooling_time: float,
        greater_mass_grid: Tuple[np.ndarray, np.ndarray],
        lesser_mass_grid: Tuple[np.ndarray, np.ndarray],
        min_and_max_mass: Tuple[float, float],
        min_row_index: int,
        max_row_index: int) -> None:
    greater_mass_cooling_time_grid, greater_mass_interest_parameter_grid = (
        greater_mass_grid)
    lesser_mass_cooling_time_grid, lesser_mass_interest_parameter_grid = (
        lesser_mass_grid)
    min_mass = min_and_max_mass[0]
    max_mass = min_and_max_mass[1] + 1.

    value = interpolate_interest_value(
            mass=mass,
            cooling_time=cooling_time,
            greater_mass_cooling_time_grid=greater_mass_cooling_time_grid,
            greater_mass_interest_parameter_grid=(
                greater_mass_interest_parameter_grid),
            lesser_mass_cooling_time_grid=lesser_mass_cooling_time_grid,
            lesser_mass_interest_parameter_grid=(
                lesser_mass_interest_parameter_grid),
            min_mass=min_mass,
            max_mass=max_mass,
            min_row_index=min_row_index,
            max_row_index=max_row_index)

    assert isinstance(value, float)
    assert math.isfinite(value)


def test_estimate_color(star_series: pd.Series,
                        color_table: Dict[int, pd.DataFrame],
                        color: str) -> None:
    color = estimate_color(star_series,
                           color_table=color_table,
                           color=color)

    assert isinstance(color, float)
    assert math.isfinite(color)


def test_estimate_by_mass(star_series: pd.Series,
                          tracks: Dict[int, pd.DataFrame],
                          interest_parameter: str) -> None:
    parameter = estimate_by_mass(star_series,
                                 tracks=tracks,
                                 interest_parameter=interest_parameter)

    assert isinstance(parameter, float)
    assert math.isfinite(parameter)


def test_assign_estimated_values(
        stars: pd.DataFrame,
        da_cooling_sequences: Dict[int, Dict[int, pd.DataFrame]],
        da_color_table: Dict[int, pd.DataFrame],
        db_cooling_sequences: Dict[int, Dict[int, pd.DataFrame]],
        db_color_table: Dict[int, pd.DataFrame],
        one_color_table: Dict[int, pd.DataFrame]) -> None:
    parameters_before = stars.columns.values
    stars = assign_estimated_values(stars,
                                    da_cooling_sequences=da_cooling_sequences,
                                    da_color_table=da_color_table,
                                    db_cooling_sequences=db_cooling_sequences,
                                    db_color_table=db_color_table,
                                    one_color_table=one_color_table)
    parameters_after = stars.columns.values

    assert isinstance(stars, pd.DataFrame)
    assert parameters_after.size > parameters_before.size
