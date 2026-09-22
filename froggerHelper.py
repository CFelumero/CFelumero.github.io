import random
import arcade

WINDOW_WIDTH = 1280  # constant for window width
WINDOW_HEIGHT = 721  # constant for window height
SPRITE_SCALING = 0.5  # constant for sprite scaling
WINDOW_SPEED = 1.25  # constant for sprite movement speed


def make_vehicles_left(num):  # draws 5 vehicles facing left
    vehicle_list_left = arcade.SpriteList()
    file_names = ["sprites/left_car1.png", "sprites/left_car2.png", "sprites/right_car1.png"]
    for car_number in range(num):
        filename = random.choice(file_names)  # randomizes the sprite of each vehicle
        vehicle = arcade.Sprite(filename)
        if filename == file_names[2]:  # flips sprite if facing wrong way
            vehicle.angle = 180
        vehicle.scale = 2
        vehicle_list_left.append(vehicle)
    for vehicle in vehicle_list_left:
        vehicle.center_x = random.randint(5, WINDOW_WIDTH - 5)  # spaces out vehicles randomly
        vehicle.center_y = 254.375
        while any(vehicle.collides_with_sprite(other_vehicle) for other_vehicle in vehicle_list_left if
                  other_vehicle != vehicle):  # prevents overlapping vehicles
            vehicle.center_x = random.randint(5, WINDOW_WIDTH - 5)
    return vehicle_list_left

def make_vehicles_right(num):  # draws 5 vehicles facing right
    vehicle_list_right = arcade.SpriteList()
    file_names = ["sprites/right_car1.png", "sprites/left_car1.png", "sprites/left_car2.png"]
    for car_number in range(num):
        filename = random.choice(file_names)  # randomizes the sprite of each vehicle
        vehicle = arcade.Sprite(filename)
        if filename == file_names[1] or filename == file_names[2]:  # flips sprite if facing wrong way
            vehicle.angle = 180
        vehicle.scale = 2
        vehicle_list_right.append(vehicle)
    for vehicle in vehicle_list_right:
        vehicle.center_x = random.randint(5, WINDOW_WIDTH - 5)  # spaces out vehicles randomly
        vehicle.center_y = 170
        while any(vehicle.collides_with_sprite(other_vehicle) for other_vehicle in vehicle_list_right if
                  other_vehicle != vehicle):  # prevents overlapping vehicles
            vehicle.center_x = random.randint(5, WINDOW_WIDTH - 5)
    return vehicle_list_right

def make_turtles_left(num):  # draws 5 turtles facing left
    turtle_list_left = arcade.SpriteList()
    for turtle_number in range(num):
        turtle = arcade.Sprite("sprites/turtle1.png")
        turtle.scale = 2
        turtle_list_left.append(turtle)
    for turtle in turtle_list_left:
        turtle.center_x = random.randint(5, WINDOW_WIDTH - 5)  # spaces out turtles randomly
        turtle.center_y = 550.875
        while any(turtle.collides_with_sprite(other_turtle) for other_turtle in turtle_list_left if
                  other_turtle != turtle):  # prevents overlapping turtles
            turtle.center_x = random.randint(5, WINDOW_WIDTH - 5)
    return turtle_list_left

def make_turtles_right(num):  # draws 5 turtles facing right
    turtle_list_right = arcade.SpriteList()
    for turtle_number in range(num):
        turtle = arcade.Sprite("sprites/turtle1.png")
        turtle.scale = 2
        turtle_list_right.append(turtle)
    for turtle in turtle_list_right:
        turtle.center_x = random.randint(5, WINDOW_WIDTH - 5)  # spaces out turtles randomly
        turtle.center_y = 466.625
        turtle.angle = 180  # makes turtle face right
        while any(turtle.collides_with_sprite(other_turtle) for other_turtle in turtle_list_right if
                  other_turtle != turtle):  # prevents overlapping turtles
            turtle.center_x = random.randint(5, WINDOW_WIDTH - 5)
    return turtle_list_right

def move_vehicles(self):
    for vehicle in self.vehicle_list_left:
        vehicle.center_x -= self.windowspeed  # Move the vehicle to the left
        # If the vehicle is at the left edge, jump to the rightmost part
        if vehicle.center_x < 0:
            vehicle.center_x = WINDOW_WIDTH
    for vehicle in self.vehicle_list_right:
        vehicle.center_x += self.windowspeed  # Move the vehicle to the right
        # If the vehicle is at the right edge, jump to the leftmost edge
        if vehicle.center_x > WINDOW_WIDTH:
            vehicle.center_x = 0

def move_turtles(self):  # moves turtles and jumps them to opposite end of window if they go out of bounds
    for turtle in self.turtle_list_right:
        turtle.center_x += self.windowspeed
        if arcade.check_for_collision(self.player, turtle):
            self.player.center_x = turtle.center_x
        if turtle.center_x > WINDOW_WIDTH:
            turtle.center_x = 0
    for turtle in self.turtle_list_left:
        turtle.center_x -= self.windowspeed
        if arcade.check_for_collision(self.player, turtle):
            self.player.center_x = turtle.center_x
        if turtle.center_x < 0:
            turtle.center_x = WINDOW_WIDTH