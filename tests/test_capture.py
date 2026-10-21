# SPDX-License-Identifier: GPL-2.0-or-later
"""A photo from GStreamer's videotestsrc, the source HALTIA_CAMERA_SOURCE
gives the program; skipped without GStreamer or haltia_kit.camera."""
import os
import tempfile
import unittest

try:
    import gi
    gi.require_version("Gst", "1.0")
    from gi.repository import Gst
    from haltia_kit import camera
    Gst.init(None)
    SOURCE = Gst.ElementFactory.find("videotestsrc") is not None
except (ImportError, ValueError, AttributeError):
    SOURCE = False


@unittest.skipUnless(SOURCE, "no GStreamer with videotestsrc, or no haltia_kit.camera")
class Capture(unittest.TestCase):
    def test_photo_is_saved(self):
        def make():
            src = Gst.ElementFactory.make("videotestsrc")
            src.set_property("is-live", True)
            return src
        with tempfile.TemporaryDirectory() as where:
            path = camera.capture(camera.Camera("videotestsrc", make), where=where)
            self.assertTrue(os.path.isabs(path))
            self.assertEqual(os.path.dirname(path), where)
            with open(path, "rb") as f:
                self.assertEqual(f.read(2), b"\xff\xd8")


if __name__ == "__main__":
    unittest.main()
