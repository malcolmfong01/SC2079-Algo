import matplotlib.pyplot as plt
import numpy as np
from algo import MazeSolver
from consts import Direction, TURN_RADIUS

def visualize_turn_area(solver: MazeSolver, start_x: int, start_y: int, 
                       robot_dir: Direction, to_direction: Direction,
                       title: str = None):
    """
    Visualize the turn area, highlighting:
    - Turn area bounds (red rectangle)
    - Green area (3x3 square)
    - Robot position and direction arrows
    """
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Get the quadrant first
    quadrant = solver.get_turn_quadrant(robot_dir, to_direction)
    
    # Get the turn area bounds
    smallest_x, smallest_y, biggest_x, biggest_y = solver.get_turn_area(start_x, start_y, robot_dir, to_direction)
    
    # Calculate turn position based on quadrant and direction
    turn_x = start_x
    turn_y = start_y
    if quadrant == 1:  # Bottom right turn
        if robot_dir == Direction.NORTH:
            turn_x = start_x + TURN_RADIUS
            turn_y = start_y + TURN_RADIUS
        elif robot_dir == Direction.WEST:
            turn_x = start_x - TURN_RADIUS
            turn_y = start_y - TURN_RADIUS

    elif quadrant == 2:  # Bottom left turn
        if robot_dir == Direction.NORTH:
            turn_x = start_x - TURN_RADIUS
            turn_y = start_y + TURN_RADIUS
        elif robot_dir == Direction.EAST:
            turn_x = start_x + TURN_RADIUS
            turn_y = start_y - TURN_RADIUS

    elif quadrant == 3:  # South->West / East->North
        if robot_dir == Direction.SOUTH:
            turn_x = start_x - TURN_RADIUS
            turn_y = start_y - TURN_RADIUS
        elif robot_dir == Direction.EAST:
            turn_x = start_x + TURN_RADIUS
            turn_y = start_y + TURN_RADIUS

    elif quadrant == 4:  # South->East / West->North
        if robot_dir == Direction.SOUTH:
            turn_x = start_x + TURN_RADIUS
            turn_y = start_y - TURN_RADIUS
        elif robot_dir == Direction.WEST:
            turn_x = start_x - TURN_RADIUS
            turn_y = start_y + TURN_RADIUS

    # Set plot limits with simple padding
    padding = 2
    ax.set_xlim(smallest_x - padding, biggest_x + padding)
    ax.set_ylim(smallest_y - padding, biggest_y + padding)
    
    # Create grid with better styling
    ax.grid(True, linestyle='--', alpha=0.5, color='gray')
    ax.set_xticks(np.arange(smallest_x - padding, biggest_x + padding + 1))
    ax.set_yticks(np.arange(smallest_y - padding, biggest_y + padding + 1))
    
    # Add minor gridlines
    ax.grid(True, which='minor', linestyle=':', alpha=0.3, color='gray')
    ax.set_xticks(np.arange(smallest_x - padding - 0.5, biggest_x + padding + 1, 0.5), minor=True)
    ax.set_yticks(np.arange(smallest_y - padding - 0.5, biggest_y + padding + 1, 0.5), minor=True)
    
    # Make tick labels more visible
    ax.tick_params(axis='both', which='major', labelsize=8)
    
    # Plot turn area bounds (red rectangle)
    rect = plt.Rectangle((smallest_x, smallest_y), 
                        biggest_x - smallest_x, 
                        biggest_y - smallest_y,
                        fill=False, color='red', linewidth=2, label='Turn Area Bounds')
    ax.add_patch(rect)
    
    # Plot green area points
    green_x = []
    green_y = []
    for x in range(smallest_x-1, biggest_x+2):
        for y in range(smallest_y-1, biggest_y+2):
            if solver.is_in_green_area(start_x, start_y, robot_dir, x, y, quadrant):
                green_x.append(x)
                green_y.append(y)
    ax.scatter(green_x, green_y, color='green', alpha=0.3, s=100, label='Green Area')
    
    # Plot robot position and turn position
    ax.scatter([start_x], [start_y], color='blue', s=200, label='Robot Position')
    ax.scatter([turn_x], [turn_y], color='red', s=200, label='Turn Position')
    
    # Add direction labels directly beneath the dots
    ax.annotate(f'Start\n({robot_dir.name})', 
               xy=(start_x, start_y), 
               xytext=(start_x, start_y - 1),
               ha='center', va='top',
               bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='blue', alpha=0.9))
               
    ax.annotate(f'End\n({to_direction.name})', 
               xy=(turn_x, turn_y), 
               xytext=(turn_x, turn_y - 1),
               ha='center', va='top',
               bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='red', alpha=0.9))
    
    # Better axis labels
    ax.set_xlabel('X Coordinate', fontsize=10)
    ax.set_ylabel('Y Coordinate', fontsize=10)
    
    # Add curved arrow to show turn path
    # Calculate radius and angle based on quadrant and direction
    if quadrant == 1:  # Top Left Quadrant
        rad = -0.3 if robot_dir == Direction.NORTH else 0.3
    elif quadrant == 2:  # Bottom left turn
        rad = 0.3 if robot_dir == Direction.NORTH else -0.3
    elif quadrant == 3:  # South->West / East->North
        rad = -0.3 if robot_dir == Direction.SOUTH else 0.3  # East->North curves right
    elif quadrant == 4:  # South->East / West->North
        rad = 0.3 if robot_dir == Direction.SOUTH else -0.3  # West->North curves left
    else:
        rad = 0.3

    curve = plt.matplotlib.patches.ConnectionPatch(
        (start_x, start_y), (turn_x, turn_y),
        "data", "data",
        connectionstyle=f"arc3,rad={rad}",
        color='purple', linestyle='--', label='Turn Path'
    )
    ax.add_patch(curve)
    
    # Set title and labels
    if title:
        plt.title(title)
    else:
        plt.title(f'Turn Visualization: {robot_dir.name} → {to_direction.name}')
    plt.xlabel('X')
    plt.ylabel('Y')
    
    # Add legend
    plt.legend()
    
    # Set equal aspect ratio
    ax.set_aspect('equal')
    
    # Save the plot with quadrant number in filename
    if title:
        # Extract quadrant number from title
        q_num = title.split('(')[1].split(')')[0]
        plt.savefig(f'{q_num}_turn_visualization_{robot_dir.name}_to_{to_direction.name}.png')
    else:
        plt.savefig(f'turn_visualization_{robot_dir.name}_to_{to_direction.name}.png')
    plt.close(fig)

