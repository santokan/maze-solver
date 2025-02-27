from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver 5000")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def bind(self, event_name, handler):
        self.__root.bind(event_name, handler)

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

    def draw_oval(self, point, radius, fill_color="red"):
        self.__canvas.create_oval(point.x - radius, point.y - radius,
                                 point.x + radius, point.y + radius,
                                 fill=fill_color, outline="")

    def draw_rect(self, x1, y1, x2, y2, fill_color="green"):
        self.__canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="")

    def draw_polyline(self, points, fill_color="red"):
        if self.__canvas and points: # check if canvas exists and points is not empty
            coords = []
            for point in points:
                coords.append(point.x)
                coords.append(point.y)
            self.__canvas.create_line(*coords, fill=fill_color, width=2)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )
