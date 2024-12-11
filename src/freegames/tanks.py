
"""
Tank Battle Game

Exercises:

1. Change the colors of the tanks and bullets.
2. Adjust the frame rate to make the game faster or slower.
3. Modify the speed of the bullets.
4. Add more obstacles or rearrange their positions.
5. Increase or decrease the tank's movement speed.
6. Implement a power-up system (e.g., extra bullets or health).
7. Create a scoring system to track wins.
8. Allow multiple players (up to 4 tanks).
9. Add a second bullet type with different behaviors.
"""

from turtle import *
from freegames import vector
from math import cos, sin, radians

class Tank:
    def __init__(self, x, y, color, controls):
        self.position = vector(x, y)
        self.speed = vector(0, 0)
        self.color = color
        self.controls = controls
        self.direction = 90  # Start direction (up)
        self.hp = 3
        self.bullets = []

        self.body = Turtle()
        self.body.shape("square")
        self.body.color(color)
        self.body.shapesize(1.5, 1)
        self.body.penup()
        self.body.goto(x, y)

        self.gun = Turtle()
        self.gun.shape("square")
        self.gun.color("black")
        self.gun.shapesize(0.5, 0.2)
        self.gun.penup()
        self.update_gun()

    def update_gun(self):
        self.gun.goto(self.position.x + 15 * cos(radians(self.direction)),
                     self.position.y + 15 * sin(radians(self.direction)))
        self.gun.setheading(self.direction)

    def move(self):
        new_pos = self.position + self.speed
        if -200 < new_pos.x < 200 and -200 < new_pos.y < 200 and self.valid_position(new_pos):
            self.position = new_pos
            self.body.goto(self.position.x, self.position.y)
            self.update_gun()

    def change_speed(self, dx, dy, angle=None):
        self.speed.x, self.speed.y = dx, dy
        if angle is not None:
            self.direction = angle

    def shoot(self):
        bullet = vector(self.position.x + 15 * cos(radians(self.direction)),
                        self.position.y + 15 * sin(radians(self.direction)))
        direction = vector(cos(radians(self.direction)), sin(radians(self.direction))) * 15  # Increased bullet speed
        bullet_turtle = Turtle()
        bullet_turtle.shape("circle")
        bullet_turtle.color(self.color)
        bullet_turtle.shapesize(0.2, 0.2)
        bullet_turtle.penup()
        bullet_turtle.goto(bullet.x, bullet.y)
        self.bullets.append((bullet, direction, bullet_turtle))

    def valid_position(self, pos):
        for obstacle in obstacles:
            if obstacle.distance(pos.x, pos.y) < 20:
                return False
        return True

    def hit(self):
        self.hp -= 1
        print(f"{self.color} tank HP: {self.hp}")
        if self.hp <= 0:
            self.body.hideturtle()
            self.gun.hideturtle()
            return True
        return False

screen = Screen()
screen.setup(420, 420)
screen.tracer(False)

# Create map
obstacles = []
for x, y in [(-100, 50), (50, -50), (0, 100)]:
    obs = Turtle()
    obs.shape("square")
    obs.color("gray")
    obs.penup()
    obs.goto(x, y)
    obstacles.append(obs)

tank1 = Tank(-150, 0, 'blue', {'up': 'w', 'down': 's', 'left': 'a', 'right': 'd', 'shoot': 'e'})
tank2 = Tank(150, 0, 'red', {'up': 'Up', 'down': 'Down', 'left': 'Left', 'right': 'Right', 'shoot': 'Return'})

def setup_controls(tank, controls):
    onkey(lambda: tank.change_speed(0, 10, 90), controls["up"])
    onkey(lambda: tank.change_speed(0, -10, 270), controls["down"])
    onkey(lambda: tank.change_speed(-10, 0, 180), controls["left"])
    onkey(lambda: tank.change_speed(10, 0, 0), controls["right"])
    onkey(tank.shoot, controls["shoot"])

setup_controls(tank1, tank1.controls)
setup_controls(tank2, tank2.controls)

def update():
    tank1.move()
    tank2.move()

    for tank in (tank1, tank2):
        new_bullets = []
        for bullet, direction, bullet_turtle in tank.bullets:
            bullet.move(direction)
            if -200 < bullet.x < 200 and -200 < bullet.y < 200:
                bullet_turtle.goto(bullet.x, bullet.y)
                new_bullets.append((bullet, direction, bullet_turtle))

                target = tank2 if tank == tank1 else tank1
                if abs(bullet - target.position) < 10 and target.hit():
                    print(f"{target.color} tank destroyed!")
                    bullet_turtle.hideturtle()
                    return
            else:
                bullet_turtle.hideturtle()
        tank.bullets = new_bullets

    screen.update()
    ontimer(update, 50)

listen()
update()
done()
