import arcade
import timeit
from pyglet import clock
import sys

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
COLUMN_WIDTH = 1920//5
X_MIN = COLUMN_WIDTH
X_MAX = SCREEN_WIDTH - COLUMN_WIDTH
SCREEN_TITLE = 'Raiden Clone - Day 0'

EXIT = 0
INTRO = 1
MENU = 2
GAME = 3
PAUSED = 4
HIGH_SCORE_LIST = 5
CREDITS = 6

DEBUG = True

class Bullet(arcade.Sprite):
    def __init__(self, path_to_img, startx, starty, speedx, speedy):
        super().__init__(path_to_img)
        self.center_x = startx
        self.center_y = starty
        self.change_x = speedx
        self.change_y = speedy

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if not (X_MIN < self.center_x < X_MAX):
            self.kill()
        if not (0 < self.center_y < SCREEN_HEIGHT):
            self.kill()

class EnemyShip(arcade.Sprite):
    def __init__(self, path_to_img, startx, starty, speedx, speedy):
        super().__init__(path_to_img)
        self.center_x = startx
        self.center_y = starty
        self.change_x = speedx
        self.change_y = speedy
    
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if not (X_MIN < self.center_x < X_MAX):
            self.kill()
        if not (0 < self.center_y < SCREEN_HEIGHT):
            self.kill() 

class PlayerShip(arcade.Sprite):
    def __init__(self, path_to_img, startx, starty):
        super().__init__(path_to_img)
        self.center_x = startx
        self.center_y = starty
        self.rof = 15

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < X_MIN:
            self.left = X_MIN
        elif self.right > X_MAX - 1:
            self.right = X_MAX - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

    def shoot(self):
        return Bullet('resources/weapon_images/spitfire.png', self.center_x, self.top, 0, 15)

class BackgroundSprite(arcade.Sprite):
    def __init__(self, path_to_img, img_height, img_width, centerx, centery, velocity):
        super().__init__(path_to_img, image_height = img_height, image_width = img_width)
        self.center_x = centerx
        self.center_y = centery
        self.velocity = velocity

    def update(self):
        super().update()
        if self.center_y <= -self.height//2:
            self.center_y = self.height + self.height//2

