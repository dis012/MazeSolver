from graphics import Window, Point, Line, Cell, Maze

def main():
    num_rows = 12
    num_cols = 12
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)

    maze.break_entrance_and_exit()

    maze.break_walls_r(0, 0)

    maze.reset_cells_visited()

    maze.solve_r()

    win.wait_for_close()

main()