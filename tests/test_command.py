# SPDX-License-Identifier: GPL-2.0-or-later
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from haltia_camera import command  # noqa: E402


class Parse(unittest.TestCase):
    def test_take_photo(self):
        self.assertEqual(command.parse(["haltia-camera", "--take-photo"]),
                         (True, ["haltia-camera"]))

    def test_by_itself(self):
        self.assertEqual(command.parse(["haltia-camera"]), (False, ["haltia-camera"]))
        self.assertEqual(command.parse(["haltia-camera", "--help"]),
                         (False, ["haltia-camera", "--help"]))


if __name__ == "__main__":
    unittest.main()
