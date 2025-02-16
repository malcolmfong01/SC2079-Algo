import json
import os
from time import sleep

def load_path():
    with open('output.json') as f:
        data = json.load(f)
    path = data['data']['path']
    commands = data['data']['commands']
    # Pair each path step with its command
    for i, step in enumerate(path):
        if i < len(commands):
            step['command'] = commands[i]
        else:
            step['command'] = 'FIN'  # Default to FIN if no command
    return path

def load_obstacles():
    with open('sample_input.json') as f:
        data = json.load(f)
    return [{'x': obs['x'], 'y': obs['y']} for obs in data['obstacles']]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_grid(grid_size, obstacles, robot_pos):
    grid = [['.' for _ in range(grid_size[0])] for _ in range(grid_size[1])]
    
    # Mark obstacles with inverted y-coordinates
    for obs in obstacles:
        grid[19 - obs['y']][obs['x']] = 'X'
    
    # Mark robot position with inverted y-coordinate
    x, y = robot_pos
    grid[19 - y][x] = 'R'
    
    # Print grid with coordinates
    print("   " + " ".join(f"{i:2}" for i in range(grid_size[0])))  # X-axis labels
    for idx, row in enumerate(grid):
        print(f"{19 - idx:2} " + " ".join(row))  # Y-axis labels + grid row
    print()

def visualize_path():
    path = load_path()
    obstacles = load_obstacles()
    grid_size = (20, 20)  # Assuming standard grid size
    
    for step in path:
        clear_screen()
        if 'command' in step:
            print(f"\nExecuting: {step['command']}\n")
        else:
            print("\nExecuting: Unknown command\n")
        display_grid(grid_size, obstacles, (step['x'], step['y']))
        print("\n" + "="*30 + "\n")
        input("Press Enter to continue...")

if __name__ == "__main__":
    visualize_path()
