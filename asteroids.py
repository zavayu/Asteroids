import csv
import random
import turtle
import math
import time

playing = False
stop = False
score = 0
level = 0

try:
    file = open("HighScores.dat", "r+")
except FileNotFoundError:
    print("Missing HighScores.dat file!")
    turtle.bye()

# Window Setup
wn = turtle.Screen()
wn.setup(800, 800)
wn.bgcolor('black')
wn.title('Asteroids Game')
turtle.setundobuffer(1)
turtle.tracer(0)

# Draw border, 400x400 square
border = turtle.Turtle()
border.speed(0)
border.color('Red')
border.up()
border.setposition(-350, -350)
border.down()
border.pensize(3)
for _ in range(4):
    border.forward(700)
    border.left(90)
border.hideturtle()

# Write Status
status = turtle.Turtle()
status.penup()
status.hideturtle()
status.goto(-325, 355)
status.pendown()
status.color("White")
status.write(f"Asteroids Game | by The Fortnite Gamers |", font=("Impact", 20, "normal"))

# Game Instructions
inst = turtle.Turtle()
inst.penup()
inst.hideturtle()
inst.pendown()
inst.color("White")
inst.write("ASTEROIDS", align="center", font=("IMPACT", 75, "bold"))
inst.penup()
inst.goto(0, -50)
inst.pendown()
inst.color("Light Blue")
inst.write("Press Enter to Start!", align="center", font=("Times New Roman", 30, "normal"))
inst.penup()
inst.color("white")
inst.goto(0, -300)
inst.pendown()
written_instructions = ("• Use Arrow Keys to move\n• Press Space to shoot\n• Hit an asteroid and you lose a life\n•You "
                        "have a total of 3 lives\n• Clear asteroids to gain points!\n• Press Escape to exit")
inst.write(written_instructions, align="center", font=("Times New Roman", 20, "normal"))


def end_game():
    """Ends the game"""
    global playing
    global stop
    playing = False
    stop = True


def start_game():
    """Exits the instructions page and begins the game"""
    global playing
    global stop
    inst.clear()
    stop = True
    playing = True


# Wait for key press to start game
turtle.listen()
turtle.onkey(start_game, "Return")
turtle.onkey(end_game, "Escape")

while not stop:
    turtle.update()

# Create Player
ship = turtle.Turtle()
ship.speed(0)
ship.penup()
ship.shape("triangle")
ship.shapesize(1, 1.25, 2)
ship.color("light blue", "Black")
ship.setheading(90)

# Create ship flame from boost
flame = turtle.Turtle()
flame.penup()
flame.color("Orange", "Yellow")
flame.shape("triangle")
flame.shapesize(0.75, 1.15, 1.2)
flame.hideturtle()

# Create Bullet
bullet = turtle.Turtle()
bullet.setposition(400, 400)
bullet.penup()
bullet.speed(0)
bullet.shape("circle")
bullet.color("white")
bullet.shapesize(0.35, 0.35, 1)
bullet.hideturtle()

# Create Asteroids
asteroids = {}

# World Building variables
speeds = [0, 0]
terminal_velocity = 8
bullet_speed = 25
shooting = False
ship.rcc = False
ship.rc = False
ship.boosting = False


# To create smoother movement from input from the user, we create a simple
# function call which changes just one boolean value of the ship
# the turtle.onkeypressed() and turtle.onkeyrelease() will call these simple functions
# and in the main loop the movement will be processed.
# If the turtle.onkeypress() referenced the movement functions, movement will be choppy
def rc_on():
    """Turns clockwise rotation on"""
    ship.rc = True


def rc_off():
    """Turns clockwise rotation off"""
    ship.rc = False


def rcc_on():
    """Turns counterclockwise rotation on"""
    ship.rcc = True


def rcc_off():
    """Turns counterclockwise rotation off"""
    ship.rcc = False


def rotate_counter_clockwise():
    """rotates the ship counterclockwise"""
    ship.left(8)


def rotate_clockwise():
    """rotates the ship clockwise"""
    ship.right(8)


def boost_on():
    """Turns boosters on"""
    ship.boosting = True


def boost_off():
    """Turns boosters off"""
    ship.boosting = False


