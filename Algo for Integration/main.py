import json
from algo import MazeSolver
from consts import Direction
from Entity import CellState

def load_input_from_file(input_file):
    """Load input data from JSON file"""
    with open(input_file, 'r') as f:
        return json.load(f)

def save_output_to_file(output_file, result):
    """Save output data to JSON file"""
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

def filter_states(path):
    """Filter the states to include only necessary states"""
    filtered_path = []
    start_state = path[0]
    filtered_path.append(start_state)
    
    for i in range(1, len(path)):
        prev_state = path[i - 1]
        current_state = path[i]
        
        # Always include states with snapshots
        if current_state['s'] != -1:
            filtered_path.append(current_state)
            continue
        
        # Check if there is a turn based on direction change
        if prev_state['d'] != current_state['d']:
            # Add the last state of the straight path
            filtered_path.append(prev_state)
            # Add the first state after the turn
            filtered_path.append(current_state)
        elif i == len(path) - 1:
            # Add the last state of the path
            filtered_path.append(current_state)
        else:
            # Check if the current state is part of a straight path
            if (prev_state['x'] != current_state['x'] or prev_state['y'] != current_state['y']):
                # Only add the current state if it's the end of a straight path
                if i < len(path) - 1:
                    next_state = path[i + 1]
                    if current_state['d'] != next_state['d']:
                        filtered_path.append(current_state)
                else:
                    filtered_path.append(current_state)
    
    # Ensure the end state is included
    if filtered_path[-1] != path[-1]:
        filtered_path.append(path[-1])
    
    # Remove duplicates
    unique_filtered_path = []
    seen = set()
    for state in filtered_path:
        state_tuple = (state['x'], state['y'], state['d'], state['s'])
        if state_tuple not in seen:
            unique_filtered_path.append(state)
            seen.add(state_tuple)
    
    return unique_filtered_path

def generate_commands(path):
    """Generate command sequence from path"""
    commands = []
    prev_state = path[0]
    current_direction = prev_state['d']
    start_x, start_y = prev_state['x'], prev_state['y']
    
    for state in path[1:]:
        # Calculate movement distance
        dx = state['x'] - start_x
        dy = state['y'] - start_y
        
        # Check if direction changes
        if state['d'] != current_direction:
            # Determine turn type
            if (current_direction == 0 and state['d'] == 2) or \
               (current_direction == 2 and state['d'] == 4) or \
               (current_direction == 4 and state['d'] == 6) or \
               (current_direction == 6 and state['d'] == 0):
                # Clockwise turn
                if (current_direction == 0 and dx > 0) or \
                   (current_direction == 2 and dy < 0) or \
                   (current_direction == 4 and dx < 0) or \
                   (current_direction == 6 and dy > 0):
                    turn_command = "FR00"
                else:
                    turn_command = "BL00"
            elif (current_direction == 0 and state['d'] == 6) or \
                 (current_direction == 6 and state['d'] == 4) or \
                 (current_direction == 4 and state['d'] == 2) or \
                 (current_direction == 2 and state['d'] == 0):
                # Counterclockwise turn
                if (current_direction == 0 and dx < 0) or \
                   (current_direction == 2 and dy > 0) or \
                   (current_direction == 4 and dx > 0) or \
                   (current_direction == 6 and dy < 0):
                    turn_command = "FL00"
                else:
                    turn_command = "BR00"
            
            # Emit turn command
            commands.append(turn_command)
            
            # Handle snapshots
            if state['s'] != -1:
                commands.append(f"SNAP{state['s']}")
            
            # Reset start position and update direction
            start_x, start_y = state['x'], state['y']
            current_direction = state['d']
            continue
        
        # Determine movement command
        if state['d'] == current_direction:
            # Forward movement
            if (current_direction == 0 and dy > 0) or \
               (current_direction == 2 and dx > 0) or \
               (current_direction == 4 and dy < 0) or \
               (current_direction == 6 and dx < 0):
                distance = (abs(dx) if dx != 0 else abs(dy)) * 10
                commands.append(f"FW{distance:02d}")
            # Backward movement
            else:
                distance = (abs(dx) if dx != 0 else abs(dy)) * 10
                commands.append(f"BW{distance:02d}")
        
        # Handle snapshots
        if state['s'] != -1:
            commands.append(f"SNAP{state['s']}")
        
        # Update start position
        start_x, start_y = state['x'], state['y']
    
    commands.append("FIN")
    return commands

def process_path_finding(input_data):
    """Process path finding using existing algorithm"""
    obstacles = input_data['obstacles']
    robot_x, robot_y = input_data['robot_x'], input_data['robot_y']
    robot_direction = Direction(input_data['robot_dir'])
    retrying = input_data.get('retrying', False)

    maze_solver = MazeSolver(20, 20, robot_x, robot_y, robot_direction)
    
    for ob in obstacles:
        maze_solver.add_obstacle(ob['x'], ob['y'], Direction(ob['d']), ob['id'])

    optimal_path, distance = maze_solver.get_optimal_order_dp(retrying=retrying)
    path = [state.get_dict() for state in optimal_path]
    
    # Filter the states before generating commands
    filtered_path = filter_states(path)
    
    commands = generate_commands(filtered_path)
    
    return {
        "data": {
            'commands': commands,
            'distance': distance,
            'path': filtered_path
        },
        "error": None
    }

def main(input_file, output_file):
    """Main function for standalone path finding"""
    input_data = load_input_from_file(input_file)
    result = process_path_finding(input_data)
    save_output_to_file(output_file, result)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 standalone_path_finder.py <input_file> <output_file>")
        sys.exit(1)
        
    main(sys.argv[1], sys.argv[2])

# run this code: python3 main.py input.json output.json