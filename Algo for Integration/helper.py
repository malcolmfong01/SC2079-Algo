import json
from algo import MazeSolver
from consts import WIDTH, HEIGHT, Direction
from processing import convert_hidden_obstacles

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
    
    i = 1
    while i < len(path):
        current_state = path[i]
        prev_state = filtered_path[-1]  # Always compare with last filtered state
        
        # Always include snapshots
        if current_state['s'] != -1:
            filtered_path.append(current_state)
            i += 1
            continue
        
        # For straight line movement
        if current_state['d'] == prev_state['d']:
            # Look ahead to find where straight line ends
            straight_end = i
            while straight_end < len(path) - 1:
                next_state = path[straight_end + 1]
                # Stop if direction changes or snapshot
                if next_state['d'] != current_state['d'] or next_state['s'] != -1:
                    break
                straight_end += 1
            
            # Only add state if there's actual movement
            end_state = path[straight_end]
            if (end_state['x'] != prev_state['x'] or end_state['y'] != prev_state['y']):
                filtered_path.append(end_state)
            i = straight_end + 1
            continue
        
        # For direction changes
        if current_state['d'] != prev_state['d']:
            # Look ahead to see if this turn leads to movement
            next_idx = i + 1
            while next_idx < len(path):
                next_state = path[next_idx]
                if (next_state['x'] != current_state['x'] or 
                    next_state['y'] != current_state['y'] or
                    next_state['s'] != -1):
                    filtered_path.append(current_state)
                    break
                if next_state['d'] != current_state['d']:
                    break
                next_idx += 1
            
        i += 1
    
    return filtered_path

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
            angle = 90  # Default 90-degree turn
            if (current_direction == 0 and state['d'] == 2) or \
               (current_direction == 2 and state['d'] == 4) or \
               (current_direction == 4 and state['d'] == 6) or \
               (current_direction == 6 and state['d'] == 0):
                # Clockwise turn
                if (current_direction == 0 and dx > 0) or \
                   (current_direction == 2 and dy < 0) or \
                   (current_direction == 4 and dx < 0) or \
                   (current_direction == 6 and dy > 0):
                    # Convert FR00 to RF090
                    turn_command = f"RF{angle:03d}"
                else:
                    # Convert BL00 to LB090
                    turn_command = f"LB{angle:03d}"
            elif (current_direction == 0 and state['d'] == 6) or \
                 (current_direction == 6 and state['d'] == 4) or \
                 (current_direction == 4 and state['d'] == 2) or \
                 (current_direction == 2 and state['d'] == 0):
                # Counterclockwise turn
                if (current_direction == 0 and dx < 0) or \
                   (current_direction == 2 and dy > 0) or \
                   (current_direction == 4 and dx > 0) or \
                   (current_direction == 6 and dy < 0):
                    # Convert FL00 to LF090
                    turn_command = f"LF{angle:03d}"
                else:
                    # Convert BR00 to RB090
                    turn_command = f"RB{angle:03d}"
            
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
            # Calculate distance in cm
            distance = (abs(dx) if dx != 0 else abs(dy)) * 10
            
            # Forward movement
            if (current_direction == 0 and dy > 0) or \
               (current_direction == 2 and dx > 0) or \
               (current_direction == 4 and dy < 0) or \
               (current_direction == 6 and dx < 0):
                # Convert FWxx to SFxxx
                commands.append(f"SF{distance:03d}")
            # Backward movement
            else:
                # Convert BWxx to SBxxx
                commands.append(f"SB{distance:03d}")
        
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

    # Convert hidden obstacles
    obstacles = convert_hidden_obstacles(obstacles)

    maze_solver = MazeSolver(WIDTH, HEIGHT, robot_x, robot_y, robot_direction)
    
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