class GUI(arcade.Window):
    """
    Main application class.

    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.frame_count = 0
        self.curr_state = MENU        

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.playerShip = None
        self.game_background = None
        self.menu_background = None

        self.player_sprites = None
        self.player_bullet_sprites = None
        self.enemy_sprites = None
        self.enemy_bullet_sprites = None

        ##key pressed setup
        self.UP_PRESSED = False
        self.DOWN_PRESSED = False
        self.LEFT_PRESSED = False
        self.RIGHT_PRESSED = False
        self.SPACEBAR_PRESSED = False
        self.ESCAPE_PRESSED = False
        self.PAUSE_PRESSED = False

        #Window setup
        arcade.set_background_color(arcade.color.BLACK)
        self.set_mouse_visible(False)

    def setup(self):
        #background setup
        #self.game_background = arcade.Sprite('nebula_blue.png')
        self.game_background = arcade.SpriteList()
        for i in range(2):
            self.game_background.append(BackgroundSprite('nebula_blue.png', 4096, 3*SCREEN_WIDTH//5, SCREEN_WIDTH//2, i*4096 + 2048, (0,-4))) ##velocity _MUST BE_ a divisor of the height.
        self.menu_background = arcade.SpriteList()
        for i in range(2):
            self.menu_background.append(BackgroundSprite('nebula_red.png', 4096, 4096, SCREEN_WIDTH//2, i*4096 + 2048, (0,-.5)))  ##velocity _MUST BE_ a divisor of the height.

        # Create your sprites and sprite lists here
        self.player_sprites = arcade.SpriteList()
        self.player_bullet_sprites = arcade.SpriteList()
        self.enemy_sprites = arcade.SpriteList()
        self.enemy_bullet_sprites = arcade.SpriteList()

        self.playerShip = PlayerShip('CoolShip.png',1000,100)
        self.player_sprites.append(self.playerShip)        

    def null_input(self):
        self.UP_PRESSED = False
        self.DOWN_PRESSED = False
        self.LEFT_PRESSED = False
        self.RIGHT_PRESSED = False
        self.SPACEBAR_PRESSED = False
        self.ESCAPE_PRESSED = False
        self.PAUSE_PRESSED = False

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()            

        if self.curr_state == INTRO:
            self.draw_intro()

        if self.curr_state == MENU:
            self.draw_menu()

        if self.curr_state == GAME:
            self.draw_game()

        if self.curr_state == PAUSED:
            self.draw_paused()

        if DEBUG:
            #draw text
            output = "Max FPS: {:3.1f}".format(clock.get_fps())
            arcade.draw_text(output, 20, 20, arcade.color.WHITE, 16)


    def draw_intro(self):
        #draw background
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2,SCREEN_WIDTH,SCREEN_HEIGHT, self.menu_background)
        ##TODO## Opening Scroll

    def draw_menu(self):
        ##TODO## I/O
        #draw background
        self.menu_background.draw()

    def draw_game(self):
        #draw background
        self.game_background.draw()

        self.playerShip.draw()
        self.player_bullet_sprites.draw()

    def draw_paused(self):
        #draw background
        self.game_background.draw()
        #draw text
        arcade.draw_text('***PAUSED***', SCREEN_WIDTH//2, SCREEN_HEIGHT//2, arcade.color.WHITE, 24, align='center', anchor_x='center', anchor_y ='center')

        self.playerShip.draw()
        self.player_bullet_sprites.draw()

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.frame_count += 1

        if self.curr_state == MENU:
            if self.SPACEBAR_PRESSED:
                self.curr_state = GAME
                self.null_input()
                arcade.pause(1)
            if self.ESCAPE_PRESSED:
                self.curr_state = EXIT
                sys.exit()
            self.menu_background.update()

        if self.curr_state == PAUSED:
            if self.ESCAPE_PRESSED:
                self.null_input()
                self.curr_state = MENU
            if self.SPACEBAR_PRESSED or self.PAUSE_PRESSED:
                self.curr_state = GAME
                self.null_input()
                for sprite in self.game_background:
                    sprite.velocity = (0,-4) 
                arcade.pause(1)

        if self.curr_state == GAME:
            self.playerShip.change_x, self.playerShip.change_y = 0, 0

            if self.UP_PRESSED and not self.DOWN_PRESSED:
                self.playerShip.change_y = 10 
            if self.DOWN_PRESSED and not self.UP_PRESSED:
                self.playerShip.change_y = -10 
            if self.RIGHT_PRESSED and not self.LEFT_PRESSED:
                self.playerShip.change_x = 10 
            if self.LEFT_PRESSED and not self.RIGHT_PRESSED:
                self.playerShip.change_x = -10  
            if self.SPACEBAR_PRESSED:
                if self.frame_count % self.playerShip.rof == 0:
                    bullet = self.playerShip.shoot()
                    self.player_bullet_sprites.append(bullet)     
            if self.ESCAPE_PRESSED:
                self.null_input()
                self.curr_state = MENU
            if self.PAUSE_PRESSED:
                self.null_input()
                for sprite in self.game_background:
                    sprite.velocity = (0,0)
                self.curr_state = PAUSED      

            self.game_background.update()
            self.playerShip.update()
            self.player_bullet_sprites.update()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.UP:
            self.UP_PRESSED = True
        if key == arcade.key.DOWN:
            self.DOWN_PRESSED = True
        if key == arcade.key.LEFT:
            self.LEFT_PRESSED = True
        if key == arcade.key.RIGHT:
            self.RIGHT_PRESSED = True
        if key == arcade.key.SPACE:
            self.SPACEBAR_PRESSED = True
        if key == arcade.key.ESCAPE:
            self.ESCAPE_PRESSED = True
        if key == arcade.key.PAUSE:
            self.PAUSE_PRESSED = True

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP:
            self.UP_PRESSED = False
        if key == arcade.key.DOWN:
            self.DOWN_PRESSED = False
        if key == arcade.key.LEFT:
            self.LEFT_PRESSED = False
        if key == arcade.key.RIGHT:
            self.RIGHT_PRESSED = False
        if key == arcade.key.SPACE:
            self.SPACEBAR_PRESSED = False
        if key == arcade.key.ESCAPE:
            self.ESCAPE_PRESSED = False
        if key == arcade.key.PAUSE:
            self.PAUSE_PRESSED = False

def main():
    """ Main method """
    game = GUI(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()