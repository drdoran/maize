# main.py

import os
import sys
import termios
import tty
from maize_reader import load_maze, find_player

def get_key():
    """Get a single character from standard input (Unix only)."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch += sys.stdin.read(2)  # For arrow keys
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def print_maze(maze, player_pos):
    os.system('clear')
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if (x, y) == player_pos:
                print('P', end='')
            else:
                print(char, end='')
        print()

def move(player_pos, direction, maze):
    x, y = player_pos
    dx, dy = direction
    new_x, new_y = x + dx, y + dy
    if maze[new_y][new_x] != '#':
        return new_x, new_y
    return player_pos

def main():
    maze = load_maze("maze.txt")
    player_pos = find_player(maze)

    key_map = {
        'w': (0, -1), 's': (0, 1),
        'a': (-1, 0), 'd': (1, 0),
        '\x1b[A': (0, -1),  # Up arrow
        '\x1b[B': (0, 1),   # Down arrow
        '\x1b[D': (-1, 0),  # Left arrow
        '\x1b[C': (1, 0),   # Right arrow
    }

    while True:
        print_maze(maze, player_pos)
        key = get_key()
        if key == 'q':
            break
        if key in key_map:
            player_pos = move(player_pos, key_map[key], maze)

if __name__ == "__main__":
    main()