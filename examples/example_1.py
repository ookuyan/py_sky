#!/usr/bin/env python

from py_sky import render, show, set_scene


def main():
    scene = set_scene(zenith=45, azimuth=180, width=32, height=32)

    rgb = render(scene)

    show(rgb)


if __name__ == '__main__':
    main()