def test_all_turns():
    """Test and visualize all possible valid turns"""
    solver = MazeSolver(20, 20, 10, 10, Direction.NORTH)
    
    # Define all valid turns to test
    turns = [
        # Q1: North->East, West->South
        (Direction.NORTH, Direction.EAST, "North to East (Q1)"),
        (Direction.WEST, Direction.SOUTH, "West to South (Q1)"),
        
        # Q2: North->West, East->South
        (Direction.NORTH, Direction.WEST, "North to West (Q2)"),
        (Direction.EAST, Direction.SOUTH, "East to South (Q2)"),
        
        # Q3: South->West, East->North
        (Direction.SOUTH, Direction.WEST, "South to West (Q3)"),
        (Direction.EAST, Direction.NORTH, "East to North (Q3)"),
        
        # Q4: South->East, West->North
        (Direction.SOUTH, Direction.EAST, "South to East (Q4)"),
        (Direction.WEST, Direction.NORTH, "West to North (Q4)")
    ]
    
    # Create a figure for each turn
    for robot_dir, to_dir, title in turns:
        visualize_turn_area(solver, 10, 10, robot_dir, to_dir, title)
        print(f"Generated visualization for {robot_dir.name} to {to_dir.name}")

if __name__ == '__main__':
    test_all_turns()
