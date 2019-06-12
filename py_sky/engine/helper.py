#!/usr/bin/env python

__all__ = ['solve_quadratic', 'intersect', 'show', 'position_of_sun']

import numpy as np
import matplotlib.pyplot as plt

from ..vec3 import Vec3


def position_of_sun(zenith, azimuth):
    zenith = np.deg2rad(zenith)
    azimuth = np.deg2rad(azimuth)

    sun_direction = Vec3(np.sin(zenith) * np.sin(azimuth),
                         np.cos(zenith),
                         -np.sin(zenith) * np.cos(azimuth))

    return sun_direction


def solve_quadratic(a, b, c, x):
    if b == 0:
        if a == 0.:
            return False

        x[0] = 0.
        x[1] = np.sqrt(-c / a)

        return True

    discr = b * b - 4 * a * c

    if discr < 0.:
        return False

    if b < 0.:
        q = -0.5 * (b - np.sqrt(discr))
    else:
        q = -0.5 * (b + np.sqrt(discr))

    x[0] = q / a
    x[1] = c / q

    return True


def intersect(r, radius, t):
    vec = r.orig

    a = r.direction.vec[0] * r.direction.vec[0] + \
        r.direction.vec[1] * r.direction.vec[1] + \
        r.direction.vec[2] * r.direction.vec[2]

    b = (r.direction.vec[0] * vec.vec[0] +
         r.direction.vec[1] * vec.vec[1] +
         r.direction.vec[2] * vec.vec[2]) * 2.

    c = vec.vec[0] * vec.vec[0] + \
        vec.vec[1] * vec.vec[1] + \
        vec.vec[2] * vec.vec[2] - \
        radius * radius

    if not solve_quadratic(a, b, c, t):
        return False

    t0, t1 = t

    if t0 > t1:
        t[0], t[1] = t[1], t[0]

    return True


def show(rgb, save=False, grid=False, filename='sky.png'):
    r, g, b = rgb

    img = np.zeros((r.shape[0], r.shape[1], 3), dtype=float)
    img[:, :, 0] = r
    img[:, :, 1] = g
    img[:, :, 2] = b

    if grid:
        plt.grid()
    plt.imshow(img, aspect='equal', interpolation=None, origin='upper')

    if save:
        plt.savefig(filename)

    plt.show()
