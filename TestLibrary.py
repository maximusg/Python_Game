import unittest
import pygame
import math
import copy
import os

import library

class TestLibrary(unittest.TestCase):
    def test_load_text(self):
        filename = 'resources/event_scrolls/credits.asset'
        with open(filename) as f:
            expected = f.readlines()
        result = library.load_text(filename)
        self.assertEqual(result, expected)

        filename = 'thisfiledoesnotexist.asset'
        flag = False
        try:
            result = library.load_text(filename)
        except FileNotFoundError as fnfe:
            flag = True
        finally:
            self.assertTrue(flag)

        filename = None
        flag = False
        try:
            result = library.load_text(filename)
        except TypeError as te:
            flag = True
        finally:
            self.assertTrue(flag)

    def test_load_sound(self):
        pass

    def test_load_background_music(self):
        pass

    def test_load_image(self):
        pass

    def test_draw_text(self):
        pass

    def test_draw_vertical_bar(self):
        pass

    def test_draw_boss_bar(self):
        pass

    def test_draw_player_lives(self):
        pass
    
    def test_draw_bombs_remaining(self):
        pass

    def test_draw_button(self):
        pass

if __name__ == "__main__":
    unittest.main(exit=False)