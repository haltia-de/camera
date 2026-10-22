# SPDX-License-Identifier: GPL-2.0-or-later
"""The window's choices without a screen: a failed still offers the shot
again, a busy camera is tried again ever later, «Отправить» hands the
photo to haltia_kit.share. Skipped without GTK, haltia_kit.camera or
haltia_kit.share."""
import importlib.machinery
import importlib.util
import os
import types
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    loader = importlib.machinery.SourceFileLoader(
        "haltia_camera_app", os.path.join(ROOT, "haltia-camera"))
    app = importlib.util.module_from_spec(
        importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(app)
except (ImportError, ValueError, AttributeError):
    app = None


class Widget:
    def __init__(self):
        self.visible = self.sensitive = None

    def set_visible(self, visible):
        self.visible = visible

    def set_sensitive(self, sensitive):
        self.sensitive = sensitive

    def set_text(self, text):
        pass


def window(**kw):
    win = types.SimpleNamespace(
        take=False, failed=False, counting=0, retry=1, wait=3, away=False,
        busy=Widget(), buttons=Widget(), shoot=Widget(), later=Widget(),
        note=Widget(), stop_count=lambda: None)
    win.__dict__.update(kw)
    return win


@unittest.skipUnless(app, "no GTK 3, haltia_kit.camera or haltia_kit.share")
class Window(unittest.TestCase):
    def test_failed_still_offers_the_shot(self):
        win = window(failed=True)
        app.Window.changed(win, app.camera.FAILED)
        self.assertTrue(win.shoot.sensitive)
        self.assertTrue(win.note.visible)
        self.assertTrue(win.buttons.visible)

    def test_camera_that_did_not_start_offers_nothing(self):
        win = window()
        app.Window.changed(win, app.camera.FAILED)
        self.assertFalse(win.shoot.sensitive)
        self.assertFalse(win.note.visible)

    def test_busy_is_tried_ever_later(self):
        calls = []
        view = types.SimpleNamespace(state=app.camera.BUSY,
                                     pause=lambda: calls.append("pause"),
                                     resume=lambda: calls.append("resume"))
        win = window(view=view, retry=0, wait=app.RETRY)
        win.try_again = lambda: False
        waits = []
        for _ in range(4):
            app.Window.try_again(win)
            app.GLib.source_remove(win.retry)
            waits.append(win.wait)
        self.assertEqual(waits, [6, 12, 12, 12])
        self.assertEqual(calls[:2], ["pause", "resume"])

    def test_not_tried_in_the_background(self):
        view = types.SimpleNamespace(state=app.camera.BUSY)
        win = window(view=view, retry=0, away=True)
        self.assertFalse(app.Window.try_again(win))
        self.assertEqual(win.retry, 0)

    def test_send_gives_the_photo_to_the_kit(self):
        sent = []
        win = window(path="/p/Камера/photo.jpg", win=object())
        real = app.share.send
        app.share.send = lambda path, parent=None: sent.append((path, parent))
        try:
            app.Window.send(win)
        finally:
            app.share.send = real
        self.assertEqual(sent, [("/p/Камера/photo.jpg", win.win)])


if __name__ == "__main__":
    unittest.main()
