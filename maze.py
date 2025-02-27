from cell import Cell
from graphics import Point, Line
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
        self._manual_solve_finished = False # add flag to track manual solve finish
        self._player_path_cells = []  # re-introduce and use to store path
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self._prev_player_col = (
            None  # keep track of previous player position for clearing
        )
        self._prev_player_row = None

    def _create_cells(self):
        self._cells = []
        for i in range(self._num_cols):
            self._cells.append([Cell(self._win) for _ in range(self._num_rows)])
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
        if (
            i == self._num_cols - 1 and j == self._num_rows - 1
        ):  # fill exit cell with green
            if self._win:
                self._win.draw_rect(x1, y1, x2, y2, "green")

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
        player_center_point = Point(center_x, center_y)
        line_color = "red"

        # check for backtracking and update line color and path
        is_backtracking = False
        if len(self._player_path_cells) >= 2:
            prev_path_point = self._player_path_cells[-2] # second to last point
            if prev_path_point.x == player_center_point.x and prev_path_point.y == player_center_point.y:
                line_color = "gray"
                is_backtracking = True


        # clear previous player path - by redrawing cells in the path - DRAW PATH *BEFORE* CLEARING CELLS
        if self._player_path_cells:
            for path_point in self._player_path_cells:
                cell_to_clear_col = int((path_point.x - self._x1) // self._cell_size_x)
                cell_to_clear_row = int((path_point.y - self._y1) // self._cell_size_y)
                if 0 <= cell_to_clear_col < self._num_cols and 0 <= cell_to_clear_row < self._num_rows: # bounds check
                    cell_to_clear = self._cells[cell_to_clear_col][cell_to_clear_row]
                    self._win.draw_rect(cell_to_clear._x1, cell_to_clear._y1, cell_to_clear._x2, cell_to_clear._y2, "white") # redraw with white to clear
                    self._draw_cell(cell_to_clear_col, cell_to_clear_row) # redraw walls


        # update path and draw polyline
        if is_backtracking:
            if len(self._player_path_cells) > 0:
                self._player_path_cells.pop() # remove last point on backtrack
        else:
            self._player_path_cells.append(player_center_point) # add current point if not backtracking

        # draw continuous line path - using polyline by unpacking all points
        if len(self._player_path_cells) >= 2:
            self._win.draw_polyline(self._player_path_cells, line_color)


        # draw player as a circle - for debugging, can switch back to line later if needed
        # player_center = Point(center_x, center_y)
        # self._win.draw_oval(player_center, player_radius, "red")

        # update previous player position
        self._prev_player_col = self._player_col
        self._prev_player_row = self._player_row

    def _on_key_press(self, event):
        if not self._manual_solve:
            return
        if self._manual_solve_finished: # check if manual solve is finished, if so, ignore keypresses
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
                    self._manual_solve_finished = True # set flag to stop further movement


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
