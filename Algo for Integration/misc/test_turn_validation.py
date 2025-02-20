import unittest
from algo import MazeSolver
from Entity import Obstacle
from consts import Direction

class TestTurnValidation(unittest.TestCase):
    def setUp(self):
        # Initialize a MazeSolver instance for testing
        self.solver = MazeSolver(20, 20, 10, 10, Direction.NORTH)

    def test_get_turn_quadrant(self):
        """Test the quadrant determination for different turn combinations"""
        # Test quadrant 1: north->east / west->south
        self.assertEqual(self.solver.get_turn_quadrant(Direction.NORTH, Direction.EAST), 1)
        self.assertEqual(self.solver.get_turn_quadrant(Direction.WEST, Direction.SOUTH), 1)

        # Test quadrant 2: north->west / east->south
        self.assertEqual(self.solver.get_turn_quadrant(Direction.NORTH, Direction.WEST), 2)
        self.assertEqual(self.solver.get_turn_quadrant(Direction.EAST, Direction.SOUTH), 2)

        # Test quadrant 3: south->east / west->north
        self.assertEqual(self.solver.get_turn_quadrant(Direction.SOUTH, Direction.EAST), 3)
        self.assertEqual(self.solver.get_turn_quadrant(Direction.WEST, Direction.NORTH), 3)

        # Test quadrant 4: south->west / east->north
        self.assertEqual(self.solver.get_turn_quadrant(Direction.SOUTH, Direction.WEST), 4)
        self.assertEqual(self.solver.get_turn_quadrant(Direction.EAST, Direction.NORTH), 4)

        # Test invalid turn
        self.assertEqual(self.solver.get_turn_quadrant(Direction.NORTH, Direction.SOUTH), 0)

    def test_is_in_green_area(self):
        """Test the green area detection for different quadrants"""
        # Test quadrant 1 (bottom right green area)
        self.assertTrue(self.solver.is_in_green_area(2, -2, Direction.NORTH, Direction.EAST))
        self.assertFalse(self.solver.is_in_green_area(0, 0, Direction.NORTH, Direction.EAST))

        # Test quadrant 2 (bottom left green area)
        self.assertTrue(self.solver.is_in_green_area(-2, -2, Direction.NORTH, Direction.WEST))
        self.assertFalse(self.solver.is_in_green_area(0, 0, Direction.NORTH, Direction.WEST))

        # Test quadrant 3 (top right green area)
        self.assertTrue(self.solver.is_in_green_area(2, 2, Direction.SOUTH, Direction.EAST))
        self.assertFalse(self.solver.is_in_green_area(0, 0, Direction.SOUTH, Direction.EAST))

        # Test quadrant 4 (top left green area)
        self.assertTrue(self.solver.is_in_green_area(-2, 2, Direction.SOUTH, Direction.WEST))
        self.assertFalse(self.solver.is_in_green_area(0, 0, Direction.SOUTH, Direction.WEST))

    def test_get_turn_area(self):
        """Test the turn area calculation"""
        # Test turn area for north->east (quadrant 1)
        area = self.solver.get_turn_area(10, 10, Direction.NORTH, Direction.EAST)
        self.assertTrue(len(area) > 0)
        # Verify green area points are not included
        self.assertNotIn((12, 8), area)  # Point in green area
        self.assertIn((13, 10), area)    # Point outside green area

    def test_is_turn_valid(self):
        """Test turn validation with obstacles"""
        # Add an obstacle in the turn area
        self.solver.add_obstacle(12, 8, Direction.NORTH, 1)
        
        # Test turn validation
        # Should be valid when no obstacles in path
        self.assertTrue(self.solver.is_turn_valid(10, 10, Direction.NORTH, Direction.EAST, []))
        
        # Should be invalid when obstacle in path (but not in green area)
        obstacles = [Obstacle(13, 10, Direction.NORTH, 1)]
        self.assertFalse(self.solver.is_turn_valid(10, 10, Direction.NORTH, Direction.EAST, obstacles))
        
        # Should be valid when obstacle is in green area
        obstacles = [Obstacle(12, 8, Direction.NORTH, 1)]
        self.assertTrue(self.solver.is_turn_valid(10, 10, Direction.NORTH, Direction.EAST, obstacles))

if __name__ == '__main__':
    unittest.main()
