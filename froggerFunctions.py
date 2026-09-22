import arcade
import froggerHelper
from froggerHelper import WINDOW_WIDTH, WINDOW_SPEED, WINDOW_HEIGHT

class Player(arcade.Sprite):  # Class to represent the player
    def __init__(self):
        super().__init__()
        self.textures = [arcade.load_texture(":resources:/images/enemies/frog.png", flipped_horizontally=True),
                         arcade.load_texture(":resources:/images/enemies/frog.png")]
        self.texture = self.textures[1]
        self.score = 0
        self.vertnum = 0
        self.lives = 3

# vertical snap points of move_up and move_down
vertical_positions = [64, 96, 180, 226, 277, 335, 370.5, 420, 483, 570, 659]
# sound effects for game
move_sound = arcade.load_sound("sounds/sound-frogger-hop.wav")
hit_sound = arcade.load_sound("sounds/sound-frogger-squash.wav")
splash_sound = arcade.load_sound("sounds/sound-frogger-plunk.wav")
win_sound = arcade.load_sound("sounds/winsound.mp3")
gameover_sound = arcade.load_sound("sounds/gameover.mp3")

def street_lines():  # draws yellow horizontal lines (purely cosmetic)
    for xpos in range(16, WINDOW_WIDTH, 160):
        arcade.draw_xywh_rectangle_filled(xpos, (212.25 - 6.25), 128, 12.5, arcade.color.YELLOW)

def draw_scene(self):  # draws background, player, scoreboard, lives counter, level counter, and enemies
    arcade.draw_xywh_rectangle_filled(0, 0, WINDOW_WIDTH, 128, arcade.color.DARK_SPRING_GREEN)
    arcade.draw_xywh_rectangle_filled(0, 128, WINDOW_WIDTH, 168.5, arcade.color.GRAY)
    arcade.draw_xywh_rectangle_filled(0, 296.5, WINDOW_WIDTH, 128, arcade.color.DARK_SPRING_GREEN)
    arcade.draw_xywh_rectangle_filled(0, 593, WINDOW_WIDTH, 128, arcade.color.DARK_SPRING_GREEN)
    self.water.draw()
    show_stats(self)
    street_lines()
    self.vehicle_list_left.draw()
    self.vehicle_list_right.draw()
    self.turtle_list_left.draw()
    self.turtle_list_right.draw()
    self.player.draw()

def move_up(self):  # moves player up
    if self.player.vertnum < len(vertical_positions) - 1:  # prevents index range error
        arcade.play_sound(move_sound)
        self.player.vertnum += 1
        self.player.center_y = vertical_positions[self.player.vertnum]

def move_down(self):
    if self.player.vertnum > 0:  # prevents moving offscreen or to end of list
        arcade.play_sound(move_sound)
        self.player.vertnum -= 1
        self.player.center_y = vertical_positions[self.player.vertnum]

def move_left(self):  # moves player left 32 pixels
    if self.player.center_x > 32:  # prevents player from moving offscreen
        self.player.texture = self.player.textures[1]
        arcade.play_sound(move_sound)
        self.player.center_x -= 32

def move_right(self):  # moves player right 32 pixels
    if self.player.center_x < WINDOW_WIDTH-32:  # prevents player from moving offscreen
        self.player.texture = self.player.textures[0]
        arcade.play_sound(move_sound)
        self.player.center_x += 32

def game_over(self):  # shows game over screen, starts gameover sequence
    arcade.draw_text("Game Over", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                     arcade.color.RED, font_size=50, anchor_x="center")
    arcade.draw_text("Press any key to restart", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50,
                     arcade.color.BLACK, font_size=20, anchor_x="center")
    if self.alive:
        arcade.play_sound(gameover_sound)
    self.alive = False

def victory(self):  # displays win screen, increases score, increase difficulty
    arcade.draw_text("You Won!", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                     arcade.color.PURPLE_HEART, font_size=50, anchor_x="center")
    arcade.draw_text("Press any key to restart", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50,
                     arcade.color.BLACK, font_size=20, anchor_x="center")
    if self.alive:
        self.player.score = self.player.score + 100  # increases score by fixed amount
        self.windowspeed += WINDOW_SPEED  # increases window speed
        arcade.play_sound(win_sound)
        self.level += 1  # increases level count
        respace_enemies(self)
    self.alive = False

def show_stats(self):  # shows scoreboard, lives, and level
    score_text = arcade.Text(f"Score:{self.player.score}", 1050, 657, arcade.color.WHITE, 30, 32)
    lives_text = arcade.Text(f"Lives:{self.player.lives}", 150, 657, arcade.color.WHITE, 30, 32)
    level_text = arcade.Text(f"Level:{self.level}", (WINDOW_WIDTH / 2) - 64, 657, arcade.color.WHITE, 30, 32)
    score_text.draw()
    lives_text.draw()
    level_text.draw()

def take_lives(self):  # decreases lives by 1
    self.player.lives -= 1
    if self.player.lives <= 0:
        self.alive = False
        self.game_over = True  # Set game_over to True if lives reach zero

def check_for_collision(self):  # if colliding -> take 1 life -> reset
    if (arcade.check_for_collision_with_list(self.player, self.vehicle_list_left) or  # checks if player is hit by car
            arcade.check_for_collision_with_list(self.player, self.vehicle_list_right)):
        arcade.play_sound(hit_sound)
        take_lives(self)
        self.reset_game_state()
    if (arcade.check_for_collision(self.player, self.water)  # checks if player is in water and not on turtle
            and not (arcade.check_for_collision_with_list(self.player, self.turtle_list_right) or
                     arcade.check_for_collision_with_list(self.player, self.turtle_list_left))):
        arcade.play_sound(splash_sound)
        take_lives(self)
        self.reset_game_state()

def respace_enemies(self):  # respaces all enemies on victory condition
    self.vehicle_list_left.clear()
    self.vehicle_list_left = froggerHelper.make_vehicles_left(5)
    self.vehicle_list_right.clear()
    self.vehicle_list_right = froggerHelper.make_vehicles_right(5)
    self.turtle_list_left.clear()
    self.turtle_list_left = froggerHelper.make_turtles_left(5)
    self.turtle_list_right.clear()
    self.turtle_list_right = froggerHelper.make_turtles_right(5)