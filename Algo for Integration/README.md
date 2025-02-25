<br />
<p align="center">
  <h1 align="center">
    CZ3004/SC2079 Multidisciplinary Project - Algorithm
  </h1>
</p>

### Primers - Constants and Parameters

#### Direction of the robot (d)

- `NORTH` - `UP` : 0
- `EAST` - `RIGHT` : 2
- `SOUTH` - `DOWN` : 4
- `WEST` - `LEFT` : 6
- `HIDDEN (Only for Checklist A5)` - `UNKNOWN` : -1

#### Parameters

- `EXPANDED_CELL` - Size of an expanded cell, normally set to just 1 unit, but expanding it to 1.5 or 2 will allow the robot to have more space to move around the obstacle at the cost of it being harder to find a shortest path. Useful to tweak if robot is banging into obstacles.
- `WIDTH` - Width of the area (in 10cm units)
- `HEIGHT` - Height of the area (in 10cm units)
- `ITERATIONS` - Number of iterations to run the algorithm for. Higher number of iterations will result in a more accurate shortest path, but will take longer to run. Useful to tweak if robot is not finding the shortest path.
- `TURN_RADIUS` - Radius of turn (in 10cm units)
- `SAFE_COST` - Used to penalise the robot for moving too close to the obstacles. Currently set to `0`. Take a look at `get_safe_cost` to tweak.
- `SCREENSHOT_COST` - Used to penalise the robot for taking pictures from a position that is not directly in front of the symbol.

### API Endpoints:

Sample JSON request body:

```
{
    "obstacles": [
        {
            "x": 0,
            "y": 9,
            "id": 1,
            "d": 2
        },
        {
            "x": 19,
            "y": 14,
            "id": 2,
            "d": 6
        },
        {
            "x": 8,
            "y": 8,
            "id": 3,
            "d": 0
        },
        {
            "x": 18,
            "y": 6,
            "id": 4,
            "d": 4
        }
    ],
    "robot_x": 1,
    "robot_y": 1,
    "robot_dir": 0,
    "retrying": false
}

```

Sample JSON response:

```
{
  "commands": [
    "SF010",
    "RF090",
    "SF080",
    "SF010",
    "SNAP4",
    "LB090",
    "RB090",
    "SF080",
    "SF010",
    "SNAP2",
    "SB090",
    "RB090",
    "SF030",
    "RB090",
    "SF010",
    "SF010",
    "SNAP1",
    "SB020",
    "RF090",
    "SB010",
    "RF090",
    "SB020",
    "RF090",
    "SNAP3",
    "FIN"
  ]
}
```

#### Make sure to traverse into /Algo for Integration folder and run the following command in your terminal to get the above JSON response:

```bash
cd ./Algo\ for\ Integration/
```

Start the algorithm computing by:

```bash
python3 main.py input.json output.json
```

This will generate two files:

- `output.json`: Contains only the commands for the robot.
- `misc/temp_output.json`: Contains the full data structure including path and distance information (only if visualization is enabled).

To disable visualization output:

1. Open `main.py`
2. Set `ENABLE_VISUALIZATION = False` at the top of the file

For console visualisation (when enabled):

```bash
python3 misc/visualize_path.py
```

Note: The visualization script reads from `misc/temp_output.json`, so make sure to run the main script with visualization enabled before running the visualization. Run both commands from the project root directory.

Currently, TURN_RADIUS is set to 40cm (TURN_RADIUS = 4). To change this, you can modify the TURN_RADIUS variable in the const.py file.
