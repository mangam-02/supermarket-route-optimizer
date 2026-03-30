# Multi-Criteria Optimization for Shopping Lists in Supermarkets

![Pareto Evolution](src/assets/pareto_evolution.gif)

## Description

This project is part of the course "Multi-Criteria Optimization and Decision Analysis for Embedded Systems Design" at the Technical University Munich (TUM). It implements algorithms to optimize shopping lists in a simulated supermarket grid. The goal is to find the best order of products that minimizes multiple criteria:

- **Distance Cost**: The total length of the path through the supermarket.
- **Weight Cost**: Avoiding crushing by wrong stacking (heavy products at the bottom).
- **Hardness**: Similar to weight, but based on product hardness.

The optimization uses heuristics like GRASP, evolutionary algorithms, and Pareto ranking for multi-objective optimization.

## Installation and Requirements

### Prerequisites
- Python 3.x
- Jupyter Notebook (for interactive notebooks)

### Dependencies
The following Python packages are required (installable via `pip`):
- numpy
- matplotlib
- (additional from imports if necessary)

### Setup
1. Clone or download the repository.
2. Activate the virtual environment (if available):
   ```
   source venv/bin/activate
   ```
3. Install dependencies from requirements.txt:
   ```
   pip install -r requirements.txt
   ```
4. Start Jupyter Notebook:
   ```
   jupyter notebook
   ```

## Usage

### Main Notebooks
- `weight_hardness_optimization.ipynb`: The central notebook for multi-objective optimization. It loads the supermarket grid and shopping list, runs the evolution, and visualizes the Pareto fronts.
- `main.ipynb`: For single objective optimization experiments.
- `create_example_shopping_lists.ipynb`: For creating example shopping lists.
- `creating_supermarket_grid.ipynb`: For creating the supermarket grid.

### Example Execution
1. Open `weight_hardness_optimization.ipynb` in Jupyter.
2. Run the cells to load the grid and list.
3. Start the evolution for 2D (Distance + Weight) or 3D (Distance + Weight + Hardness).
4. Visualize the results and the optimal path.

### Data
- `grid.txt` / `grid_eng.txt`: The supermarket grid.
- `Long_shopping_list.txt` / `small_shopping_list.txt`: Example shopping lists.

## Project Structure

```
src
├── order_functions.py           # Functions to handle order processing
├── evolution.py                 # Main evolution algorithm logic
├── evolution_2d.py              # 2D-specific evolution routines
├── evolution_3d.py              # 3D-specific evolution routines
├── plotting.py                  # Functions for plotting results
├── optimization_1d.ipynb        # 1D optimization experiments
├── optimization_2d.ipynb        # 2D optimization experiments
├── optimization_3d.ipynb        # 3D optimization experiments
├── create_shopping_lists.ipynb  # Scripts to generate shopping lists
├── create_supermarket_grid.ipynb # Script to create supermarket grid
├── hardness.py                  # Functions for item hardness metrics
├── weight.py                     # Weight calculation utilities
├── distance.py                   # Distance calculation utilities
├── shopping_list.py              # Shopping list management
├── astar.py                      # A* pathfinding algorithm
├── decision_making.py            # Decision-making logic for agents
├── supermarket.py                # Supermarket environment definition
├── Long_shopping_list.txt        # Example long shopping list
├── small_shopping_list.txt       # Example small shopping list
├── grid.txt                       # Grid definition for tests
├── grid_eng.txt                   # Grid definition (English version)
└── assets                        # Images and gifs
    ├── pareto_evolution.gif      # Example Pareto evolution animation
    └── figures                   # Folder containing plot figures
```

## Algorithms and Methods

- **A***: For optimal pathfinding in the grid.
- **GRASP (Greedy Randomized Adaptive Search Procedure)**: For generating initial solutions with randomization and local search.
- **Local Search**: Used within GRASP to explore neighborhoods and improve solutions.
- **Evolutionary Algorithms**: With selection, crossover, mutation, and Pareto ranking for population-based optimization.
- **Greedy Heuristics**: Including weight-greedy, hardness-greedy, and distance-greedy algorithms for biased initial ordering.
- **Random Search**: For generating diverse random orders in the population.
- **Pareto Ranking**: For multi-objective optimization with crowding distance to maintain diversity.
- **Hypervolume**: To measure the quality and convergence of the Pareto front.

## Visualization

- 2D and 3D Pareto fronts with Matplotlib.
- Path visualization in the supermarket grid.
- Hypervolume plots for convergence.

## Authors

- Timo Matuszewski

## License

This project is created for educational purposes within the course. Please use it accordingly.

## Notes

- The notebooks are commented in German.
- For questions or improvements: Contact.