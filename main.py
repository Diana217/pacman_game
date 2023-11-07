from turtle import *
from random import choice
from freegames import floor, vector
from game_data import tiles

state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80)
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

def draw_square(x, y):
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def calculate_tile_index(point):
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def is_valid_tile_position(point):
    index = calculate_tile_index(point)

    if tiles[index] == 0:
        return False

    index = calculate_tile_index(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def draw_world():
    bgcolor('blue')
    path.color('yellow')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            draw_square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'black')

def move_pacman_and_ghosts():
    writer.undo()
    writer.write(state['score'])

    clear()

    if is_valid_tile_position(pacman + aim):
        pacman.move(aim)

    index = calculate_tile_index(pacman)

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        draw_square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'green')

    for point, course in ghosts:
        if is_valid_tile_position(point + course):
            point.move(course)
        else:
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return

    ontimer(move_pacman_and_ghosts, 100)


def change_pacman_direction(x, y):
    if is_valid_tile_position(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


setup(420, 420, 370, 0)
hideturtle()
tracer(False)

writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])

listen()

onkey(lambda: change_pacman_direction(5, 0), 'Right')
onkey(lambda: change_pacman_direction(-5, 0), 'Left')
onkey(lambda: change_pacman_direction(0, 5), 'Up')
onkey(lambda: change_pacman_direction(0, -5), 'Down')

draw_world()

move_pacman_and_ghosts()

done()