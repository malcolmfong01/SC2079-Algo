import heapq
import math
from typing import List
import numpy as np
from entities.Robot import Robot
from entities.Entity import Obstacle, CellState, Grid
from consts import Direction, MOVE_DIRECTION, TURN_FACTOR, ITERATIONS, TURN_RADIUS, SAFE_COST
from python_tsp.exact import solve_tsp_dynamic_programming

class MazeSolver:
    def __init__(
            self,
            size_x: int,
            size_y: int,
            robot_x: int,
            robot_y: int,
            robot_direction: Direction,
            big_turn=None
    ):
        self.grid = Grid(size_x, size_y)
        self.robot = Robot(robot_x, robot_y, robot_direction)
        self.path_table = dict()
        self.cost_table = dict()

    def add_obstacle(self, x: int, y: int, direction: Direction, obstacle_id: int):
        obstacle = Obstacle(x, y, direction, obstacle_id)
        self.grid.add_obstacle(obstacle)

    def reset_obstacles(self):
        self.grid.reset_obstacles()

    @staticmethod
    def compute_coord_distance(x1: int, y1: int, x2: int, y2: int, level=1):
        horizontal_distance = x1 - x2
        vertical_distance = y1 - y2

        if level == 2:
            return math.sqrt(horizontal_distance ** 2 + vertical_distance ** 2)

        return abs(horizontal_distance) + abs(vertical_distance)

    @staticmethod
    def compute_state_distance(start_state: CellState, end_state: CellState, level=1):
        return MazeSolver.compute_coord_distance(start_state.x, start_state.y, end_state.x, end_state.y, level)

    @staticmethod
    def get_visit_options(n):
        s = []
        l = bin(2 ** n - 1).count('1')

        for i in range(2 ** n):
            s.append(bin(i)[2:].zfill(l))

        s.sort(key=lambda x: x.count('1'), reverse=True)
        return s

    def get_optimal_order_dp(self, retrying) -> List[CellState]:
        distance = 1e9
        optimal_path = []

        all_view_positions = self.grid.get_view_obstacle_positions(retrying)

        for op in self.get_visit_options(len(all_view_positions)):
            items = [self.robot.get_start_state()]
            cur_view_positions = []
            
            for idx in range(len(all_view_positions)):
                if op[idx] == '1':
                    items = items + all_view_positions[idx]
                    cur_view_positions.append(all_view_positions[idx])

            self.path_cost_generator(items)
            combination = []
            self.generate_combination(cur_view_positions, 0, [], combination, [ITERATIONS])

            for c in combination:
                visited_candidates = [0]

                cur_index = 1
                fixed_cost = 0
                for index, view_position in enumerate(cur_view_positions):
                    visited_candidates.append(cur_index + c[index])
                    fixed_cost += view_position[c[index]].penalty
                    cur_index += len(view_position)
                
                cost_np = np.zeros((len(visited_candidates), len(visited_candidates)))

                for s in range(len(visited_candidates) - 1):
                    for e in range(s + 1, len(visited_candidates)):
                        u = items[visited_candidates[s]]
                        v = items[visited_candidates[e]]
                        if (u, v) in self.cost_table.keys():
                            cost_np[s][e] = self.cost_table[(u, v)]
                        else:
                            cost_np[s][e] = 1e9
                        cost_np[e][s] = cost_np[s][e]
                cost_np[:, 0] = 0
                _permutation, _distance = solve_tsp_dynamic_programming(cost_np)
                if _distance + fixed_cost >= distance:
                    continue

                optimal_path = [items[0]]
                distance = _distance + fixed_cost

                for i in range(len(_permutation) - 1):
                    from_item = items[visited_candidates[_permutation[i]]]
                    to_item = items[visited_candidates[_permutation[i + 1]]]

                    cur_path = self.path_table[(from_item, to_item)]
                    for j in range(1, len(cur_path)):
                        optimal_path.append(CellState(cur_path[j][0], cur_path[j][1], cur_path[j][2]))

                    optimal_path[-1].set_screenshot(to_item.screenshot_id)

            if optimal_path:
                break

        return optimal_path, distance

    @staticmethod
    def generate_combination(view_positions, index, current, result, iteration_left):
        if index == len(view_positions):
            result.append(current[:])
            return

        if iteration_left[0] == 0:
            return

        iteration_left[0] -= 1
        for j in range(len(view_positions[index])):
            current.append(j)
            MazeSolver.generate_combination(view_positions, index + 1, current, result, iteration_left)
            current.pop()

    def get_safe_cost(self, x, y):
        for ob in self.grid.obstacles:
            if abs(ob.x-x) == 2 and abs(ob.y-y) == 2:
                return SAFE_COST
            
            if abs(ob.x-x) == 1 and abs(ob.y-y) == 2:
                return SAFE_COST
            
            if abs(ob.x-x) == 2 and abs(ob.y-y) == 1:
                return SAFE_COST

        return 0

    def get_turn_quadrant(self, from_direction: Direction, to_direction: Direction) -> int:
        if ((from_direction == Direction.NORTH and to_direction == Direction.EAST) or 
            (from_direction == Direction.WEST and to_direction == Direction.SOUTH)):
            return 1
        elif ((from_direction == Direction.NORTH and to_direction == Direction.WEST) or 
              (from_direction == Direction.EAST and to_direction == Direction.SOUTH)):
            return 2
        elif ((from_direction == Direction.SOUTH and to_direction == Direction.WEST) or 
              (from_direction == Direction.EAST and to_direction == Direction.NORTH)):
            return 3
        elif ((from_direction == Direction.SOUTH and to_direction == Direction.EAST) or 
              (from_direction == Direction.WEST and to_direction == Direction.NORTH)):
            return 4
        return 0

    def is_in_green_area(self, robot_x: int, robot_y: int, robot_dir: Direction, x: int, y: int, quadrant: int) -> bool:
        if TURN_RADIUS < 4:
            return False
            
        new_x = robot_x
        new_y = robot_y
        
        if quadrant == 1:
            if robot_dir == Direction.NORTH:
                new_x = robot_x + TURN_RADIUS
                new_y = robot_y + TURN_RADIUS
            elif robot_dir == Direction.WEST:
                new_x = robot_x - TURN_RADIUS
                new_y = robot_y - TURN_RADIUS
            green_x = max(robot_x, new_x)
            green_y = min(robot_y, new_y)

        elif quadrant == 2:
            if robot_dir == Direction.NORTH:
                new_x = robot_x - TURN_RADIUS
                new_y = robot_y + TURN_RADIUS
            elif robot_dir == Direction.EAST:
                new_x = robot_x + TURN_RADIUS
                new_y = robot_y - TURN_RADIUS
            green_x = min(robot_x, new_x)
            green_y = min(robot_y, new_y)

        elif quadrant == 3:
            if robot_dir == Direction.SOUTH:
                new_x = robot_x - TURN_RADIUS
                new_y = robot_y - TURN_RADIUS
            elif robot_dir == Direction.EAST:
                new_x = robot_x + TURN_RADIUS
                new_y = robot_y + TURN_RADIUS
            green_x = min(robot_x, new_x)
            green_y = max(robot_y, new_y)

        elif quadrant == 4:
            if robot_dir == Direction.SOUTH:
                new_x = robot_x + TURN_RADIUS
                new_y = robot_y - TURN_RADIUS
            elif robot_dir == Direction.WEST:
                new_x = robot_x - TURN_RADIUS
                new_y = robot_y + TURN_RADIUS
            green_x = max(robot_x, new_x)
            green_y = max(robot_y, new_y)
        else:
            return False

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (green_x + i == x) and (green_y + j == y):
                    return True
        return False

    def get_turn_area(self, current_x: int, current_y: int, robot_dir: Direction, to_direction: Direction) -> tuple:
        quadrant = self.get_turn_quadrant(robot_dir, to_direction)
        if quadrant == 0:
            return (0, 0, 0, 0)

        turn_x = current_x
        turn_y = current_y
        
        if quadrant == 1:
            if robot_dir == Direction.NORTH:
                turn_x = current_x + TURN_RADIUS
                turn_y = current_y + TURN_RADIUS
            elif robot_dir == Direction.WEST:
                turn_x = current_x - TURN_RADIUS
                turn_y = current_y - TURN_RADIUS

        elif quadrant == 2:
            if robot_dir == Direction.NORTH:
                turn_x = current_x - TURN_RADIUS
                turn_y = current_y + TURN_RADIUS
            elif robot_dir == Direction.EAST:
                turn_x = current_x + TURN_RADIUS
                turn_y = current_y - TURN_RADIUS

        elif quadrant == 3:
            if robot_dir == Direction.SOUTH:
                turn_x = current_x - TURN_RADIUS
                turn_y = current_y - TURN_RADIUS
            elif robot_dir == Direction.EAST:
                turn_x = current_x + TURN_RADIUS
                turn_y = current_y + TURN_RADIUS

        elif quadrant == 4:
            if robot_dir == Direction.SOUTH:
                turn_x = current_x + TURN_RADIUS
                turn_y = current_y - TURN_RADIUS
            elif robot_dir == Direction.WEST:
                turn_x = current_x - TURN_RADIUS
                turn_y = current_y + TURN_RADIUS

        smallest_x = min(current_x, turn_x) - 1
        smallest_y = min(current_y, turn_y) - 1
        biggest_x = max(current_x, turn_x) + 1
        biggest_y = max(current_y, turn_y) + 1

        return (smallest_x, smallest_y, biggest_x, biggest_y)

    def is_turn_valid(self, current_x: int, current_y: int, robot_dir: Direction, to_direction: Direction, obstacles: List[Obstacle]) -> bool:
        smallest_x, smallest_y, biggest_x, biggest_y = self.get_turn_area(current_x, current_y, robot_dir, to_direction)
        
        quadrant = self.get_turn_quadrant(robot_dir, to_direction)
        if quadrant == 0:
            return False

        for obstacle in obstacles:
            if (smallest_x <= obstacle.x <= biggest_x and 
                smallest_y <= obstacle.y <= biggest_y):
                if not self.is_in_green_area(current_x, current_y, robot_dir, obstacle.x, obstacle.y, quadrant):
                    return False
        
        return True

    def get_neighbors(self, x, y, direction):
        neighbors = []
        for dx, dy, md in MOVE_DIRECTION:
            if md == direction:
                if self.grid.reachable(x + dx, y + dy):
                    safe_cost = self.get_safe_cost(x + dx, y + dy)
                    neighbors.append((x + dx, y + dy, md, safe_cost))
                if self.grid.reachable(x - dx, y - dy):
                    safe_cost = self.get_safe_cost(x - dx, y - dy)
                    neighbors.append((x - dx, y - dy, md, safe_cost))

            else:
                quadrant = self.get_turn_quadrant(direction, md)
                if quadrant == 0:
                    continue

                turn_x = x
                turn_y = y
                
                if quadrant == 1:
                    if direction == Direction.NORTH:
                        turn_x = x + TURN_RADIUS
                        turn_y = y + TURN_RADIUS
                    elif direction == Direction.WEST:
                        turn_x = x - TURN_RADIUS
                        turn_y = y - TURN_RADIUS

                elif quadrant == 2:
                    if direction == Direction.NORTH:
                        turn_x = x - TURN_RADIUS
                        turn_y = y + TURN_RADIUS
                    elif direction == Direction.EAST:
                        turn_x = x + TURN_RADIUS
                        turn_y = y - TURN_RADIUS

                elif quadrant == 3:
                    if direction == Direction.SOUTH:
                        turn_x = x - TURN_RADIUS
                        turn_y = y - TURN_RADIUS
                    elif direction == Direction.EAST:
                        turn_x = x + TURN_RADIUS
                        turn_y = y + TURN_RADIUS

                elif quadrant == 4:
                    if direction == Direction.SOUTH:
                        turn_x = x + TURN_RADIUS
                        turn_y = y - TURN_RADIUS
                    elif direction == Direction.WEST:
                        turn_x = x - TURN_RADIUS
                        turn_y = y + TURN_RADIUS

                reachable = self.grid.reachable(turn_x, turn_y, turn=True)
                valid_turn = self.is_turn_valid(x, y, direction, md, self.grid.obstacles)
                
                if reachable and valid_turn:
                    safe_cost = self.get_safe_cost(turn_x, turn_y)
                    neighbors.append((turn_x, turn_y, md, safe_cost + 10))

        return neighbors

    def path_cost_generator(self, states: List[CellState]):
        def record_path(start, end, parent: dict, cost: int):
            self.cost_table[(start, end)] = cost
            self.cost_table[(end, start)] = cost

            path = []
            cursor = (end.x, end.y, end.direction)

            while cursor in parent:
                path.append(cursor)
                cursor = parent[cursor]

            path.append(cursor)

            self.path_table[(start, end)] = path[::-1]
            self.path_table[(end, start)] = path

        def astar_search(start: CellState, end: CellState):
            if (start, end) in self.path_table:
                return

            g_distance = {(start.x, start.y, start.direction): 0}
            heap = [(self.compute_state_distance(start, end), start.x, start.y, start.direction)]
            parent = dict()
            visited = set()

            while heap:
                _, cur_x, cur_y, cur_direction = heapq.heappop(heap)
                
                if (cur_x, cur_y, cur_direction) in visited:
                    continue

                if end.is_eq(cur_x, cur_y, cur_direction):
                    record_path(start, end, parent, g_distance[(cur_x, cur_y, cur_direction)])
                    return

                visited.add((cur_x, cur_y, cur_direction))
                cur_distance = g_distance[(cur_x, cur_y, cur_direction)]

                for next_x, next_y, new_direction, safe_cost in self.get_neighbors(cur_x, cur_y, cur_direction):
                    if (next_x, next_y, new_direction) in visited:
                        continue

                    move_cost = Direction.rotation_cost(new_direction, cur_direction) * TURN_FACTOR + 1 + safe_cost

                    next_cost = cur_distance + move_cost + \
                                self.compute_coord_distance(next_x, next_y, end.x, end.y)

                    if (next_x, next_y, new_direction) not in g_distance or \
                            g_distance[(next_x, next_y, new_direction)] > cur_distance + move_cost:
                        g_distance[(next_x, next_y, new_direction)] = cur_distance + move_cost
                        parent[(next_x, next_y, new_direction)] = (cur_x, cur_y, cur_direction)

                        heapq.heappush(heap, (next_cost, next_x, next_y, new_direction))

        for i in range(len(states) - 1):
            for j in range(i + 1, len(states)):
                astar_search(states[i], states[j])

if __name__ == "__main__":
    pass
