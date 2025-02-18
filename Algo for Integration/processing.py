from consts import Direction, WIDTH, HEIGHT

def is_valid(x, y, direction):
    if direction == Direction.NORTH and y > 0:
        return True
    if direction == Direction.EAST and x < WIDTH - 1:
        return True
    if direction == Direction.SOUTH and y < HEIGHT - 1:
        return True
    if direction == Direction.WEST and x > 0:
        return True
    return False

def convert_hidden_obstacles(obstacles):
    new_obstacles = []
    for obstacle in obstacles:
        x, y, obstacle_id, direction = obstacle['x'], obstacle['y'], obstacle['id'], obstacle['d']
        if direction == Direction.HIDDEN:
            for dir in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]:
                if is_valid(x, y, dir):
                    new_obstacles.append({"x": x, "y": y, "id": obstacle_id, "d": dir})
        else:
            new_obstacles.append(obstacle)
    return new_obstacles