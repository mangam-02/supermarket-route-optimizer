# Multi-Criteria Optimization for Shopping Lists in Supermarkets

![Pareto Evolution](src/assets/pareto_evolution.gif)

## Description

Dieses Projekt ist Teil der Vorlesung "Multi-Criteria Optimization and Decision Analysis for Embedded Systems Design" an der TUM. Es implementiert Algorithmen zur Optimierung von Einkaufslisten in einem simulierten Supermarkt-Grid und betrachtet mehrere Zielfunktionen gleichzeitig (z. B. Distanz, Gewicht, Hardness).

## Installation und Requirements

### Voraussetzungen
- Python 3.x
- Jupyter Notebook (optional)

### Abhängigkeiten
Installiere die Abhängigkeiten mit:

```
pip install -r requirements.txt
```

### Setup
1. Repository klonen oder entpacken
2. Virtuelle Umgebung aktivieren (optional):
```
source venv/bin/activate
```
3. Abhängigkeiten installieren (s.o.)
````markdown
# Multi-Criteria Optimization for Shopping Lists in Supermarkets

![Pareto Evolution](src/assets/figures/pareto_evolution.gif)

## Description

This repository contains code for multi-criteria optimization of shopping lists in a simulated supermarket grid. It was developed for the course "Multi-Criteria Optimization and Decision Analysis for Embedded Systems Design" (TUM). The goal is to find product pickup orders that balance multiple objectives such as travel distance, stacking/weight constraints, and product hardness.

## Installation and Requirements

### Prerequisites
- Python 3.x
- Jupyter Notebook (optional)

### Dependencies
Install required Python packages with:

```
pip install -r requirements.txt
```

### Setup
1. Clone or download the repository.
2. (Optional) Activate a virtual environment:

```
source venv/bin/activate
```

3. Install dependencies as shown above.
4. Start Jupyter Notebook if you want to run the notebooks interactively:

```
jupyter notebook
```

## Notebooks and Examples
Key notebooks located in `src/`:
- `optimization_1d.ipynb`
- `optimization_2d.ipynb`  (contains simulated annealing and Pareto visualizations)
- `optimization_3d.ipynb`
- `create_shopping_lists.ipynb`
- `create_supermarket_grid.ipynb`

To run: open the notebook and execute cells in order. `optimization_2d.ipynb` demonstrates 2D optimization (distance vs. weight) and plotting utilities.

## Data
- Supermarket grids: `src/supermarket-grids/grid.txt`, `src/supermarket-grids/grid_eng.txt`
- Shopping lists: `src/shopping-lists/Long_shopping_list.txt`, `src/shopping-lists/small_shopping_list.txt`

## Project Structure

```
README.md
requirements.txt
src/
├── astar.py
├── assets/
│   └── figures/
├── create_shopping_lists.ipynb
├── create_supermarket_grid.ipynb
├── creating_gif.py
├── decision_making.py
├── distance.py
├── evolution.py
├── evolution_2d.py
├── evolution_3d.py
├── hardness.py
├── hypervolume.py
├── optimization_1d.ipynb
├── optimization_2d.ipynb
├── optimization_3d.ipynb
├── order_functions.py
├── plotting.py
├── simulated_annealing_2d.py
├── shopping_list.py
├── supermarket.py
├── shopping-lists/
│   ├── Long_shopping_list.txt
│   └── small_shopping_list.txt
├── supermarket-grids/
│   ├── grid.txt
│   └── grid_eng.txt
└── weight.py

assets/ (project-wide assets if needed outside `src`)
```

## Algorithms and Methods

- A* for pathfinding inside the grid
- GRASP and greedy heuristics for generating biased initial orders
- Local search (swap operations) for neighborhood exploration
- Evolutionary algorithms with Pareto ranking and crowding distance to maintain diversity
- Hypervolume calculation to assess Pareto-front quality

## Visualization

- 2D Pareto plots (Distance vs Weight)
- 3D Pareto plots (Distance vs Weight vs Hardness)
- Path visualization inside the supermarket grid
- Hypervolume plots for convergence analysis

## Author

- Timo Matuszewski

## License

This project was developed for educational purposes. Please follow your institution's guidelines for reuse.

## Notes

- Most notebooks contain German comments and explanations.
- If you have questions or suggestions, please get in touch.
````