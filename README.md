# Maze Solver Game

A Python-based maze solving game where players navigate through a randomly generated maze to reach the end point. The game features a simple yet engaging interface built with Pygame.

## Features

- Randomly generated mazes using a recursive backtracking algorithm
- Smooth player movement with multiple control options
- Visual representation of the maze with different colors for walls, paths, start, and end points
- Win condition detection and celebration message
- Responsive controls with both arrow keys and WASD support

## How to Play

1. Run `game1.py` to start the game
2. Navigate the blue player through the maze to reach the red end point
3. Avoid the black walls and stay on the white paths
4. The game starts at the green 'S' point and ends at the red 'E' point

### Controls

- **Arrow Keys** or **WASD**: Move in four directions
- **Q, E, Z, C**: Move diagonally
- **Close Window**: Exit the game

## Technical Details

- The maze is generated using a recursive backtracking algorithm
- Maze size is 50x50 cells
- Each cell is represented by:
  - 0: Wall (black)
  - 1: Path (white)
  - 'S': Start point (green)
  - 'E': End point (red)
- Player is represented by a blue circle

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install pygame
   ```
3. Run the game:
   ```bash
   python game1.py
   ```

## Project Structure

- `game1.py`: Main game file containing the game loop and rendering logic
- `generate_maze.py`: Contains the maze generation algorithm

## License

This project is open source and available for personal and educational use.

## Contributing

Feel free to fork this repository and submit pull requests for any improvements or new features. 