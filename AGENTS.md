# haltia-camera

Камера: a calm camera for an older person's Haltia tablet. A full-screen
viewfinder, one big «Снять» button and «Через 3 секунды»; after the shot,
the photo large with «Ещё раз» and «Готово». No settings, no video, no
camera switch: keep it that way. The UI and README are in Russian; code,
comments, this file and commits are in English.

The shared rules are in haltia-de/haltia's `docs/conventions.md`; this file
adds only what is this repository's own.

## Running and testing

- `sh tests/run.sh`: byte-compiles the program and runs the unit tests
  (standard library). The photo test uses GStreamer's `videotestsrc`
  through `haltia_kit.camera` and is skipped without them.
- `HALTIA_CAMERA_SOURCE=videotestsrc ./haltia-camera` runs it without a
  camera; add `--take-photo` to try what a program gets.
- Needs Python 3, PyGObject with GTK 3, GStreamer (gst-plugins-base for the
  GstVideo typelib, gst-plugins-good for jpegdec and v4l2src; libcamera's
  element later) and haltia-kit with `haltia_kit.camera` (after kit 2.2.0;
  until it is released, test against kit main).
- Folders come from GLib via `haltia_kit.camera` (`<Pictures>/Камера`),
  never from `~`.

## Layout

- `haltia-camera`: the GTK program (pages: viewfinder, photo, programs).
- `haltia_camera/takers.py`: no screen: which programs take a photo, and
  the command line.
- `data/`: the .desktop file, icon and AppStream metainfo.
- `packaging/alpine/APKBUILD`; Flatpak comes later.

## A photo for a program

The contract in kit's AGENTS.md: `haltia-camera --take-photo` is its own
instance (`Gio.ApplicationFlags.NON_UNIQUE`) and never forwards to an open
one; if the open one holds the camera, the new one shows the busy state.
«Готово» prints the photo's absolute path as the last stdout line and
exits 0; closing or «Отмена» exits 0 with no path. Nothing else may be
printed after the path.

## Programs that take a photo

Opened by itself, «Готово» shows up to three big buttons, one per program
whose .desktop file has `image/jpeg` in `MimeType` and the key
`X-Haltia-Photo`, the words on the button (translated like `Name`):

    MimeType=image/jpeg;image/png;
    X-Haltia-Photo=Colour in
    X-Haltia-Photo[ru]=Раскрасить

The program is started with the photo as its file (`%f`/`%F`/`%u`/`%U`)
and the Camera closes. There is no built-in list of programs.

## Busy camera

A busy camera (`haltia_kit.camera.BUSY`, in practice a call) shows only
«Камера занята звонком», no buttons, and is tried again every 3 seconds.
When `--take-photo` finds the camera held by the open Camera (its name is
owned on the session bus), it says «Камера уже открыта» instead.

## Conventions

- Source files carry an SPDX line and LF line endings.
- Each release is described in `NEWS.md` (Русский, then English); the
  version in NEWS.md, the metainfo and the APKBUILD agree (a test checks).
