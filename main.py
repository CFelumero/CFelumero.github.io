import arcade
import froggerFunctions
import froggerHelper
from froggerHelper import WINDOW_HEIGHT, WINDOW_WIDTH, SPRITE_SCALING, WINDOW_SPEED

class FroggerWindow(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Frogger Program")
        self.player = None
        self.water = None
        self.vehicle_list_left = froggerHelper.make_vehicles_left(5)
        self.vehicle_list_right = froggerHelper.make_vehicles_right(5)
        self.turtle_list_left = froggerHelper.make_turtles_left(5)
        self.turtle_list_right = froggerHelper.make_turtles_right(5)
        self.game_over = False  # Flag to track game over state
        self.alive = True  # sets alive state to true
        self.victory = False  # win condition
        self.windowspeed = 0
        self.level = 1

    def setup(self):
        self.player = froggerFunctions.Player()  # Create an instance of the Player class
        self.player.center_x = WINDOW_WIDTH / 2
        self.player.center_y = 64
        self.player.scale = SPRITE_SCALING
        self.water = arcade.Sprite("sprites/watersprite.png")
        self.water.center_x = WINDOW_WIDTH / 2
        self.water.center_y = 508.75
        self.game_over = False
        self.alive = True
        self.victory = False
        self.windowspeed = WINDOW_SPEED
        self.level = 1
        self.player.texture = self.player.textures[1]

    def on_update(self, delta_time: float):
        froggerHelper.move_vehicles(self)
        froggerHelper.move_turtles(self)
        froggerFunctions.check_for_collision(self)
        if self.player.center_y == froggerFunctions.vertical_positions[-1]:
            self.victory = True

    def on_key_press(self, key, modifiers):
        if self.alive:
            if key == arcade.key.UP or key == arcade.key.W:
                froggerFunctions.move_up(self)
            elif key == arcade.key.DOWN or key == arcade.key.S:
                froggerFunctions.move_down(self)
            elif key == arcade.key.LEFT or key == arcade.key.A:
                froggerFunctions.move_left(self)
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                froggerFunctions.move_right(self)
        elif self.victory:
            if key != arcade.key.MOTION_END_OF_FILE:  # placeholder key so that all keys work
                # If any key is pressed during victory, only reset the vertical position
                self.reset_game_state()
        elif self.game_over:
            self.alive = False
            self.setup()  # Reset the game when key is pressed
            self.game_over = False  # Hide game-over text

    def reset_game_state(self):  # alternative function to reset game without gameover condition
        self.player.vertnum = 0
        self.player.center_x = WINDOW_WIDTH/2
        self.player.center_y = froggerFunctions.vertical_positions[self.player.vertnum]
        self.alive = True
        self.victory = False

    def on_draw(self):
        arcade.start_render()
        froggerFunctions.draw_scene(self)
        if self.victory:
            froggerFunctions.victory(self)
        if self.game_over:
            froggerFunctions.game_over(self)
        arcade.finish_render()

def main():
    our_window = FroggerWindow()
    our_window.setup()
    arcade.run()

main()