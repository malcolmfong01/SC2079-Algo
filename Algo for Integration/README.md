<br />
<p align="center">
  <h1 align="center">
    CZ3004/SC2079 Multidisciplinary Project - Algorithm API
  </h1>
</p>

### Primers - Constants and Parameters

#### Direction of the robot (d)

- `NORTH` - `UP` - 0
- `EAST` - `RIGHT` - 2
- `SOUTH` - `DOWN` - 4
- `WEST` - `LEFT` 6

#### Parameters

- `EXPANDED_CELL` - Size of an expanded cell, normally set to just 1 unit, but expanding it to 1.5 or 2 will allow the robot to have more space to move around the obstacle at the cost of it being harder to find a shortest path. Useful to tweak if robot is banging into obstacles.
- `WIDTH` - Width of the area (in 10cm units)
- `HEIGHT` - Height of the area (in 10cm units)
- `ITERATIONS` - Number of iterations to run the algorithm for. Higher number of iterations will result in a more accurate shortest path, but will take longer to run. Useful to tweak if robot is not finding the shortest path.
- `TURN_RADIUS` - Number of units the robot turns. We set the turns to `3 * TURN_RADIUS, 1 * TURN_RADIUS` units. Can be tweaked in the algorithm
- `SAFE_COST` - Used to penalise the robot for moving too close to the obstacles. Currently set to `1000`. Take a look at `get_safe_cost` to tweak.
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
  "data": {
    "commands": [
      "FW30",
      "FR00",
      "FW20",
      "BL00",
      "BL00",
      "SNAP1",
      "BW10",
      "FR00",
      "FW20",
      "BR00",
      "BR00",
      "SNAP3",
      "BW30",
      "FL00",
      "FW40",
      "SNAP2",
      "FW10",
      "BR00",
      "BW70",
      "BR00",
      "BW10",
      "BL00",
      "SNAP4",
      "FIN"
    ],
    "distance": 154.0,
    "path": [
      {
        "x": 1,
        "y": 1,
        "d": 0,
        "s": -1
      },
      {
        "x": 1,
        "y": 4,
        "d": 0,
        "s": -1
      },
      {
        "x": 4,
        "y": 5,
        "d": 2,
        "s": -1
      },
      {
        "x": 6,
        "y": 5,
        "d": 2,
        "s": -1
      },
      {
        "x": 3,
        "y": 6,
        "d": 4,
        "s": -1
      },
      {
        "x": 4,
        "y": 9,
        "d": 6,
        "s": 1
      },
      {
        "x": 5,
        "y": 9,
        "d": 6,
        "s": -1
      },
      {
        "x": 4,
        "y": 12,
        "d": 0,
        "s": -1
      },
      {
        "x": 4,
        "y": 14,
        "d": 0,
        "s": -1
      },
      {
        "x": 5,
        "y": 11,
        "d": 6,
        "s": -1
      },
      {
        "x": 8,
        "y": 12,
        "d": 4,
        "s": 3
      },
      {
        "x": 8,
        "y": 15,
        "d": 4,
        "s": -1
      },
      {
        "x": 11,
        "y": 14,
        "d": 2,
        "s": -1
      },
      {
        "x": 15,
        "y": 14,
        "d": 2,
        "s": 2
      },
      {
        "x": 16,
        "y": 14,
        "d": 2,
        "s": -1
      },
      {
        "x": 13,
        "y": 13,
        "d": 0,
        "s": -1
      },
      {
        "x": 13,
        "y": 6,
        "d": 0,
        "s": -1
      },
      {
        "x": 14,
        "y": 3,
        "d": 6,
        "s": -1
      },
      {
        "x": 15,
        "y": 3,
        "d": 6,
        "s": -1
      },
      {
        "x": 18,
        "y": 2,
        "d": 0,
        "s": 4
      }
    ]
  },
  "error": null
}
```

#### Make sure to traverse into Algo for Integration folder and run the following command in your terminal to get the above JSON response:

Start the algorithm computing by

```bash
python3 main.py input.json output.json
```

For console visualisation:

```bash
python3 visualise.py output.json
```
