# main.py

import os
import sys
import termios
import tty
from maize_reader import load_maze, find_player
from rich.console import Console
from rich.text import Text

console = Console()

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch += sys.stdin.read(2)  # for arrow keys
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def print_maze(maze, player_pos):
    console.clear()
    for y, row in enumerate(maze):
        line = Text()
        for x, char in enumerate(row):
            if (x, y) == player_pos:
                line.append("P", style="bold yellow")
            elif char == '#':
                line.append("█", style="dim")
            elif char == 'E':
                line.append("E", style="bold green")
            else:
                line.append(" ")
        console.print(line)

def move(player_pos, direction, maze):
    x, y = player_pos
    dx, dy = direction
    new_x, new_y = x + dx, y + dy
    if maze[new_y][new_x] != '#':
        return new_x, new_y
    return player_pos

def main():
    maze = load_maze(os.path.join(os.path.dirname(__file__), "../data/maze.txt"))
    player_pos = find_player(maze)

    key_map = {
        'w': (0, -1), 's': (0, 1),
        'a': (-1, 0), 'd': (1, 0),
        '\x1b[A': (0, -1),
        '\x1b[B': (0, 1),
        '\x1b[D': (-1, 0),
        '\x1b[C': (1, 0),
    }

    while True:
        print_maze(maze, player_pos)
        key = get_key()
        if key == 'q':
            break
        if key in key_map:
            player_pos = move(player_pos, key_map[key], maze)
            x, y = player_pos
            if maze[y][x] == 'E':
                console.print("\n[bold green]You reached the exit![/bold green]\n")
                break

if __name__ == "__main__":
    main()