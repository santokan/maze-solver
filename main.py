from graphics import Window
from cell import Cell


def main():
    win = Window(800, 600)
    c = Cell(win)
    c.has_left_wall = False
    c.draw(100, 100, 200, 200)

    c = Cell(win)
    c.has_right_wall = False
    c.draw(250, 250, 400, 400)

    c = Cell(win)
    c.has_top_wall = False
    c.draw(400, 400, 500, 500)

    c = Cell(win)
    c.has_bottom_wall = False
    c.draw(600, 600, 700, 700)
    win.wait_for_close()


if __name__ == "__main__":
    main()
