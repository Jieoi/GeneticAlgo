# GeneticAlgo

Welcome to the GeneticAlgo repository! This project is dedicated to harnessing the power of genetic algorithms for training robots, specifically focusing on improving their performance in the PyBullet environment. If you have a keen interest in evolutionary algorithms and robotics, you're exactly where you need to be.

## Project Focus
The primary objective of this project is to optimize the movement of robots within the PyBullet environment. The fitness function employed here quantifies the distance covered by the robot, as specified in the URDF (Unified Robot Description Format). This metric serves as a key indicator of the robot's performance and guides the evolutionary process.

## Getting Started
1. Run `starter.py` to set up the initial environment.
2. Visualize and interact with trained robots by loading your specific URDF file.

## Hello World Folder
Explore the `hello_world` folder for introductory training and trial files in both Python (`*.py`) and Jupyter Notebook (`*.ipynb`). These files provide a hands-on introduction to utilizing genetic algorithms in a simplified setting.

## Genetic Folder
The core of the repository resides in the `genetic` folder, containing the essential implementation of the genetic algorithm for robot training. Key components include:

- **`creature.py`**: Implements elitism to enhance evolutionary dynamics.
- **`genome.py`**: Includes functionality for saving to and reading from CSV for efficient data management.
- **`motor_test.py`**: Incorporates components of the fitness function related to distance traveled.
- **`population.py`**: Adds mutation for crossover, point/shrink/grow mutations.
- **`run_genome.py`**: Implements saving to and reading from CSV for genome data.
- **`simulation.py`**: Tests the system by running `test_ga.py` and saves training data.

## Test Files
Navigate to the `test` folder for various test files that validate the functionality of the genetic algorithm. Key ones include:

- **`test_creature.py`**: Generates a simple motor with a link.
- **`test_ga.py`**: Conducts thorough testing with results saved as CSV.
- **`test_genome.py`**: Includes saving to and reading from CSV for genome data.
- **`test_population.py`**: Adds a roulette wheel for parent selection.
- **`test_simulation.py`**: Integrates a roulette wheel for parent selection.

Feel free to explore the code, experiment with different configurations, and optimize your robot training experience!

Happy coding! 🤖✨