def boost():
    """Propels the ship forward"""
    # print(speeds)
    heading = ship.heading()
    x_angle = math.cos(heading * math.pi / 180)
    y_angle = math.sin(heading * math.pi / 180)
    if abs(speeds[0] + x_angle / 2) < terminal_velocity:
        speeds[0] += x_angle / 2
    if abs(speeds[1] + y_angle / 2) < terminal_velocity:
        speeds[1] += y_angle / 2


def shoot():
    """If a bullet is not currently firing, fires a bullet from the player's ship"""
    if not shooting:
        bullet.setposition(ship.xcor(), ship.ycor())
        bullet.showturtle()
        bullet.setheading(ship.heading())


def check_collision(projectile):
    """Checks each asteroid to detect if the ship has collided with any"""
    for asteroid in asteroids:
        size = asteroid.shapesize()
        radius = size[0] * (17 - size[0])
        asteroid_pos = [asteroid.xcor(), asteroid.ycor()]
        projectile_pos = [projectile.xcor(), projectile.ycor()]
        # Use distance formula to detect if ship is within bounds of asteroid
        distance = math.sqrt((asteroid_pos[0] - projectile_pos[0]) ** 2 + (asteroid_pos[1] - projectile_pos[1]) ** 2)
        if distance <= radius:
            return True, asteroid


def add_asteroid(size=1, x_max=4, y_max=4, ast_x=-500, ast_y=-500):
    """Adds an asteroid to the screen"""
    asteroid = turtle.Turtle()
    asteroid.penup()
    asteroid.shapesize(size, size, 3)
    asteroid.speed(0)
    asteroid.shape("circle")
    asteroid.color("#784c00", "Black")

    if ast_x == -500 or ast_y == -500:
        ast_x = random.randint(-290, 290)
        ast_y = random.randint(-290, 290)
        while (-100 <= ast_x <= 100) or (-100 <= ast_x <= 100):
            ast_x = random.randint(-290, 290)
            ast_y = random.randint(-290, 290)

    x_vel = random.randint(-x_max, x_max)
    y_vel = random.randint(-y_max, y_max)
    while x_vel == 0 or y_vel == 0:
        x_vel = random.randint(-x_max, x_max)
        y_vel = random.randint(-y_max, y_max)

    asteroid.setposition(ast_x, ast_y)
    asteroids[asteroid] = [x_vel, y_vel, x_max, y_max, size]


def split_asteroid(asteroid):
    """splits an asteroid into 2 smaller asteroids"""
    size = asteroids[asteroid][4]
    ast_x = asteroid.xcor()
    ast_y = asteroid.ycor()

    size -= 1
    add_asteroid(size, 4, 4, ast_x + 1, ast_y + 1)
    add_asteroid(size, 4, 4, ast_x + 1, ast_y + 1)


def del_asteroid(asteroid):
    """Deletes an asteroid from the screen and dictionary"""
    asteroid.hideturtle()
    asteroids.pop(asteroid)


# Write score at top of frame
write_score = turtle.Turtle()
write_score.penup()
write_score.goto(235, 355)
write_score.color("Gold")
write_score.hideturtle()

# Write level at the bottom of frame
level_pen = turtle.Turtle()
level_pen.penup()
level_pen.goto(255, -390)
level_pen.color("White")
level_pen.hideturtle()


def update_score():
    """Updates the score at the top of the frame"""
    write_score.clear()
    write_score.write(f"Score: {score}", font=("Impact", 20, "normal"))


def update_flame():
    """Updates the position of the flame to point opposite of ship and appear behind it"""
    flame.setposition(ship.xcor() - math.cos(math.pi * ship.heading() / 180) * 12,
                      ship.ycor() - math.sin(math.pi * ship.heading() / 180) * 12)
    flame.setheading(180 + ship.heading())


def update_level():
    level_pen.clear()
    level_pen.write(f"Level: {level}", font=("Impact", 20, "normal"))


# Main Event Handlers
turtle.onkeypress(rc_on, "Right")
turtle.onkeyrelease(rc_off, "Right")
turtle.onkeypress(rcc_on, "Left")
turtle.onkeyrelease(rcc_off, "Left")
turtle.onkeypress(boost_on, "Up")
turtle.onkeyrelease(boost_off, "Up")
turtle.onkey(end_game, "Escape")
turtle.onkey(shoot, "space")

