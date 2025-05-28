# maize_reader.py

def load_maze(file_path):
    with open(file_path, 'r') as f:
        maze = [list(line.rstrip('\n')) for line in f]
    return maze

def find_player(maze):
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == 'P':
                return x, y
    return None