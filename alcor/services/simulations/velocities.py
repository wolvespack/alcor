from collections import namedtuple
from functools import partial
from typing import Tuple

import numpy as np
import pandas as pd

from alcor.models.star import GalacticDiskType
from alcor.types import GaussianGeneratorType

VelocityVector = namedtuple('VelocityVector', ['u', 'v', 'w'])


def set_velocities(stars: pd.DataFrame,
                   *,
                   thin_disk_velocity_std: VelocityVector = VelocityVector(
                           u=32.4, v=23., w=18.1),
                   thick_disk_velocity_std: VelocityVector = VelocityVector(
                           u=50., v=56., w=34.),
                   peculiar_solar_velocity: VelocityVector = VelocityVector(
                           u=-11., v=-12., w=-7.),
                   solar_galactocentric_distance: float,
                   oort_constant_a: float,
                   oort_constant_b: float,
                   generator: GaussianGeneratorType = np.random.normal
                   ) -> None:
    thin_disk_stars_mask = (stars['galactic_disk_type']
                            == GalacticDiskType.thin)
    thick_disk_stars_mask = (stars['galactic_disk_type']
                             == GalacticDiskType.thick)

    stars_velocities = partial(
            disk_stars_velocities,
            peculiar_solar_velocity=peculiar_solar_velocity,
            solar_galactocentric_distance=solar_galactocentric_distance,
            oort_constant_a=oort_constant_a,
            oort_constant_b=oort_constant_b,
            generator=generator)

    (stars.loc[thin_disk_stars_mask, 'u_velocity'],
     stars.loc[thin_disk_stars_mask, 'v_velocity'],
     stars.loc[thin_disk_stars_mask, 'w_velocity']) = stars_velocities(
            r_cylindrical=stars.loc[thin_disk_stars_mask, 'r_cylindrical'],
            thetas_cylindrical=stars.loc[thin_disk_stars_mask,
                                         'theta_cylindrical'],
            velocity_dispersion=thin_disk_velocity_std)
    (stars.loc[thick_disk_stars_mask, 'u_velocity'],
     stars.loc[thick_disk_stars_mask, 'v_velocity'],
     stars.loc[thick_disk_stars_mask, 'w_velocity']) = stars_velocities(
            r_cylindrical=stars.loc[thick_disk_stars_mask, 'r_cylindrical'],
            thetas_cylindrical=stars.loc[thick_disk_stars_mask,
                                         'theta_cylindrical'],
            velocity_dispersion=thick_disk_velocity_std)


def disk_stars(*,
               stars: pd.DataFrame,
               disk_type: GalacticDiskType) -> pd.DataFrame:
    mask = stars['galactic_disk_type'] == disk_type
    return stars[mask]


def disk_stars_velocities(*,
                          r_cylindrical: np.ndarray,
                          thetas_cylindrical: np.ndarray,
                          peculiar_solar_velocity: VelocityVector,
                          solar_galactocentric_distance: float,
                          oort_constant_a: float,
                          oort_constant_b: float,
                          velocity_dispersion: VelocityVector,
                          generator: GaussianGeneratorType
                          ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    # TODO: find out what it means
    uops = (peculiar_solar_velocity.u
            + ((3. - (2. * r_cylindrical) / solar_galactocentric_distance)
               * oort_constant_a - oort_constant_b) * r_cylindrical
            * np.sin(thetas_cylindrical))
    vops = (peculiar_solar_velocity.v
            + ((3. - (2. * r_cylindrical) / solar_galactocentric_distance)
               * oort_constant_a - oort_constant_b) * r_cylindrical
            * np.cos(thetas_cylindrical)
            - (oort_constant_a - oort_constant_b)
            * solar_galactocentric_distance)

    stars_count = r_cylindrical.size

    u_velocities = (velocity_dispersion.u * generator(size=stars_count)
                    + uops)
    # TODO: what is this 120.?
    v_velocities = (velocity_dispersion.v * generator(size=stars_count)
                    + vops - velocity_dispersion.u ** 2 / 120.)
    w_velocities = (velocity_dispersion.w * generator(size=stars_count)
                    + peculiar_solar_velocity.w)

    return u_velocities, v_velocities, w_velocities


# TODO: find out what is going on here
def halo_stars_velocities(*,
                          galactic_longitudes: np.ndarray,
                          thetas_cylindrical: np.ndarray,
                          peculiar_solar_velocity: VelocityVector,
                          lsr_velocity: float,
                          spherical_velocity_component_sigma: float,
                          generator: GaussianGeneratorType
                          ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    More details at: "Simulating Gaia performances on white dwarfs" by S.Torres
    """
    stars_count = galactic_longitudes.size

    r_spherical_velocities = (spherical_velocity_component_sigma
                              * generator(size=stars_count))
    theta_spherical_velocities = (spherical_velocity_component_sigma
                                  * generator(size=stars_count))
    phi_spherical_velocities = (spherical_velocity_component_sigma
                                * generator(size=stars_count))

    deltas = np.pi - galactic_longitudes - thetas_cylindrical

    x_velocities, y_velocities = rotate_vectors(
            x_values=r_spherical_velocities,
            y_values=phi_spherical_velocities,
            angles=deltas)
    x_velocities = -x_velocities  # TODO: why minus?
    z_velocities = theta_spherical_velocities

    v_velocities, u_velocities = rotate_vectors(x_values=x_velocities,
                                                y_values=z_velocities,
                                                angles=galactic_longitudes)
    w_velocities = y_velocities

    u_velocities += peculiar_solar_velocity.u
    v_velocities += peculiar_solar_velocity.v - lsr_velocity
    w_velocities += peculiar_solar_velocity.w

    return u_velocities, v_velocities, w_velocities


def rotate_vectors(*,
                   x_values: np.ndarray,
                   y_values: np.ndarray,
                   angles: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    sin_angles = np.sin(angles)
    cos_angles = np.cos(angles)

    rotated_x_values = cos_angles * x_values - sin_angles * y_values
    rotated_y_values = sin_angles * x_values + cos_angles * y_values

    return rotated_x_values, rotated_y_values