played_game = False
# Main game loop
while playing:
    played_game = True
    # Basic game updates, 0.03 tic rate
    turtle.update()
    update_score()
    update_flame()
    time.sleep(0.03)
    x = ship.xcor()
    y = ship.ycor()

    # Level setup
    if len(asteroids) == 0:
        level += 1
        update_level()
        lvl_file = open("Levels.csv", "r")
        lvl_reader = csv.reader(lvl_file)
        first_line = True
        for data in lvl_reader:
            if first_line:
                first_line = False
                continue
            curr = data[0]
            if int(curr) == level:
                add_asteroid(int(data[1]), int(data[2]), int(data[3]))

    # Move the ship from user input
    if ship.rcc:
        rotate_counter_clockwise()
    if ship.rc:
        rotate_clockwise()
    if ship.boosting:
        flame.showturtle()
        boost()
    else:
        flame.hideturtle()

    # Teleport Ship to the other side if exiting frame
    if abs(x) >= 360:
        ship.setposition(-x + abs(x)/x, y)
    if abs(y) >= 360:
        ship.setposition(x, -y + abs(y)/y)

    # Hide bullet and allow the player to shoot again once bullet exits frame
    if abs(bullet.xcor()) >= 350 or abs(bullet.ycor()) >= 350:
        bullet.hideturtle()
        shooting = False
    else:
        shooting = True
        bullet.forward(bullet_speed)

    # Move the ship
    ship.setposition(ship.xcor() + speeds[0], ship.ycor() + speeds[1])
    update_flame()
    # Apply friction force
    if speeds[0] != 0:
        speeds[0] -= (0.05 * abs(speeds[0]) / speeds[0])
    if speeds[1] != 0:
        speeds[1] -= (0.05 * abs(speeds[1]) / speeds[1])

    # Teleport Each asteroid to other side if exiting frame
    for ast in asteroids:
        x1 = ast.xcor()
        y1 = ast.ycor()
        if abs(x1) >= (350 - ast.shapesize()[0] * 12):
            ast.setposition(-x1 + abs(x1) / x1, y1)
        if abs(y1) >= (350 - ast.shapesize()[0] * 12):
            ast.setposition(x1, -y1 + abs(y1) / y1)
        ast.setposition(ast.xcor() + asteroids[ast][0], ast.ycor() + asteroids[ast][1])

    # If the ship collides with an asteroid, decrease life, teleport to 0,0
    # If out of lives, game over
    if check_collision(ship):
        ship.goto(0, 0)
        speeds[0:2] = [0, 0]

    # If an asteroid is shot, split into two smaller, faster asteroids
    if check_collision(bullet) and shooting:
        shooting = False
        ast_shot = check_collision(bullet)[1]
        if asteroids[ast_shot][4] > 2:
            split_asteroid(ast_shot)
        del_asteroid(ast_shot)
        score += 20
        bullet.setposition(-500, -500)

# End of game loop - calculate high scores
file.write(f'{score}\n')
lvl_file.close()
lines = file.readlines() + [score]
scores = []
highest_scores = []

for line in lines:
    scores.append(int(line))
file.close()
if len(lines) > 3:
    for _ in range(3):
        maximum = max(scores)
        highest_scores.append(str(maximum))
        scores.pop(scores.index(maximum))
else:
    for s in scores:
        highest_scores.append(str(s))
    for s in range(3 - len(lines)):
        highest_scores.append("0")

if played_game:
    playing = True
    while playing:
        ship.hideturtle()
        bullet.hideturtle()
        write_score.penup()
        write_score.goto(0, 0)
        write_score.color("Light Blue")
        write_score.write(f"GAME OVER", align="center", font=("Impact", 80, "normal"))
        write_score.goto(0, -50)
        write_score.color("white")
        write_score.write(f"High Scores:", align="center", font=("Times New Roman", 35, "normal"))
        write_score.goto(0, -210)
        write_score.color("white")
        display_scores = ""
        you = False
        for i, high in enumerate(highest_scores):
            if int(high) == score and not you:
                display_scores += f"{i + 1}:  {high} (YOU!)\n"
                you = True
            else:
                display_scores += f"{i + 1}:  {high}\n"
        write_score.write(display_scores, align="center", font=("Times New Roman", 25, "normal"))
        for asteroid in asteroids:
            asteroid.hideturtle()
        turtle.update()
