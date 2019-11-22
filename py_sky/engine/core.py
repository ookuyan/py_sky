#!/usr/bin/env python

__all__ = ['render', 'show', 'set_scene']

import numpy as np

from ..vec3 import Vec3
from .helper import intersect, show, set_scene


class RayType:
    kUnknownRay, kCameraRay, kShadowRay = range(3)


class Ray:
    def __init__(self, orig, direction):
        self.orig = orig
        self.direction = direction
        self.tmin = 0
        self.tmax = 1.e24
        self.type = RayType.kUnknownRay

    def __call__(self, t):
        return self.orig + self.direction * t


class Atmosphere:
    def __init__(self, sd=Vec3(0., 1., 0.), re=6360.e3,
                 ra=6420.e3, hr=7994., hm=1200.):

        self.sundir = sd
        self.radiusEarth = re
        self.radiusAtmosphere = ra
        self.Hr = hr
        self.Hm = hm

        # For Mars
        # self.sundir = sd
        # self.radiusEarth = 3389.5e3
        # self.radiusAtmosphere = 3396.2e3
        # self.Hr = hr
        # self.Hm = hm

        # Rayleigh scattering coefficients at sea level (for Earth)
        # 440 nm, 550 nm, 680 nm
        self.betaR = Vec3(3.8e-6, 13.5e-6, 33.1e-6)

        # Rayleigh scattering coefficients (for Mars)
        # 440 nm, 550 nm, 680 nm
        # self.betaR = Vec3(5.75e-3, 13.57e-3, 19.918e-3)

        # Mie scattering coefficient at sea level (for Earth)
        self.betaM = Vec3(21.e-6)

    def compute_incident_light(self, r):
        t0 = self.radiusEarth + 1
        t1 = 0

        t = [t0, t1]

        if (not intersect(r, self.radiusAtmosphere, t)) or (t1 < 0.):
            return Vec3(0)

        t0, t1 = t

        if (t0 > r.tmin) and (t0 > 0):
            r.tmin = t0

        if t1 < r.tmax:
            r.tmax = t1

        numSamples = 16.
        numSamplesLight = 16.

        segmentLength = (r.tmax - r.tmin) / numSamples
        tCurrent = r.tmin

        sumR = Vec3(0.)
        sumM = Vec3(0.)

        opticalDepthR = 0
        opticalDepthM = 0

        mu = r.direction.dot(self.sundir)

        # Anisotropy of the medium (aerosol)
        # if g = 0, function is equal to rayleigh
        g = 0.76

        phaseR = 3. / (16. * np.pi) * (mu * mu + 1.)
        phaseM = 3. / (8. * np.pi) * \
                 ((1. - g * g) * (1. + mu * mu)) / \
                 ((2. + g * g) * np.power(1. + g * g - 2. * g * mu, 1.5))

        for i in np.arange(numSamples):
            samplePosition = r(tCurrent + segmentLength * 0.5)
            height = samplePosition.length() - self.radiusEarth

            hr = segmentLength * np.exp(-height / self.Hr)
            hm = segmentLength * np.exp(-height / self.Hm)

            opticalDepthR += hr
            opticalDepthM += hm

            lightRay = Ray(samplePosition, self.sundir)
            l = [lightRay.tmin, lightRay.tmax]
            intersect(lightRay, self.radiusAtmosphere, l)
            lightRay.tmin, lightRay.tmax = l

            segmentLengthLight = lightRay.tmax / numSamplesLight

            tCurrentLight = 0
            opticalDepthLightR = 0
            opticalDepthLightM = 0

            for j in np.arange(numSamplesLight):
                samplePositionLight = \
                    lightRay(tCurrentLight + segmentLengthLight * 0.5)
                heightLight = samplePositionLight.length() - self.radiusEarth

                if heightLight < 0.:
                    break

                opticalDepthLightR += \
                    segmentLengthLight * np.exp(-heightLight / self.Hr)
                opticalDepthLightM += \
                    segmentLengthLight * np.exp(-heightLight / self.Hm)

                tCurrentLight += segmentLengthLight

            if numSamplesLight == (j + 1.):
                tau = self.betaR * (opticalDepthR + opticalDepthLightR) + \
                      self.betaM * 1.1 * (opticalDepthM + opticalDepthLightM)

                attenuation = Vec3(np.exp(-tau.vec[0]),
                                   np.exp(-tau.vec[1]),
                                   np.exp(-tau.vec[2]))

                sumR = sumR + attenuation * hr
                sumM = sumM + attenuation * hm

            tCurrent += segmentLength

        # 20 is a magic number :)
        # For Mars, 20e25
        return (sumR * self.betaR * phaseR + sumM * self.betaM * phaseM) * 20.


def render(scene):
    sun_direction, window = scene
    width, height = window

    atmosphere = Atmosphere(sun_direction)

    r = np.zeros(width * height).reshape((width, height))
    g = np.zeros(width * height).reshape((width, height))
    b = np.zeros(width * height).reshape((width, height))

    origin = Vec3(0., atmosphere.radiusEarth + 1., 0.)

    for j in np.arange(height):
        y = (j + 0.5) * 2. / (height - 1.) - 1.

        for i in np.arange(width):
            x = (i + 0.5) * 2. / (width - 1.) - 1.
            z2 = x * x + y * y

            if z2 <= 1.:
                phi = np.arctan2(y, x)
                theta = np.arccos(1. - z2)

                direction = Vec3(np.sin(theta) * np.cos(phi),
                                 np.cos(theta),
                                 np.sin(theta) * np.sin(phi))

                ray = Ray(origin, direction)
                flux = atmosphere.compute_incident_light(ray)

                r[i][j] = flux.vec[0]
                g[i][j] = flux.vec[1]
                b[i][j] = flux.vec[2]

    data = np.zeros((width, height, 3))
    data[..., 0] = r
    data[..., 1] = g
    data[..., 2] = b

    return data
