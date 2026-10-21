# SPDX-License-Identifier: GPL-2.0-or-later
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from haltia_camera import takers  # noqa: E402


class Choose(unittest.TestCase):
    def test_only_programs_with_a_label(self):
        found = [("paint.desktop", "Раскрасить"), ("viewer.desktop", None),
                 ("editor.desktop", "  ")]
        self.assertEqual(takers.choose(found), [("paint.desktop", "Раскрасить")])

    def test_not_the_camera_itself(self):
        found = [(takers.APP + ".desktop", "Снять"), ("chat.desktop", "Отправить")]
        self.assertEqual([i[0] for i in takers.choose(found)], ["chat.desktop"])

    def test_two_or_three_by_label_each_once(self):
        found = [("d.desktop", "Г"), ("a.desktop", "В"), ("b.desktop", "Б"),
                 ("a.desktop", "В"), ("c.desktop", "А")]
        self.assertEqual([i[1] for i in takers.choose(found)], ["А", "Б", "В"])

    def test_keeps_what_follows(self):
        info = object()
        self.assertIs(takers.choose([("p.desktop", "Раскрасить", info)])[0][2], info)


class Parse(unittest.TestCase):
    def test_take_photo(self):
        self.assertEqual(takers.parse(["haltia-camera", "--take-photo"]),
                         (True, ["haltia-camera"]))

    def test_by_itself(self):
        self.assertEqual(takers.parse(["haltia-camera"]), (False, ["haltia-camera"]))
        self.assertEqual(takers.parse(["haltia-camera", "--help"]),
                         (False, ["haltia-camera", "--help"]))


if __name__ == "__main__":
    unittest.main()
