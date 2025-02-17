from cell import Cell
import time
import random


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
        manual_solve=False,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)
        self._player_row = 0
        self._player_col = 0
        self._manual_solve = manual_solve
        self._player_path_cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        row_cells = []
        for j in range(self._num_rows):
            c = Cell(self._win)
            row_cells.append(c)
        self._cells.append(row_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        # self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.07)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):  # recursive backtracking algorithm
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            # which cells to visit
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return

            # random direction
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # break walls
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False

            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False

            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False

            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # recursively call the next cell
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for colum in self._cells:
            for cell in colum:
                cell.visited = False

    def solve(self):
        if self._manual_solve:
            self._start_manual_solve()
            return False  # indicate manual solve started
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):  # recursive backtracking algorithm for solving
        self._animate()
        self._cells[i][j].visited = True
        # self._cells[i][j].draw_cell(True) # highlight current cell - for debugging

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # move right
        if (
            i < self._num_cols - 1
            and not self._cells[i + 1][j].visited
            and not self._cells[i][j].has_right_wall
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        # move left
        if (
            i > 0
            and not self._cells[i - 1][j].visited
            and not self._cells[i][j].has_left_wall
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        # move down
        if (
            j < self._num_rows - 1
            and not self._cells[i][j + 1].visited
            and not self._cells[i][j].has_bottom_wall
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        # move up
        if (
            j > 0
            and not self._cells[i][j - 1].visited
            and not self._cells[i][j].has_top_wall
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        return False

    def solve_maze_manually(self):
        """
        call this method to enable manual solve mode
        """
        self._manual_solve = True
        self.solve()  # this will now call _start_manual_solve instead of _solve_r

    def _start_manual_solve(self):
        if self._win is None:
            return

        # bind keyboard events
        self._win.bind("<KeyPress>", self._on_key_press)

        # draw initial player position
        self._draw_player()

    def _draw_player(self):
        """
        draws a red circle to represent the player in the current cell
        """
        cell = self._cells[self._player_col][self._player_row]
        center_x = (cell._x1 + cell._x2) / 2
        center_y = (cell._y1 + cell._y2) / 2
        player_radius = (
            min(self._cell_size_x, self._cell_size_y) / 4
        )  # adjust player size as needed

        # clear previous player position if any - by redrawing the cells
        if self._player_path_cells:
            for path_cell in self._player_path_cells:
                self._redraw_cell_path(path_cell[0], path_cell[1])
            self._player_path_cells = []  # clear path after redrawing

        # draw player
        p1 = Point(center_x - player_radius, center_y - player_radius)
        p2 = Point(center_x + player_radius, center_y + player_radius)
        self._player_path_cells.append(
            (self._player_col, self._player_row)
        )  # store current cell in path
        self._win.draw_line(Line(p1, Point(p1.x, p2.y)), "red")  # top line
        self._win.draw_line(Line(p1, Point(p2.x, p1.y)), "red")  # left line
        self._win.draw_line(Line(p2, Point(p1.x, p2.y)), "red")  # bottom line
        self._win.draw_line(Line(p2, Point(p2.x, p1.y)), "red")  # right line

    def _redraw_cell_path(self, col_index, row_index):
        """
        redraw cell at given index without player, but keeping walls
        """
        cell = self._cells[col_index][row_index]
        # redraw walls based on cell's wall status
        if cell.has_left_wall:
            self._win.draw_line(
                Line(Point(cell._x1, cell._y1), Point(cell._x1, cell._y2)), "black"
            )
        else:
            self._win.draw_line(
                Line(Point(cell._x1, cell._y1), Point(cell._x1, cell._y2)), "white"
            )
        if cell.has_top_wall:
            self._win.draw_line(
                Line(Point(cell._x1, cell._y1), Point(cell._x2, cell._y1)), "black"
            )
        else:
            self._win.draw_line(
                Line(Point(cell._x1, cell._y1), Point(cell._x2, cell._y1)), "white"
            )
        if cell.has_right_wall:
            self._win.draw_line(
                Line(Point(cell._x2, cell._y1), Point(cell._x2, cell._y2)), "black"
            )
        else:
            self._win.draw_line(
                Line(Point(cell._x2, cell._y1), Point(cell._x2, cell._y2)), "white"
            )
        if cell.has_bottom_wall:
            self._win.draw_line(
                Line(Point(cell._x1, cell._y2), Point(cell._x2, cell._y2)), "black"
            )
        else:
            self._win.draw_line(
                Line(Point(cell._x1, cell._y2), Point(cell._x2, cell._y2)), "white"
            )

    def _on_key_press(self, event):
        if not self._manual_solve:
            return

        dx = 0
        dy = 0
        if event.keysym == "Up" or event.keysym == "w":
            dy = -1
        elif event.keysym == "Down" or event.keysym == "s":
            dy = 1
        elif event.keysym == "Left" or event.keysym == "a":
            dx = -1
        elif event.keysym == "Right" or event.keysym == "d":
            dx = 1

        new_col = self._player_col + dx
        new_row = self._player_row + dy

        if 0 <= new_col < self._num_cols and 0 <= new_row < self._num_rows:
            if self._is_valid_move(
                self._player_col, self._player_row, new_col, new_row
            ):
                # valid move
                self._player_col = new_col
                self._player_row = new_row
                self._draw_player()
                if (
                    self._player_col == self._num_cols - 1
                    and self._player_row == self._num_rows - 1
                ):
                    print("Maze Solved Manually!")  # trigger win condition

    def _is_valid_move(self, old_col, old_row, new_col, new_row):
        if (
            new_col > old_col and not self._cells[old_col][old_row].has_right_wall
        ):  # moving right
            return True
        if (
            new_col < old_col and not self._cells[old_col][old_row].has_left_wall
        ):  # moving left
            return True
        if (
            new_row > old_row and not self._cells[old_col][old_row].has_bottom_wall
        ):  # moving down
            return True
        if (
            new_row < old_row and not self._cells[old_col][old_row].has_top_wall
        ):  # moving up
            return True
        return False
