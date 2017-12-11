from typing import (Any,
                    Iterable)

import numpy as np
import pandas as pd
from scipy.interpolate import InterpolatedUnivariateSpline


def white_dwarfs(stars: pd.DataFrame,
                 *,
                 max_galactic_structure_age: float,
                 # TODO: rename, IFMR - initial-to-finall mass relationship
                 ifmr_parameter: float = 1.,
                 chandrasekhar_limit: float = 1.4,
                 max_mass: float = 10.5,
                 solar_metallicity: float = 0.01,
                 subsolar_metallicity: float = 0.001,
                 min_cooling_time: float = 0.) -> pd.DataFrame:
    """
    Filters white dwarfs stars from initial sample of main sequence stars
    and assigns metallicities, cooling times and masses.

    :param stars: main sequence stars
    :param max_galactic_structure_age: the highest age of thin disk,
    thick disk and halo
    :param ifmr_parameter: factor by which white dwarf's mass is multiplied
    :param chandrasekhar_limit: maximum mass of a stable white dwarf
    :param max_mass: maximum mass of a main sequence star
    that can generate a white dwarf
    :param solar_metallicity: metallicity assigned to all thin
    and thick disks white dwarfs due to relatively young ages
    :param subsolar_metallicity: metallicity assigned to all halo white dwarfs
    :param min_cooling_time: natural lower limit for cooling time
    :return: white dwarfs
    """
    stars = stars[stars['progenitor_mass'] < max_mass]
    set_metallicities(stars,
                      subsolar_metallicity=subsolar_metallicity,
                      solar_metallicity=solar_metallicity)
    set_cooling_times(stars,
                      max_galactic_structure_age=max_galactic_structure_age,
                      subsolar_metallicity=subsolar_metallicity,
                      solar_metallicity=solar_metallicity)
    stars = stars[stars['cooling_time'] > min_cooling_time]
    set_masses(stars,
               ifmr_parameter=ifmr_parameter)

    return stars[stars['mass'] <= chandrasekhar_limit]


def set_metallicities(stars: pd.DataFrame,
                      *,
                      subsolar_metallicity: float,
                      solar_metallicity: float) -> None:
    stars['metallicity'] = np.empty(stars.shape[0])

    halo_stars_mask = (stars['galactic_disk_type'] == 'halo')
    non_halo_stars_mask = (stars['galactic_disk_type'] != 'halo')

    stars.loc[halo_stars_mask, 'metallicity'] = subsolar_metallicity
    stars.loc[non_halo_stars_mask, 'metallicity'] = solar_metallicity


def set_cooling_times(stars: pd.DataFrame,
                      *,
                      max_galactic_structure_age: float,
                      solar_metallicity: float,
                      subsolar_metallicity: float) -> None:
    main_sequence_lifetimes = get_main_sequence_lifetimes(
            masses=stars['progenitor_mass'],
            metallicities=stars['metallicity'],
            solar_metallicity=solar_metallicity,
            subsolar_metallicity=subsolar_metallicity)

    stars['cooling_time'] = (max_galactic_structure_age
                             - stars['birth_time']
                             - main_sequence_lifetimes)


def set_masses(stars: pd.DataFrame,
               *,
               ifmr_parameter: float) -> None:
    stars['mass'] = ifmr_parameter * white_dwarf_masses(
            progenitor_masses=stars['progenitor_mass'])


def immutable_array(elements: Iterable[Any]) -> np.ndarray:
    result = np.array(elements)
    result.setflags(write=False)
    return result


def get_main_sequence_lifetimes(*,
                                masses: np.ndarray,
                                metallicities: np.ndarray,
                                solar_metallicity: float,
                                subsolar_metallicity: float,
                                model_solar_masses: immutable_array(
                                        [1.00, 1.50, 1.75, 2.00, 2.25,
                                         2.50, 3.00, 3.50, 4.00, 5.00]),
                                model_solar_times: immutable_array(
                                        [8.614, 1.968, 1.249, 0.865, 0.632,
                                         0.480, 0.302, 0.226, 0.149, 0.088]),
                                model_subsolar_masses: immutable_array(
                                        [0.85, 1.00, 1.25, 1.50,
                                         1.75, 2.00, 3.00]),
                                model_subsolar_times: immutable_array(
                                        [10.34, 5.756, 2.623, 1.412,
                                         0.905, 0.639, 0.245])
                                ) -> np.ndarray:
    """
    Calculates lifetime of a main sequence star
    according to model by Leandro & Renedo et al.(2010).
    Solar metallicity values from Althaus priv. comm (X = 0.725, Y = 0.265)
    Sub-solar metallicity values from Althaus priv. comm (X = 0.752, Y = 0.247)
    """
    solar_main_sequence_lifetimes = estimated_times(
            masses=masses,
            model_masses=model_solar_masses,
            model_times=model_solar_times)
    subsolar_main_sequence_lifetimes = estimated_times(
            masses=masses,
            model_masses=model_subsolar_masses,
            model_times=model_subsolar_times)

    estimate_lifetimes = np.vectorize(estimate_lifetime)

    return estimate_lifetimes(
            metallicity=metallicities,
            subsolar_main_sequence_lifetime=subsolar_main_sequence_lifetimes,
            solar_main_sequence_lifetime=solar_main_sequence_lifetimes,
            subsolar_metallicity=subsolar_metallicity,
            solar_metallicity=solar_metallicity)


def estimated_times(*,
                    masses: np.ndarray,
                    model_masses: np.ndarray,
                    model_times: np.ndarray) -> np.ndarray:
    times = np.empty(masses.size)

    spline = InterpolatedUnivariateSpline(x=model_masses,
                                          y=model_times,
                                          k=1)

    masses_lt_max_mask = masses < model_masses[-1]
    masses_ge_max_mask = ~masses_lt_max_mask
    times[masses_lt_max_mask] = spline(masses[masses_lt_max_mask])
    times[masses_ge_max_mask] = extrapolated_times(
            masses=masses[masses_ge_max_mask],
            rightmost_mass=model_masses[-1],
            rightmost_time=model_times[-1])

    return times


def extrapolated_times(*,
                       masses: np.ndarray,
                       rightmost_mass: float,
                       rightmost_time: float) -> np.ndarray:
    """
    Extrapolates main sequence stars' (progenitors)
    lifetime vs mass to the right.
    Makes sure that no negative values will be produced.
    """
    return rightmost_time * rightmost_mass / masses


def estimate_lifetime(*,
                      metallicity: float,
                      subsolar_main_sequence_lifetime: float,
                      solar_main_sequence_lifetime: float,
                      subsolar_metallicity: float,
                      solar_metallicity: float) -> float:
    spline = InterpolatedUnivariateSpline(
            x=(subsolar_metallicity, solar_metallicity),
            y=(subsolar_main_sequence_lifetime, solar_main_sequence_lifetime),
            k=1)
    return spline(metallicity)


def white_dwarf_masses(progenitor_masses: np.ndarray) -> np.ndarray:
    """
    IFMR (Initial-to-final mass relationship)
    according to model by Catalan et al. 2008).
    Combination with a model by Iben for masses greater than 6 solar masses
    :param progenitor_masses: masses of main sequence stars
    :return: masses of resulting white dwarfs
    """
    masses = np.empty(progenitor_masses.size)

    low_progenitor_masses_mask = progenitor_masses < 2.7
    low_progenitor_masses = progenitor_masses[low_progenitor_masses_mask]

    medium_progenitor_masses_mask = ((progenitor_masses >= 2.7)
                                     & (progenitor_masses <= 6.))
    medium_progenitor_masses = progenitor_masses[medium_progenitor_masses_mask]

    high_progenitor_masses_mask = (progenitor_masses > 6.)
    high_progenitor_masses = progenitor_masses[high_progenitor_masses_mask]

    masses[low_progenitor_masses_mask] = 0.096 * low_progenitor_masses + 0.429
    masses[medium_progenitor_masses_mask] = (0.137 * medium_progenitor_masses
                                             + 0.3183)
    masses[high_progenitor_masses_mask] = (0.1057 * high_progenitor_masses
                                           + 0.5061)

    return masses
