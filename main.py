import arcade

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = 'Day 0'

class PlayerShip(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

class GUI(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.playerShip = None

        self.UP_PRESSED = False
        self.DOWN_PRESSED = False
        self.LEFT_PRESSED = False
        self.RIGHT_PRESSED = False

    def setup(self):
        # Create your sprites and sprite lists here
        self.playerShip = PlayerShip('CoolShip.png')
        self.playerShip.center_x, self.playerShip.center_y = 1000, 100
        

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.playerShip.draw()

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.playerShip.change_x, self.playerShip.change_y = 0, 0

        if self.UP_PRESSED and not self.DOWN_PRESSED:
            self.playerShip.change_y = 10 
        if self.DOWN_PRESSED and not self.UP_PRESSED:
            self.playerShip.change_y = -10 
        if self.RIGHT_PRESSED and not self.LEFT_PRESSED:
            self.playerShip.change_x = 10 
        if self.LEFT_PRESSED and not self.RIGHT_PRESSED:
            self.playerShip.change_x = -10     

        self.playerShip.update()

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

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = GUI(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()