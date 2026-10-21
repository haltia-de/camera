# SPDX-License-Identifier: GPL-2.0-or-later
"""The programs that take a photo from the Camera, and the command line.

A program says it takes photos with two lines in its .desktop file:
image/jpeg in MimeType (so it opens a photo given as %f, %F, %u or %U)
and X-Haltia-Photo, the words on its button, translated like Name:

    MimeType=image/jpeg;image/png;
    X-Haltia-Photo=Colour in
    X-Haltia-Photo[ru]=Раскрасить

A program without the key is not offered, even if it opens JPEG files:
an image viewer or editor is not something a photo is «sent» to.
"""

APP = "io.github.haltia_de.Camera"
KEY = "X-Haltia-Photo"
MIME = "image/jpeg"
# Two or three big buttons, not a list to read through.
MOST = 3
TAKE = "--take-photo"


def choose(found, own=APP + ".desktop", most=MOST):
    """The programs to offer from found, (desktop id, label, ...) tuples:
    those with a label, not the Camera itself, each once, by label."""
    seen, out = set(), []
    for item in found:
        app_id, label = item[0], (item[1] or "").strip()
        if not label or app_id == own or app_id in seen:
            continue
        seen.add(app_id)
        out.append((app_id, label) + tuple(item[2:]))
    out.sort(key=lambda item: (item[1].casefold(), item[0]))
    return out[:most]


def parse(argv):
    """(take, argv): whether a program asks for a photo (--take-photo),
    and the arguments left for GApplication."""
    rest = [a for a in argv[1:] if a != TAKE]
    return len(rest) < len(argv) - 1, argv[:1] + rest
