from math import (sqrt,
                  pi,
                  sin,
                  cos,
                  asin,
                  acos,
                  atan)
from typing import List

from alcor.models.star import Star


# TODO: find out the meaning of parameters
# ngp - North Galactic Pole
def calculate_coordinates(stars: List[Star],
                          solar_galactocentric_distance: float,
                          ngp_declination: float = 0.478,
                          theta: float = 2.147,
                          alphag: float = 3.35
                          ) -> None:
    for star in stars:
        # TODO: give shorter name
        stellar_galactocentric_distance_plane_projection = (
            opposite_triangle_side(solar_galactocentric_distance,
                                   star.r_cylindric_coordinate,
                                   star.th_cylindric_coordinate))
        star.galactic_distance = sqrt(
            stellar_galactocentric_distance_plane_projection ** 2
            + star.z_coordinate ** 2)

        # TODO: implement function
        star.galactic_longitude = acos(
            (solar_galactocentric_distance ** 2
             + stellar_galactocentric_distance_plane_projection ** 2
             - star.r_cylindric_coordinate ** 2)
            / (2. * stellar_galactocentric_distance_plane_projection
               * solar_galactocentric_distance))

        if (star.r_cylindric_coordinate * cos(star.th_cylindric_coordinate)
                > solar_galactocentric_distance):
            star.galactic_longitude = pi - star.galactic_longitude
        elif sin(star.th_cylindric_coordinate) < 0.:
            star.galactic_longitude += 2. * pi

        if star.galactic_longitude > 2. * pi:
            star.galactic_longitude -= 2. * pi

        # TODO: or use arctan2
        star.galactic_latitude = atan(
            abs(star.z_coordinate
                / stellar_galactocentric_distance_plane_projection))

        if star.z_coordinate < 0.:
            star.galactic_latitude = -star.galactic_latitude

        sin_longitude = sin(star.galactic_longitude)
        cos_longitude = cos(star.galactic_longitude)
        sin_latitude = sin(star.galactic_latitude)
        cos_latitude = cos(star.galactic_latitude)

        # TODO: what is this?
        zkri = 1. / (4.74E3 * star.galactic_distance)

        star.proper_motion_component_l = (
            (-zkri * (sin_longitude / cos_latitude) * star.u_velocity)
            + (zkri * (cos_longitude / cos_latitude) * star.v_velocity))
        star.proper_motion_component_b = (
            (-zkri * cos_longitude * sin_latitude * star.u_velocity)
            + (-zkri * sin_latitude * sin_longitude * star.v_velocity)
            + (zkri * cos_latitude * star.w_velocity))
        # TODO: rename as radial velocity
        star.proper_motion_component_vr = (
            (cos_latitude * cos_longitude * star.u_velocity)
            + (cos_latitude * sin_latitude * star.v_velocity)
            + (sin_latitude * star.w_velocity))
        star.proper_motion = sqrt(star.proper_motion_component_l ** 2
                                  + star.proper_motion_component_b ** 2)

        star.declination = (asin(sin(ngp_declination) * sin_latitude
                                 + cos(ngp_declination) * cos_latitude
                                   * cos(theta - star.galactic_longitude)))

        # TODO: what is xs and xc?
        xs = ((cos_latitude * sin(theta - star.galactic_longitude))
              / cos(star.declination))
        xc = ((cos(ngp_declination) * sin_latitude
               - sin(ngp_declination) * cos_latitude
                 * cos(theta - star.galactic_longitude))
              / cos(star.declination))

        if xs >= 0.:
            if xc >= 0.:
                star.right_ascension = asin(xs) + alphag
            else:
                star.right_ascension = acos(xc) + alphag
        else:
            if xc < 0.:
                star.right_ascension = pi - asin(xs) + alphag
            else:
                star.right_ascension = 2. * pi + asin(xs) + alphag

        if star.right_ascension > 2. * pi:
            star.right_ascension -= 2. * pi


def opposite_triangle_side(adjacent: float,
                           other_adjacent: float,
                           enclosed_angle: float) -> float:
    return sqrt(adjacent ** 2 + other_adjacent ** 2
                - 2. * adjacent * other_adjacent * cos(enclosed_angle))
