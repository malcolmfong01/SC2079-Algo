import json
from consts import Direction

def load_input(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_input(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def update_input(file_path, obstacle_id, new_robot_x, new_robot_y, new_robot_dir):
    input_data = load_input(file_path)
    
    # Remove the obstacle with the specified ID
    input_data['obstacles'] = [obs for obs in input_data['obstacles'] if obs['id'] != obstacle_id]
    
    # Update the robot's position and direction
    input_data['robot_x'] = new_robot_x
    input_data['robot_y'] = new_robot_y
    input_data['robot_dir'] = new_robot_dir.value  # Assuming Direction is an enum
    
    save_input(input_data, file_path)

if __name__ == "__main__":
    input_file_path = '/Users/mal/Documents/codes/SC2079-Algo/Algo for Integration/input.json'
    
    # Example usage
    obstacle_id_to_remove = 1
    new_robot_x = 5
    new_robot_y = 5
    new_robot_dir = Direction.NORTH  # Assuming Direction is an enum
    
    update_input(input_file_path, obstacle_id_to_remove, new_robot_x, new_robot_y, new_robot_dir)