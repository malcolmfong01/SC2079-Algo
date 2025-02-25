import os
import json
from helper import load_input_from_file, process_path_finding, save_output_to_file

# Set to True if visualization is needed, False otherwise
ENABLE_VISUALIZATION = True

def save_visualization_data(result):
    """Save full result for visualization in misc folder"""
    misc_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'misc')
    temp_output_path = os.path.join(misc_dir, 'temp_output.json')
    with open(temp_output_path, 'w') as f:
        json.dump(result, f, indent=2)

def merge_consecutive_moves(commands):
    """Merge all consecutive identical commands between SNAPs"""
    merged = []
    current_cmd = None
    current_total = 0

    for cmd in commands:
        if cmd.startswith('SNAP') or cmd == 'FIN':
            if current_cmd:
                merged.append(f"{current_cmd}{current_total:03d}")
                current_cmd = None
                current_total = 0
            merged.append(cmd)
        elif cmd.startswith(('SF', 'SB', 'RF', 'RB', 'LF', 'LB')):
            cmd_type = cmd[:2]
            cmd_value = int(cmd[2:])
            if cmd_type == current_cmd:
                current_total += cmd_value
            else:
                if current_cmd:
                    merged.append(f"{current_cmd}{current_total:03d}")
                current_cmd = cmd_type
                current_total = cmd_value
        else:
            if current_cmd:
                merged.append(f"{current_cmd}{current_total:03d}")
                current_cmd = None
                current_total = 0
            merged.append(cmd)

    if current_cmd:
        merged.append(f"{current_cmd}{current_total:03d}")

    return merged

def main(input_file, output_file):
    """Main function for standalone path finding"""
    input_data = load_input_from_file(input_file)
    result = process_path_finding(input_data)
    
    # Save visualization data (set ENABLE_VISUALIZATION to False to disable)
    if ENABLE_VISUALIZATION:
        save_visualization_data(result)
    
    # Merge consecutive SF and SB commands for output file only
    merged_commands = merge_consecutive_moves(result['data']['commands'])
    
    # Save merged commands for output
    save_output_to_file(output_file, {'commands': merged_commands})

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <input_file> <output_file>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])
