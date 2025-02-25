import json
import os
import sys
import os.path as path

# Add the parent directory to the Python path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from consts import Direction

import os

def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_output_path = os.path.join(script_dir, 'temp_output.json')
    with open(temp_output_path) as f:
        data = json.load(f)
    path = data['data']['path']
    commands = data['data']['commands']
    return path, commands

def load_obstacles():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    input_path = os.path.join(root_dir, 'input.json')
    with open(input_path) as f:
        data = json.load(f)
    return [{'x': obs['x'], 'y': obs['y'], 'd': obs['d']} for obs in data['obstacles']]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_grid(step_number, commands, grid_size, obstacles, robot_pos, robot_dir, is_snapshot=False):
    grid = [['.' for _ in range(grid_size[0])] for _ in range(grid_size[1])]
    
    # Mark obstacles with inverted y-coordinates
    for obs in obstacles:
        x, y, direction = obs['x'], obs['y'], obs['d']
        if direction == Direction.NORTH:
            grid[19 - y][x] = 'U'
        elif direction == Direction.EAST:
            grid[19 - y][x] = 'R'
        elif direction == Direction.SOUTH:
            grid[19 - y][x] = 'B'
        elif direction == Direction.WEST:
            grid[19 - y][x] = 'L'
        elif direction == Direction.HIDDEN:
            grid[19 - y][x] = 'H'
    
    # Mark robot position with inverted y-coordinate
    x, y = robot_pos
    if is_snapshot:
        grid[19 - y][x] = 'O'
    else:
        if robot_dir == Direction.NORTH:
            grid[19 - y][x] = 'W'
        elif robot_dir == Direction.EAST:
            grid[19 - y][x] = 'D'
        elif robot_dir == Direction.SOUTH:
            grid[19 - y][x] = 'S'
        elif robot_dir == Direction.WEST:
            grid[19 - y][x] = 'A'
    
    # Print current command
    print(f"Next Execution: {commands[step_number]}\n")
    
    # Print grid with coordinates
    print("  " + " ".join(f"{i % 10}" for i in range(grid_size[0])))  # X-axis labels
    for idx, row in enumerate(grid):
        print(f"{(19 - idx) % 10} " + " ".join(row))  # Y-axis labels + grid row
    print()

def visualize_path():
    path, commands = load_data()
    obstacles = load_obstacles()
    grid_size = (20, 20)  # Assuming standard grid size

    step_number = 0
    for i, step in enumerate(path):
        clear_screen()
        display_grid(step_number, commands, grid_size, obstacles, (step['x'], step['y']), Direction(step['d']), False)
        print("\n" + "="*30 + "\n")
        input("Press Enter to continue...")
        step_number += 1
        
        if step['s'] > 0:
            clear_screen()
            display_grid(step_number, commands, grid_size, obstacles, (step['x'], step['y']), Direction(step['d']), True)
            print("\n" + "="*30 + "\n")
            input("Press Enter to continue...")
            step_number += 1

if __name__ == "__main__":
    visualize_path()
