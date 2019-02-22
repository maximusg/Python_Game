import arcade
import timeit

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
COLUMN_WIDTH = 1920//5
X_MIN = COLUMN_WIDTH
X_MAX = SCREEN_WIDTH - COLUMN_WIDTH
SCREEN_TITLE = 'Day 0'

class Bullet(arcade.Sprite):
    def __init__(self, path_to_img, startx, starty):
        super().__init__(path_to_img)
        self.center_x = startx
        self.center_y = starty
        self.change_x = 0
        self.change_y = 15

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
        self.rof -= 1
        if self.rof == 0:
            self.rof = 15
            return Bullet('resources/weapon_images/spitfire.png', self.center_x, self.top)
        return None

class GUI(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.drawing_time = 0
        self.processing_time = 0

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.playerShip = None
        self.background = None

        self.player_sprites = None
        self.player_bullet_sprites = None

        ##key pressed setup
        self.UP_PRESSED = False
        self.DOWN_PRESSED = False
        self.LEFT_PRESSED = False
        self.RIGHT_PRESSED = False
        self.SPACEBAR_PRESSED = False

        #Window setup
        arcade.set_background_color(arcade.color.BLACK)
        self.set_mouse_visible(False)

    def setup(self):
        #background setup
        self.background = arcade.load_texture('nebula_blue.png')
        # Create your sprites and sprite lists here
        self.player_sprites = arcade.SpriteList()
        self.player_bullet_sprites = arcade.SpriteList()

        self.playerShip = PlayerShip('CoolShip.png',1000,100)
        self.player_sprites.append(self.playerShip)        

    def on_draw(self):
        """
        Render the screen.
        """
        draw_start_time = timeit.default_timer()

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        #draw background
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2,SCREEN_WIDTH-(2*COLUMN_WIDTH),SCREEN_HEIGHT, self.background)

        #draw text
        fps = 1 / (self.drawing_time + self.processing_time)
        output = "Max FPS: {:3.1f}".format(fps)
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 80, arcade.color.WHITE, 16)

        # Call draw() on all your sprite lists below
        self.playerShip.draw()
        self.player_bullet_sprites.draw()

        self.drawing_time = timeit.default_timer() - draw_start_time

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        process_start_time = timeit.default_timer()

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
            bullet = self.playerShip.shoot()
            if bullet:   
                self.player_bullet_sprites.append(bullet)
        

        self.playerShip.update()
        self.player_bullet_sprites.update()

        self.processing_time = timeit.default_timer() - process_start_time

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

def main():
    """ Main method """
    game = GUI(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()