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

    def test_load_sound(self):
        flag = False
        try:
            sound = library.load_sound(str(library.SOUND_EFFECT_PATH.joinpath('explosion.ogg')))
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        pygame.mixer.init()
        sound = library.load_sound(str(library.SOUND_EFFECT_PATH.joinpath('explosion.ogg')))
        self.assertIsInstance(sound, pygame.mixer.Sound)

        flag = False
        try:
            sound = library.load_sound(str(library.SOUND_EFFECT_PATH.joinpath('thisfiledoesnotexist')))
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        pygame.mixer.quit()

    def test_load_background_music(self):
        '''Functional testing required'''
        pass

    def test_draw_text(self):
        flag = False
        try:
            text = library.draw_text(to_print='Lorem ipsum dolor sit amet.', text_color=library.WHITE, bg_color=library.BLACK, text_size=25, bold=False)
        except pygame.error as pe:
            flag = True
        finally:
            self.assertTrue(flag)

        pygame.font.init()
        flag = True
        try:
            text = library.draw_text(to_print='Lorem ipsum dolor sit amet.', text_color=library.WHITE, bg_color=library.BLACK, text_size=25, bold=False)
        except pygame.error as pe:
            flag = False
        finally:
            self.assertTrue(flag)

        text = library.draw_text(to_print='Lorem ipsum dolor sit amet.', text_color=library.WHITE, bg_color=library.BLACK, text_size=25, bold=False)
        self.assertIsInstance(text, pygame.surface.Surface)

        pygame.font.quit()

    def test_draw_vertical_bar(self):
        bar, rect = library.draw_vertical_bar(library.WHITE, 50, 100, 1.0)
        self.assertIsInstance(bar, pygame.surface.Surface)
        self.assertIsInstance(rect, pygame.rect.Rect)

        flag = False
        try:
            bar, rect = library.draw_vertical_bar(library.WHITE, 50, 100, 2.0)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

    def test_draw_boss_bar(self):
        bar, rect = library.draw_boss_bar(50, 100, 1.0, 1.0)
        self.assertIsInstance(bar, pygame.surface.Surface)
        self.assertIsInstance(rect, pygame.rect.Rect)

        flag = False
        try:
            bar, rect = library.draw_boss_bar(50, 100, 1.0, 2.0)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            bar, rect = library.draw_boss_bar(50, 100, 2.0, 1.0)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            bar, rect = library.draw_boss_bar(50, 100, 1.0, 'a')
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            bar, rect = library.draw_boss_bar(50, 100, 'a', 1.0)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

    def test_draw_player_lives(self):
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_mode((1,1))
        image, rect = library.draw_player_lives(3)
        self.assertIsInstance(image, pygame.surface.Surface)
        self.assertIsInstance(rect, pygame.rect.Rect)
        pygame.font.quit()
        pygame.display.quit()
    
    def test_draw_bombs_remaining(self):
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_mode((1,1))
        image, rect = library.draw_bombs_remaining(3)
        self.assertIsInstance(image, pygame.surface.Surface)
        self.assertIsInstance(rect, pygame.rect.Rect)
        pygame.font.quit()
        pygame.display.quit()

    def test_draw_instructions(self):
        flag = False
        try:
            block = library.draw_instructions()
        except pygame.error as pe:
            flag = True
        finally:
            self.assertTrue(flag)

        pygame.font.init()
        block = library.draw_instructions()
        self.assertIsInstance(block, pygame.surface.Surface)
        pygame.font.quit()

    def test_draw_button(self):
        flag = False
        try:
            button, rect = library.draw_button(text='Lorem ipsum dolor sit amet.')
        except pygame.error as pe:
            flag = True
        finally:
            self.assertTrue(flag)

        pygame.font.init()
        button, rect = library.draw_button(text='Lorem ipsum dolor sit amet.')
        self.assertIsInstance(button, pygame.surface.Surface)
        self.assertIsInstance(rect, pygame.rect.Rect)
        pygame.font.quit()

    def test_savegame(self):
        '''tested concurrently with loadgame'''
        pass       
    
    def test_loadgame(self):
        test_save = [1,'a',[]]
        library.saveGame(test_save, 'unittest.sav')
        result = library.loadGame('unittest.sav')
        self.assertEqual(test_save, result)
        os.remove(library.SAVES_PATH.joinpath('unittest.sav'))

if __name__ == "__main__":
    unittest.main(exit=False)