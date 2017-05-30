import csv

from bokeh.layouts import column
from bokeh.plotting import (figure,
                            output_file,
                            show)


def plot() -> None:
    output_file("velocities_vs_magnitude.html")

    with open('uvw_vs_mag_bins.csv', 'r') as file:
        reader = csv.reader(file,
                            delimiter=' ')

        header_row = next(reader)

        rows = (map(float, row) for row in reader)
        (average_bin_magnitude,
            average_velocity_u,
            average_velocity_v,
            average_velocity_w,
            velocity_u_std,
            velocity_v_std,
            velocity_w_std) = zip(*rows)

    top_plot = figure(width=500, height=250)
    top_plot.line(average_bin_magnitude,
                  average_velocity_u)
    top_plot.square(average_bin_magnitude,
                    average_velocity_u)

    middle_plot = figure(width=500, height=250)
    middle_plot.line(average_bin_magnitude,
                     average_velocity_v)
    middle_plot.square(average_bin_magnitude,
                       average_velocity_v)

    bottom_plot = figure(width=500, height=250)
    bottom_plot.line(average_bin_magnitude,
                     average_velocity_w)
    bottom_plot.square(average_bin_magnitude,
                       average_velocity_w)

    multiline_x = []
    multiline_y_u = []
    multiline_y_v = []
    multiline_y_w = []

    for (magnitude,
         velocity_u, velocity_v, velocity_w,
         std_u, std_v, std_w) in zip(average_bin_magnitude,
                                     average_velocity_u,
                                     average_velocity_v,
                                     average_velocity_w,
                                     velocity_u_std,
                                     velocity_v_std,
                                     velocity_w_std):
        multiline_x.append((magnitude,
                            magnitude))
        multiline_y_u.append((velocity_u - std_u,
                              velocity_u + std_u))
        multiline_y_v.append((velocity_v - std_v,
                              velocity_v + std_v))
        multiline_y_w.append((velocity_w - std_w,
                              velocity_w + std_w))

    top_plot.multi_line(multiline_x,
                        multiline_y_u)
    middle_plot.multi_line(multiline_x,
                           multiline_y_v)
    bottom_plot.multi_line(multiline_x,
                           multiline_y_w)

    with open('uvw_vs_mag_cloud.csv', 'r') as file:
        reader = csv.reader(file,
                            delimiter=' ')

        header_row = next(reader)

        rows = (map(float, row) for row in reader)
        (bolometric_magnitude,
            velocity_u,
            velocity_v,
            velocity_w) = zip(*rows)

    top_plot.circle(bolometric_magnitude,
                    velocity_u,
                    size=1)
    middle_plot.circle(bolometric_magnitude,
                       velocity_v,
                       size=1)
    bottom_plot.circle(bolometric_magnitude,
                       velocity_w,
                       size=1)

    show(column(top_plot,
                middle_plot,
                bottom_plot))


def plot_lepine_case():
    output_file("velocities_vs_magnitude.html")

    with open('u_vs_mag_bins.csv', 'r') as file:
        reader = csv.reader(file,
                            delimiter=' ')
        header_row = next(reader)
        rows = (map(float, row) for row in reader)
        (average_bin_magnitude_u,
            average_velocity_u,
            velocity_u_std) = zip(*rows)

    with open('v_vs_mag_bins.csv', 'r') as file:
        reader = csv.reader(file,
                            delimiter=' ')
        header_row = next(reader)
        rows = (map(float, row) for row in reader)
        (average_bin_magnitude_v,
            average_velocity_v,
            velocity_v_std) = zip(*rows)

    with open('w_vs_mag_bins.csv', 'r') as file:
        reader = csv.reader(file,
                            delimiter=' ')
        header_row = next(reader)
        rows = (map(float, row) for row in reader)
        (average_bin_magnitude_w,
            average_velocity_w,
            velocity_w_std) = zip(*rows)

    top_plot = figure(width=500, height=250)
    top_plot.line(average_bin_magnitude_u,
                  average_velocity_u)
    top_plot.square(average_bin_magnitude_u,
                    average_velocity_u)

    middle_plot = figure(width=500, height=250)
    middle_plot.line(average_bin_magnitude_v,
                     average_velocity_v)
    middle_plot.square(average_bin_magnitude_v,
                       average_velocity_v)

    bottom_plot = figure(width=500, height=250)
    bottom_plot.line(average_bin_magnitude_w,
                     average_velocity_w)
    bottom_plot.square(average_bin_magnitude_w,
                       average_velocity_w)

    multiline_x_u = []
    multiline_x_v = []
    multiline_x_w = []
    multiline_y_u = []
    multiline_y_v = []
    multiline_y_w = []

    for (magnitude_u, magnitude_v, magnitude_w,
         velocity_u, velocity_v, velocity_w,
         std_u, std_v, std_w) in zip(average_bin_magnitude_u,
                                     average_bin_magnitude_v,
                                     average_bin_magnitude_w,
                                     average_velocity_u,
                                     average_velocity_v,
                                     average_velocity_w,
                                     velocity_u_std,
                                     velocity_v_std,
                                     velocity_w_std):
        multiline_x_u.append((magnitude_u,
                              magnitude_u))
        multiline_x_v.append((magnitude_v,
                              magnitude_v))
        multiline_x_w.append((magnitude_w,
                              magnitude_w))
        multiline_y_u.append((velocity_u - std_u,
                              velocity_u + std_u))
        multiline_y_v.append((velocity_v - std_v,
                              velocity_v + std_v))
        multiline_y_w.append((velocity_w - std_w,
                              velocity_w + std_w))

    top_plot.multi_line(multiline_x_u,
                        multiline_y_u)
    middle_plot.multi_line(multiline_x_v,
                           multiline_y_v)
    bottom_plot.multi_line(multiline_x_w,
                           multiline_y_w)

    with open('u_vs_mag_cloud.csv', 'r') as file:
        reader = csv.reader(file,
                            delimiter=' ')
        header_row = next(reader)
        rows = (map(float, row) for row in reader)
        (bolometric_magnitude,
            velocity_u) = zip(*rows)

    with open('v_vs_mag_cloud.csv', 'r') as file:
        reader = csv.reader(file,
                            delimiter=' ')
        header_row = next(reader)
        rows = (map(float, row) for row in reader)
        (bolometric_magnitude,
            velocity_v) = zip(*rows)

    with open('w_vs_mag_cloud.csv', 'r') as file:
        reader = csv.reader(file,
                            delimiter=' ')
        header_row = next(reader)
        rows = (map(float, row) for row in reader)
        (bolometric_magnitude,
            velocity_w) = zip(*rows)

    top_plot.circle(bolometric_magnitude,
                    velocity_u,
                    size=1)
    middle_plot.circle(bolometric_magnitude,
                       velocity_v,
                       size=1)
    bottom_plot.circle(bolometric_magnitude,
                       velocity_w,
                       size=1)

    show(column(top_plot,
                middle_plot,
                bottom_plot))