#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later
# Install haltia-camera (Камера): sh install.sh [ROOT] [PREFIX]
# ROOT empty or / for this system; PREFIX /usr/local unless given (a
# package passes /usr). It needs Python 3 with PyGObject (GTK 3),
# GStreamer with gst-plugins-base and gst-plugins-good, and haltia-kit
# with haltia_kit.camera and haltia_kit.share (github.com/haltia-de/kit). The .desktop file
# shows it in any desktop's launcher; the Haltia tablet shell puts it on
# its home screen (X-B8K-Home).
set -eu
root=${1:-}
root=${root%/}
prefix=${2:-/usr/local}
here=$(cd "$(dirname "$0")" && pwd)
share=$root$prefix/share
id=io.github.haltia_de.Camera
install -D -m 755 "$here/haltia-camera" "$root$prefix/bin/haltia-camera"
install -D -m 644 "$here/data/$id.desktop" "$share/applications/$id.desktop"
install -D -m 644 "$here/data/$id.svg" "$share/icons/hicolor/scalable/apps/$id.svg"
install -D -m 644 "$here/data/$id.metainfo.xml" "$share/metainfo/$id.metainfo.xml"
# The program's own modules (haltia_camera/).
rm -rf "$root$prefix/lib/haltia-camera/haltia_camera"
install -d -m 755 "$root$prefix/lib/haltia-camera/haltia_camera"
install -m 644 "$here"/haltia_camera/*.py "$root$prefix/lib/haltia-camera/haltia_camera/"
