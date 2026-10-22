# SPDX-License-Identifier: GPL-2.0-or-later
"""The Camera's id and its command line.

Opened by itself, the Camera sends a photo on with haltia_kit.share;
opened with --take-photo (haltia_kit.camera.take_photo()), it gives the
photo's path to the program that asked.
"""

APP = "io.github.haltia_de.Camera"
TAKE = "--take-photo"


def parse(argv):
    """(take, argv): whether a program asks for a photo (--take-photo),
    and the arguments left for GApplication."""
    rest = [a for a in argv[1:] if a != TAKE]
    return len(rest) < len(argv) - 1, argv[:1] + rest
