import turtle
import math

playing = True

# Window Setup
wn = turtle.Screen()
wn.bgcolor('black')
wn.title('Asteroids Game')

# Draw border, 400x400 square
border = turtle.Turtle()
border.speed(0)
border.color('white')
border.up()
border.setposition(-350, -350)
border.down()
border.pensize(3)
for side in range(4):
    border.fd(700)
    border.lt(90)
border.hideturtle()

# Create Player
ship = turtle.Turtle()
ship.speed(0)
ship.penup()
ship.shape("triangle")
ship.shapesize(1, 1.25, 1)
ship.color("white")
ship.setheading(90)

# World Building variables
speeds = [0, 0]
terminal_velocity = 8


# Event Handlers
def rotate_clockwise():
    """rotates the ship clockwise"""
    ship.right(25)


def rotate_counter_clockwise():
    """rotates the ship counterclockwise"""
    ship.left(25)


def boost():
    heading = ship.heading()
    x_angle = math.cos(heading * math.pi / 180)
    y_angle = math.sin(heading * math.pi / 180)
    if speeds[0] + x_angle < terminal_velocity:
        speeds[0] += x_angle
    if speeds[1] + y_angle < terminal_velocity:
        speeds[1] += y_angle


turtle.listen()
turtle.onkeypress(rotate_clockwise, "Right")
turtle.onkeypress(rotate_counter_clockwise, "Left")
turtle.onkeypress(boost, "Up")

while playing:
    x = ship.xcor()
    y = ship.ycor()
    if abs(x) >= 350:
        ship.setposition(-x, y)
    if abs(y) >= 350:
        ship.setposition(x, -y)

    ship.setposition(ship.xcor() + speeds[0], ship.ycor() + speeds[1])
