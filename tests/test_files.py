# SPDX-License-Identifier: GPL-2.0-or-later
"""The release files agree: NEWS.md, the metainfo, the APKBUILD and the
.desktop file the kit runs with --take-photo."""
import configparser
import os
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID = "io.github.haltia_de.Camera"


def read(*path):
    with open(os.path.join(ROOT, *path), encoding="utf-8") as f:
        return f.read()


class Files(unittest.TestCase):
    def test_versions_agree(self):
        news = re.search(r"^##\s+(\S+)\s+\((\d{4}-\d\d-\d\d)\)",
                         read("NEWS.md"), re.M).groups()
        release = ET.fromstring(read("data", ID + ".metainfo.xml").encode()) \
            .find("releases/release")
        self.assertEqual((release.get("version"), release.get("date")), news)
        apk = re.search(r"^pkgver=(\S+)$",
                        read("packaging", "alpine", "APKBUILD"), re.M).group(1)
        self.assertEqual(apk, news[0])

    def test_desktop_entry(self):
        entry = configparser.ConfigParser(interpolation=None)
        entry.optionxform = str
        entry.read_string(read("data", ID + ".desktop"))
        main = entry["Desktop Entry"]
        # take_photo() appends --take-photo to Exec, without field codes.
        self.assertEqual(main["Exec"], "haltia-camera")
        self.assertEqual(main["Icon"], ID)
        self.assertEqual(main["X-Haltia-Home"], "true")
        self.assertNotIn("X-B8K-Home", main)


if __name__ == "__main__":
    unittest.main()
