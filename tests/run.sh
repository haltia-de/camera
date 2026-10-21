#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later
# The tests: sh tests/run.sh (standard library; the photo test needs
# GStreamer and haltia_kit.camera and is skipped without them).
set -eu
cd "$(dirname "$0")/.."
python3 -m py_compile haltia-camera haltia_camera/*.py
python3 -m unittest discover -s tests "$@"
