# Maze Game with AI Solver

A Python-based maze game with multiple maze generation algorithms and AI pathfinding solutions.

## Description

This project is a maze game where players navigate through randomly generated mazes. The game features:

- Random selection from 6 different maze generation patterns (standard, rhombus, brain, spiral, heart, and sphere)
- Player movement in 8 directions (up, down, left, right, and diagonals)
- Two AI pathfinding algorithms:
  - A* algorithm (optimal path finding)
  - BFS (Breadth-First Search) algorithm
- Visual representation of AI-calculated paths

## How to Play

1. Run the game with `python game1.py`
2. Use the following controls:
   - Arrow keys or WASD: Move in four directions (up, down, left, right)
   - Q, E, Z, C: Move diagonally
   - SPACE: Toggle A* algorithm path visualization
   - P: Toggle BFS algorithm path visualization

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/jaibhasin/maze-game.git
   ```

2. Install the required package:
   ```
   pip install pygame
   ```

3. Run the game:
   ```
   python game1.py
   ```

## Features

- **Multiple Maze Patterns**: Each time you play, the game randomly selects one of six different maze generation algorithms.
- **AI Solvers**: Press SPACE to see the optimal path using A* algorithm or P to see the path using BFS.
- **Win Detection**: The game detects when you reach the end point and displays a win message.

## Project Structure

- `game1.py`: Main game file with game logic, rendering, and AI algorithms
- `paths/`: Directory containing different maze generation algorithms:
  - `generate_maze.py`: Standard maze generator
  - `generate_maze_rhombus.py`: Rhombus-shaped maze generator
  - `generate_maze_brain.py`: Brain-shaped maze generator
  - `generate_maze_spiral.py`: Spiral-shaped maze generator
  - `generate_maze_heart.py`: Heart-shaped maze generator
  - `generate_maze_sphere.py`: Sphere-shaped maze generator

## License

[MIT License](https://opensource.org/licenses/MIT)

## Author

Jai Bhasin
