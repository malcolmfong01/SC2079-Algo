import os
import json
from helper import load_input_from_file, process_path_finding, save_output_to_file

def main(input_file, output_file):
    """Main function for standalone path finding"""
    input_data = load_input_from_file(input_file)
    result = process_path_finding(input_data)
    
    # Save full result for visualization in misc folder
    
    misc_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'misc')
    temp_output_path = os.path.join(misc_dir, 'temp_output.json')
    with open(temp_output_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    # Save commands for output
    save_output_to_file(output_file, {'commands': result['data']['commands']})

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <input_file> <output_file>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])
