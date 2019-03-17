import pygame
import GUI
import library
import highscore
import levelLoader
import copy
import unittest

class TestGUI(unittest.TestCase):
    def test__init__(self):
        '''Testing either covered by various setters/getters or require functional tests'''
        pass

    def test_screen_setter(self):
        window = GUI.GUI()

        sample_surf = pygame.surface.Surface((1,1))
        window.screen = sample_surf
        self.assertEqual(id(window.screen), id(sample_surf))

        flag = False
        try:
            window.screen = '42'
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        pygame.quit()

    def test_screen_rect_setter(self):
        window = GUI.GUI()

        sample_rect = pygame.rect.Rect(0,0,1,1)
        window.screen_rect = sample_rect
        self.assertEqual(window.screen_rect, sample_rect)

        flag = False
        try:
            window.screen_rect = '42'
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        pygame.quit()

    def test_hs_list_setter(self):
        window = GUI.GUI()

        sample_hs_list = highscore.Scoreboard()
        sample_hs_list.resetList()
        window.hs_list = sample_hs_list
        self.assertEqual(window.hs_list, sample_hs_list)

        flag = False
        try:
            window.hs_list = '42'
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        pygame.quit()

    def test_loader_setter(self):
        window = GUI.GUI()

        loader = levelLoader.LevelLoader()
        window.loader = loader
        self.assertEqual(window.loader, loader)

        flag = False
        try:
            window.loader = '42'
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = True
        try:
            window.loader = None
        except RuntimeError as rte:
            flag = False
        finally:
            self.assertTrue(flag)

        pygame.quit()

    def test_clock_setter(self):
        window = GUI.GUI()

        clock = pygame.time.Clock()
        window.clock = clock
        self.assertEqual(window.clock, clock)

        flag = False
        try:
            window.clock = '42'
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        pygame.quit()

    def test_game_intro(self):
        '''Functional Testing Required.'''
        pass
        
    def test_main(self):
        '''Functional Testing Required.'''
        pass

    def test_pause_screen(self):
        '''Functional Testing Required.'''
        pass
    
    def test_ask_to_save(self):
        '''Functional Testing Required.'''
        pass

    def test_level_complete(self):
        '''Functional Testing Required.'''
        pass

    def test_death_loop(self):
        '''Functional Testing Required.'''
        pass

    def test_game_over(self):
        '''Functional Testing Required.'''
        pass

    def test_add_to_hs(self):
        '''Functional Testing Required.'''
        pass

    def test_menu(self):
        '''Functional Testing Required.'''
        pass

    def test_credits(self):
        '''Functional Testing Required.'''
        pass

    def test_high_scores(self):
        '''Functional Testing Required.'''
        pass
    
    def test_level_loop(self):
        '''Functional Testing Required.'''
        pass

    def test_victory(self):
        '''Functional Testing Required.'''
        pass


if __name__ == "__main__":
    unittest.main(exit=False)
        