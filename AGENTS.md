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
  element later) and haltia-kit with `haltia_kit.camera` and
  `haltia_kit.share` (after kit 2.2.0; until they are released, test
  against kit main).
- Folders come from GLib via `haltia_kit.camera` (`<Pictures>/Камера`),
  never from `~`.

## Layout

- `haltia-camera`: the GTK program (pages: viewfinder, photo, send).
- `haltia_camera/command.py`: no screen: the app id and the command line.
- `data/`: the .desktop file, icon and AppStream metainfo.
- `packaging/alpine/APKBUILD`; Flatpak comes later.
- Installed (`sh install.sh [ROOT] [PREFIX]`): Python never caches the
  script it is started by, so the code of `haltia-camera` goes in as the
  module `lib/haltia-camera/haltia_camera_main.py`, beside `haltia_camera/`
  and compiled with it by the package build (haltia-de/ci), and
  `bin/haltia-camera` is a stub that runs it with
  `runpy.run_module(..., run_name="__main__", alter_sys=False)`: `sys.argv`
  and the `python3 /usr/bin/haltia-camera` command line stay. `__file__` is
  then that module, so the program finds `haltia_camera/` beside itself
  either way. The checkout keeps the script, which the tests load by path.

## A photo for a program

The contract in kit's AGENTS.md: `haltia-camera --take-photo` is its own
instance (`Gio.ApplicationFlags.NON_UNIQUE`) and never forwards to an open
one; if the open one holds the camera, the new one shows the busy state.
«Готово» prints the photo's absolute path as the last stdout line and
exits 0; closing or «Отмена» exits 0 with no path. Nothing else may be
printed after the path.

## Sending a photo

Opened by itself, «Готово» shows «Фото сохранено» with «Отправить» and
«Снять ещё». «Отправить» calls `haltia_kit.share.send(path, window)`: the
kit's dialog finds the receivers (`X-Haltia-Share=true` and `image/jpeg`
in `MimeType`), starts the one tapped with the photo, or says there is
nowhere to send it. The Camera keeps no list of programs and reads no
.desktop key of its own.

## Busy camera

A busy camera (`haltia_kit.camera.BUSY`, in practice a call) shows only
«Камера занята звонком», no buttons, and is tried again after 3 seconds,
then each time twice as late, up to 12 (`Viewfinder.pause()`/`resume()`:
the kit opens the camera on its thread, never in the window's). When
`--take-photo` finds the camera held by the open Camera (its name is
owned on the session bus), it says «Камера уже открыта» instead.

The camera is held only while the window is active (`is-active`): in the
background the viewfinder is paused, so a call can have the camera.

A still that failed (`haltia_kit.camera.FAILED`) says «Не получилось,
попробуйте ещё раз» over the viewfinder with the shot buttons back.

## Conventions

- Source files carry an SPDX line and LF line endings.
- Each release is described in `NEWS.md` (Русский, then English); the
  version in NEWS.md, the metainfo and the APKBUILD agree (a test checks).
