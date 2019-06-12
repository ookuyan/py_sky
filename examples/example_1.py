#!/usr/bin/env python

from engine import render, show, position_of_sun


def main():
    height, width = 32, 32

    sun_direction = position_of_sun(30, 180)

    rgb = render(sun_direction, height, width)

    show(rgb)


if __name__ == '__main__':
    main()
