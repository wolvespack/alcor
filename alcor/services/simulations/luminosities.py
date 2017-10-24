import numpy as np
import pandas as pd

from alcor.models.star import GalacticDiskType


def get_white_dwarfs(stars: pd.DataFrame,
                     max_galactic_structure_age: float,
                     ifmr_parameter: float,
                     chandrasekhar_limit: float = 1.4,
                     max_mass: float = 10.5,
                     solar_metallicity: float = 0.01,
                     subsolar_metallicity: float = 0.001) -> pd.DataFrame:
    stars = filter_by_max_mass(stars,
                               max_mass=max_mass)
    set_metallicities(stars,
                      subsolar_metallicity=subsolar_metallicity,
                      solar_metallicity=solar_metallicity)
    set_cooling_times(stars,
                      max_galactic_structure_age=max_galactic_structure_age)
    stars = filter_by_cooling_time(stars)
    set_masses(stars,
               ifmr_parameter=ifmr_parameter)

    return filter_by_chandrasekhar_limit(stars,
                                         limit=chandrasekhar_limit)


def filter_by_chandrasekhar_limit(stars: pd.DataFrame,
                                  limit: float) -> pd.DataFrame:
    return stars[stars['mass'] <= limit]


def set_masses(stars: pd.DataFrame,
               ifmr_parameter: float) -> None:
    stars['mass'] = ifmr_parameter * get_white_dwarf_masses(
            progenitor_masses=stars['progenitor_mass'])


def filter_by_cooling_time(stars: pd.DataFrame,
                           min_cooling_time: float = 0.) -> pd.DataFrame:
    return stars[stars['cooling_times'] > min_cooling_time]


def filter_by_max_mass(stars: pd.DataFrame,
                       max_mass: float) -> pd.DataFrame:
    return stars[stars['progenitor_mass'] < max_mass]


def set_metallicities(stars: pd.DataFrame,
                      subsolar_metallicity: float,
                      solar_metallicity: float) -> None:
    stars['metallicity'] = np.empty(stars.shape[0])

    halo_stars_mask = (stars['galactic_disk_type']
                       == GalacticDiskType.halo)
    non_halo_stars_mask = (stars['galactic_disk_type']
                           != GalacticDiskType.halo)

    stars[halo_stars_mask] = subsolar_metallicity
    stars[non_halo_stars_mask] = solar_metallicity


# TODO: avoid iteration by rows of pandas DataFrame
def set_cooling_times(stars: pd.DataFrame,
                      max_galactic_structure_age: float) -> None:
    main_sequence_lifetimes = []
    for progenitor_mass, metallicity in zip(stars['progenitor_mass'],
                                            stars['metallicity']):
        main_sequence_lifetimes.append(get_main_sequence_lifetime(
                mass=progenitor_mass,
                metallicity=metallicity))
    main_sequence_lifetimes = np.array(main_sequence_lifetimes)

    stars['cooling_times'] = (max_galactic_structure_age - stars['birth_time']
                              - main_sequence_lifetimes)


# TODO: use pandas
# According to model by Leandro & Renedo et al.(2010)
def get_main_sequence_lifetime(*,
                               mass: float,
                               metallicity: float) -> float:
    main_sequence_masses = np.array([1.00, 1.50, 1.75, 2.00, 2.25,
                                     2.50, 3.00, 3.50, 4.00, 5.00])
    # Althaus priv. comm X = 0.725, Y = 0.265
    main_sequence_times = np.array([8.614, 1.968, 1.249, 0.865, 0.632,
                                    0.480, 0.302, 0.226, 0.149, 0.088])

    if mass < main_sequence_masses[0]:
        pen = ((main_sequence_times[1] - main_sequence_times[0])
               / (main_sequence_masses[1] - main_sequence_masses[0]))
        tsol = pen * mass + (main_sequence_times[0]
                             - pen * main_sequence_masses[0])
    else:
        if mass > main_sequence_masses[-1]:
            tsol = (main_sequence_masses[-1] / mass) * main_sequence_times[-1]
        else:
            tsol = interpolated_time(mass=mass,
                                     model_masses=main_sequence_masses,
                                     model_times=main_sequence_times)

    main_sequence_masses = np.array([0.85, 1.00, 1.25, 1.50, 1.75, 2.00, 3.00])
    # Althaus priv. comm X = 0.752, Y = 0.247
    main_sequence_times = np.array([10.34, 5.756, 2.623, 1.412,
                                    0.905, 0.639, 0.245])

    # TODO: put this in a function as it is the same if as before
    if mass < main_sequence_masses[0]:
        pen = ((main_sequence_times[1] - main_sequence_times[0])
               / (main_sequence_masses[1] - main_sequence_masses[0]))
        tsub = pen * mass + (main_sequence_times[0]
                             - pen * main_sequence_masses[0])
    else:
        if mass > main_sequence_masses[-1]:
            tsub = (main_sequence_masses[-1] / mass) * main_sequence_times[-1]
        else:
            tsub = interpolated_time(mass=mass,
                                     model_masses=main_sequence_masses,
                                     model_times=main_sequence_times)

    return tsub + ((tsol - tsub) / (0.01 - 0.001)) * (metallicity - 0.001)


def interpolated_time(*,
                      mass: float,
                      model_masses: np.ndarray,
                      model_times: np.ndarray) -> float:
    index = np.searchsorted(model_masses, mass)

    pen = ((model_times[index] - model_times[index - 1])
           / (model_masses[index] - model_masses[index - 1]))
    return pen * mass + (model_masses[index] - pen * model_masses[index])


def get_white_dwarf_masses(progenitor_masses: pd.Series) -> np.ndarray:
    masses = np.empty(progenitor_masses.shape[0])

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
