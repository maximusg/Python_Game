import pygame
import GUI
import bomb_explosion
import weapon
import explosion
import unittest

class TestAnims(unittest.TestCase):

    def test_animation_frames(self):
        '''Testing ensures that the animation frames are updated every frame'''
        pygame.init()
        screen = pygame.display.set_mode((1, 1))
        screen.fill((0,0,0))
        pygame.display.set_caption('Testy mcTetsterson')
        bombExplAnim = bomb_explosion.BombExplosion(1,1)

        #tests bombExplosion
        frame1 = bombExplAnim.frame
        bombExplAnim.update()
        frame2 = bombExplAnim.image

        self.assertNotEqual(frame1, frame2)

        #tests explosions
        explosionAnim = explosion.ExplosionSprite(1,1)
        frame1 =explosionAnim.frame
        explosionAnim.update()
        frame2 = explosionAnim.image

        self.assertNotEqual(frame1, frame2)

        pygame.quit()

if __name__ == "__main__":
    unittest.main(exit=False)
