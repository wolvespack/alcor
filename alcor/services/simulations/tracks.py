import os
from typing import (Dict,
                    List)

import h5py
import pandas as pd


def read_da_cooling(path: str = 'input_data/da_cooling.hdf5'
                    ) -> Dict[int, Dict[int, pd.DataFrame]]:
    file = open_hdf5(path)
    da_cooling_tracks_by_metallicities = {1: {},
                                          10: {},
                                          30: {},
                                          60: {}}
    fill_cooling_tracks(da_cooling_tracks_by_metallicities,
                        file=file)

    return da_cooling_tracks_by_metallicities


def read_db_cooling(path: str = 'input_data/db_cooling.hdf5'
                    ) -> Dict[int, Dict[int, pd.DataFrame]]:
    file = open_hdf5(path)
    db_cooling_tracks_by_metallicities = {1: {},
                                          10: {},
                                          60: {}}
    fill_cooling_tracks(db_cooling_tracks_by_metallicities,
                        file=file)

    return db_cooling_tracks_by_metallicities


def read_colors(path: str) -> Dict[int, pd.DataFrame]:
    file = open_hdf5(path)
    colors = {}
    fill_colors(colors,
                file=file)

    return colors


def read_da_colors(path: str = 'input_data/da_colors.hdf5'
                   ) -> Dict[int, pd.DataFrame]:
    return read_colors(path)


def read_db_colors(path: str = 'input_data/db_colors.hdf5'
                   ) -> Dict[int, pd.DataFrame]:
    return read_colors(path)


def read_one_tables(path: str = 'input_data/one_wds_tracks.hdf5'
                    ) -> Dict[int, pd.DataFrame]:
    file = open_hdf5(path)
    one_tables = {}
    fill_one_table(one_tables,
                   file=file)

    return one_tables


def fill_cooling_tracks(cooling_tracks: Dict[int, Dict],
                        *,
                        file: h5py.File) -> None:
    for metallicity in cooling_tracks.keys():
        metallicity_group = str(metallicity) + '/'
        masses = sort_mass_indexes(indexes=file[metallicity_group])

        for mass in masses:
            mass_group = metallicity_group + mass + '/'
            cooling_tracks_by_metallicity = cooling_tracks[metallicity]
            cooling_tracks_by_metallicity[int(mass)] = pd.DataFrame(
                    dict(cooling_time=file[mass_group + 'cooling_time'],
                         effective_temperature=file[mass_group
                                                    + 'effective_temperature'],
                         luminosity=file[mass_group + 'luminosity']))


def fill_colors(color_table: Dict,
                *,
                file: h5py.File) -> None:
    for mass in file:
        mass_group = mass + '/'
        color_table[int(mass)] = pd.DataFrame(dict(
                luminosity=file[mass_group + 'luminosity'],
                color_u=file[mass_group + 'color_u'],
                color_b=file[mass_group + 'color_b'],
                color_v=file[mass_group + 'color_v'],
                color_r=file[mass_group + 'color_r'],
                color_i=file[mass_group + 'color_i'],
                color_j=file[mass_group + 'color_j']))


def fill_one_table(table: Dict,
                   *,
                   file: h5py.File) -> None:
    for mass in file:
        mass_group = mass + '/'
        table[int(mass)] = pd.DataFrame(dict(
                luminosity=file[mass_group + 'luminosity'],
                cooling_time=file[mass_group + 'cooling_time'],
                effective_temperature=file[mass_group
                                           + 'effective_temperature'],
                color_u=file[mass_group + 'color_u'],
                color_b=file[mass_group + 'color_b'],
                color_v=file[mass_group + 'color_v'],
                color_r=file[mass_group + 'color_r'],
                color_i=file[mass_group + 'color_i'],
                color_j=file[mass_group + 'color_j']))


def open_hdf5(path: str) -> h5py.File:
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, path)

    return h5py.File(path,
                     mode='r')


def sort_mass_indexes(indexes: List[str]) -> List[str]:
    indexes = [int(index) for index in indexes]
    indexes.sort()
    return list(map(str, indexes))
