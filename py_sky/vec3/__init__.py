#!/usr/bin/env python

__all__ = ['Vec3']

import numpy as np


class Vec3:
    """
    A 3d Vector library based on 'numpy'

    Parameters
    ----------
    x : float
        x coordinate.

    y : float or optional
        y coordinate.

    z : float or optional
        z coordinate.

    Returns
    -------

    Vec3 object

    Examples
    --------

    >>> from vec3 import Vec3
    >>>
    >>> v = Vec3(1., 2., 3.)
    >>> w = Vec3(4., 3., -3.)
    >>>
    >>> a = (v * w - 7.) / Vec3(3., 2., 1.)
    >>>
    >>> a += Vec3(0., 1., 0.)
    >>>
    >>> print(a)
    [-1.0, -0.5, -16.0]
    """

    def __init__(self, x=0., y=None, z=None):
        if isinstance(x, self.__class__):
            self.vec = np.array([x.vec[0], x.vec[1], x.vec[2]])
        else:
            if (y is None) and (z is None):
                self.vec = np.array([x, x, x])
            else:
                self.vec = np.array([x, y, z])

    def length(self):
        _len = self.vec[0] * self.vec[0] + \
               self.vec[1] * self.vec[1] + \
               self.vec[2] * self.vec[2]

        return np.sqrt(_len)

    def max(self):
        return max(self.vec[0], max(self.vec[1], self.vec[2]))

    def dot(self, v):
        return v.vec[0] * self.vec[0] + \
               v.vec[1] * self.vec[1] + \
               v.vec[2] * self.vec[2]

    def normalize(self):
        length = self.vec[0] * self.vec[0] + \
                 self.vec[1] * self.vec[1] + \
                 self.vec[2] * self.vec[2]

        if length > 0:
            inv_length = 1 / np.sqrt(length)

            self.vec[0] *= inv_length
            self.vec[1] *= inv_length
            self.vec[2] *= inv_length

        return self.vec

    def __str__(self):
        return '[{0}, {1}, {2}]'.format(self.vec[0], self.vec[1], self.vec[2])

    def __repr__(self):
        return '[{0}, {1}, {2}]'.format(self.vec[0], self.vec[1], self.vec[2])

    def __getitem__(self, i):
        return self.vec[i]

    def __setitem__(self, i, value):
        self.vec[i] = value

    def __neg__(self):
        return Vec3(-self.vec[0], -self.vec[1], self.vec[2])

    def __sub__(self, x):
        if isinstance(x, self.__class__):
            return Vec3(self.vec[0] - x.vec[0],
                        self.vec[1] - x.vec[1],
                        self.vec[2] - x.vec[2])
        else:
            return Vec3(self.vec[0] - x, self.vec[1] - x, self.vec[2] - x)

    def __add__(self, x):
        if isinstance(x, self.__class__):
            return Vec3(self.vec[0] + x.vec[0],
                        self.vec[1] + x.vec[1],
                        self.vec[2] + x.vec[2])
        else:
            return Vec3(self.vec[0] + x,
                        self.vec[1] + x,
                        self.vec[2] + x)

    def __truediv__(self, x):  # __div__
        if isinstance(x, self.__class__):
            return Vec3(self.vec[0] / x.vec[0],
                        self.vec[1] / x.vec[1],
                        self.vec[2] / x.vec[2])
        else:
            r_inv = 1. / x
            return Vec3(self.vec[0] * r_inv,
                        self.vec[1] * r_inv,
                        self.vec[2] * r_inv)

    def __mul__(self, x):
        if isinstance(x, self.__class__):
            return Vec3(self.vec[0] * x.vec[0],
                        self.vec[1] * x.vec[1],
                        self.vec[2] * x.vec[2])
        else:
            return Vec3(self.vec[0] * x,
                        self.vec[1] * x,
                        self.vec[2] * x)

    def __iadd__(self, x):
        if isinstance(x, self.__class__):
            self.vec[0] += x.vec[0]
            self.vec[1] += x.vec[1]
            self.vec[2] += x.vec[2]
        else:
            self.vec[0] += x
            self.vec[1] += x
            self.vec[2] += x

        return self.vec

    def __imul__(self, x):
        if isinstance(x, self.__class__):
            self.vec[0] *= x.vec[0]
            self.vec[1] *= x.vec[1]
            self.vec[2] *= x.vec[2]
        else:
            self.vec[0] *= x
            self.vec[1] *= x
            self.vec[2] *= x

        return self.vec
