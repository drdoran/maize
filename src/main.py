# main.py

import curses
import os
from maize_reader import load_maze, find_player

def move_player(pos, direction, maze):
    x, y = pos
    dx, dy = direction
    new_x, new_y = x + dx, y + dy
    if maze[new_y][new_x] != '#':
        return (new_x, new_y)
    return pos

def draw_maze(stdscr, maze, player_pos):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    for y, row in enumerate(maze):
        if y >= max_y:
            break
        for x, char in enumerate(row):
            if x >= max_x:
                break
            if (x, y) == player_pos:
                stdscr.addch(y, x, 'P', curses.A_BOLD)
            else:
                stdscr.addch(y, x, char)
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    maze = load_maze(os.path.join(os.path.dirname(__file__), "../data/maze.txt"))
    player_pos = find_player(maze)

    directions = {
        curses.KEY_UP: (0, -1),
        curses.KEY_DOWN: (0, 1),
        curses.KEY_LEFT: (-1, 0),
        curses.KEY_RIGHT: (1, 0),
        ord('w'): (0, -1),
        ord('s'): (0, 1),
        ord('a'): (-1, 0),
        ord('d'): (1, 0),
    }

    while True:
        draw_maze(stdscr, maze, player_pos)
        key = stdscr.getch()
        if key == ord('q'):
            break
        if key in directions:
            player_pos = move_player(player_pos, directions[key], maze)
            x, y = player_pos
            if maze[y][x] == 'E':
                stdscr.clear()
                stdscr.addstr(0, 0, "🎉 You reached the exit! Press any key to exit.")
                stdscr.refresh()
                stdscr.getch()
                break

if __name__ == "__main__":
    curses.wrapper(main)