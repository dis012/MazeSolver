from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height):
        """
        Initialize the window and canvas.
        """
        self.root = Tk()
        self.root.title("The maze")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.root, bg='white', width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=1)
        self.is_running = False

    def redraw(self):
        """
        Redraw the window.
        """
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        """
        Run the main loop until the window is closed.
        """
        self.is_running = True
        while self.is_running:
            self.redraw()
        print("You have closed the window")

    def draw_line(self, line, fill_color="black"):
        """
        Draw a line on the canvas.
        """
        line.draw(self.canvas, fill_color)
        self.redraw()  # Make sure to refresh after drawing

    def close(self):
        """
        Close the window.
        """
        self.is_running = False
        self.root.destroy()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, A, B):
        self.p1 = A
        self.p2 = B

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)

class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win
        self.visited = False # This is how we track which cells have had their walls broken

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, "white")

        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, "white")

        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, "white")

        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        if undo:
            color = "grey"
        else:
            color = "red"

        x1 = (self._x1 + self._x2)/2
        y1 = (self._y1 + self._y2)/2

        x2 = (to_cell._x1 + to_cell._x2)/2
        y2 = (to_cell._y1 + to_cell._y2)/2

        line = Line(Point(x1, y1), Point(x2, y2))
        self._win.draw_line(line, color)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed = None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.cells = []
        self.seed = seed
        if self.seed is not None:
            random.seed(self.seed) 
        self.create_cells()

    def create_cells(self):
        self.cells = [
            [Cell(self.win) for _ in range(self.num_cols)] for _ in  range(self.num_rows)
        ]
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.draw_cell(i,j)

    def draw_cell(self, i, j):
        if self.win is None:
            return
        
        x1 = self.x1 + j * self.cell_size_x
        y1 = self.y1 + i * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y

        self.cells[i][j].draw(x1, y1, x2, y2)
        self.animate()

    def animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.05)

    def break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self.draw_cell(0, 0)
        i = len(self.cells) - 1
        j = len(self.cells[0]) - 1
        self.cells[i][j].has_bottom_wall = False
        self.draw_cell(i,j)

    def break_walls_r(self, i, j):
        current = self.cells[i][j]
        current.visited = True

        while True:
            unviseted_neighboor = {}

            # Get all the neighbors
            # Up
            if i > 0 and not self.cells[i-1][j].visited:
                #unviseted_neighboor.append(self.cells[i-1][j])
                unviseted_neighboor["up"] = (i-1, j)

            # Down
            if i < self.num_rows-1 and not self.cells[i+1][j].visited:
                #unviseted_neighboor.append(self.cells[i+1][j])
                unviseted_neighboor["down"] = (i+1, j)

            # Left
            if j > 0 and not self.cells[i][j-1].visited:
                #unviseted_neighboor.append(self.cells[i][j-1])
                unviseted_neighboor["left"] = (i, j-1)

            # Right
            if j < self.num_cols - 1 and not self.cells[i][j+1].visited:
                #unviseted_neighboor.append(self.cells[i][j+1])
                unviseted_neighboor["right"] = (i, j+1)

            # Base case
            if not unviseted_neighboor:
                self.draw_cell(i, j)
                return
            
            direction = random.choice(list(unviseted_neighboor.keys()))

            next_i, next_j = unviseted_neighboor[direction]

            if direction == "up":
                current.has_top_wall = False
                self.cells[next_i][next_j].has_bottom_wall = False

            if direction == "down":
                current.has_bottom_wall = False
                self.cells[next_i][next_j].has_top_wall = False

            if direction == "left":
                current.has_left_wall = False
                self.cells[next_i][next_j].has_right_wall = False

            if direction == "right":
                current.has_right_wall = False
                self.cells[next_i][next_j].has_left_wall = False

            self.break_walls_r(next_i, next_j)
    
    def reset_cells_visited(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False
                
    
    def solve_r(self, i=0, j=0):
        self.animate()
        current = self.cells[i][j]
        current.visited = True

        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True
        

        if not current.has_right_wall and not self.cells[i][j+1].visited:
            current.draw_move(self.cells[i][j+1])
            if self.solve_r(i, j+1):
                return True
            else:
                current.draw_move(self.cells[i][j+1], undo=True)

        if not current.has_left_wall and not self.cells[i][j-1].visited:
            current.draw_move(self.cells[i][j-1])
            if self.solve_r(i, j-1):
                return True
            else:
                current.draw_move(self.cells[i][j-1], undo=True)

        if not current.has_top_wall and not self.cells[i-1][j].visited:
            current.draw_move(self.cells[i-1][j])
            if self.solve_r(i-1, j):
                return True
            else:
                current.draw_move(self.cells[i-1][j], undo=True)

        if not current.has_bottom_wall and not self.cells[i+1][j].visited:
            current.draw_move(self.cells[i+1][j])
            if self.solve_r(i+1, j):
                return True
            else:
                current.draw_move(self.cells[i+1][j], undo=True)



        return False