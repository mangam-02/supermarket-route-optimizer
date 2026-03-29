import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
import plotting
import order_functions
import weight
import hardness
import distance
from shopping_list import ShoppingList
import hypervolume as hv
import evolution
import random

def pareto_rank_3_with_crowding(cost1, cost2, cost3):
    """
    Computes Pareto ranks for three objectives (minimization) and sorts
    solutions within each front by crowding distance (descending).

    Returns:
        - final_ranking: list of indices sorted by Pareto rank and crowding distance
        - ranks: list of Pareto ranks for each solution (rank 1 = best front)
        - crowding_distances: np.ndarray of crowding distances
    """
    n = len(cost1)
    assert n == len(cost2) == len(cost3)
    
    ranks = [-1] * n
    remaining = set(range(n))
    current_rank = 1
    fronts = []

    # Step 1: Identify Pareto fronts
    while remaining:
        current_front = []
        for i in remaining:
            dominated = False
            for j in remaining:
                if j == i:
                    continue
                if ((cost1[j] <= cost1[i] and cost2[j] <= cost2[i] and cost3[j] <= cost3[i]) and
                    (cost1[j] < cost1[i] or cost2[j] < cost2[i] or cost3[j] < cost3[i])):
                    dominated = True
                    break
            if not dominated:
                current_front.append(i)

        for i in current_front:
            ranks[i] = current_rank
            remaining.remove(i)

        fronts.append(current_front)
        current_rank += 1

    # Step 2: Compute crowding distance for each front
    crowding_distances = np.zeros(n)
    for front in fronts:
        if len(front) == 1:
            crowding_distances[front[0]] = float('inf')
            continue

        front_cost1 = np.array([cost1[i] for i in front])
        front_cost2 = np.array([cost2[i] for i in front])
        front_cost3 = np.array([cost3[i] for i in front])
        
        # Sort by each objective
        sorted1 = np.argsort(front_cost1)
        sorted2 = np.argsort(front_cost2)
        sorted3 = np.argsort(front_cost3)
        
        # Boundaries get infinite distance
        crowding_distances[front[sorted1[0]]] = float('inf')
        crowding_distances[front[sorted1[-1]]] = float('inf')
        crowding_distances[front[sorted2[0]]] = float('inf')
        crowding_distances[front[sorted2[-1]]] = float('inf')
        crowding_distances[front[sorted3[0]]] = float('inf')
        crowding_distances[front[sorted3[-1]]] = float('inf')
        
        # Normalize ranges
        norm1 = front_cost1.max() - front_cost1.min() or 1.0
        norm2 = front_cost2.max() - front_cost2.min() or 1.0
        norm3 = front_cost3.max() - front_cost3.min() or 1.0

        # Interior points
        for k in range(1, len(front)-1):
            crowding_distances[front[sorted1[k]]] += (front_cost1[sorted1[k+1]] - front_cost1[sorted1[k-1]]) / norm1
            crowding_distances[front[sorted2[k]]] += (front_cost2[sorted2[k+1]] - front_cost2[sorted2[k-1]]) / norm2
            crowding_distances[front[sorted3[k]]] += (front_cost3[sorted3[k+1]] - front_cost3[sorted3[k-1]]) / norm3

    # Step 3: Produce final ranking (rank ascending, crowding distance descending)
    all_indices = list(range(n))
    final_ranking = sorted(all_indices, key=lambda i: (ranks[i], -crowding_distances[i]))

    return final_ranking, ranks, crowding_distances

def plot_pareto_3(ranks, cost1, cost2, cost3,
                  xlabel="Cost 1", ylabel="Cost 2", zlabel="Cost 3",
                  max_legend_ranks=5, plot_high_ranks=True,
                  reference_point=None, saving_path = None):
    """
    3D Pareto Front Plot for 3 objectives.

    - First max_legend_ranks fronts get distinct colors + legend entry
    - Remaining fronts plotted in black with single legend entry "Rank ≥ max_legend_ranks"
    - reference_point: tuple/list (x, y, z) to mark a reference in red
    """
    max_rank = max(ranks)
    colors = [mcolors.hsv_to_rgb((i / max_legend_ranks, 0.85, 0.9)) for i in range(max_legend_ranks)]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    black_plotted = False

    for r in range(1, max_rank + 1):
        indices = [i for i in range(len(ranks)) if ranks[i] == r]
        xs = [cost1[i] for i in indices]
        ys = [cost2[i] for i in indices]
        zs = [cost3[i] for i in indices]

        if r < max_legend_ranks:
            ax.scatter(xs, ys, zs, color=colors[r], marker='x', label=f"Rank {r}")
        elif plot_high_ranks:
            label = f"Rank ≥ {max_legend_ranks}" if not black_plotted else None
            ax.scatter(xs, ys, zs, color="black", marker='x', label=label)
            black_plotted = True

    if reference_point is not None:
        ax.scatter(reference_point[0], reference_point[1], reference_point[2],
                   color="red", marker="x", s=100, label="Reference-point")
    # Set axes to start at 0
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.set_zlim(bottom=0)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)

    ax.set_title("3D Pareto Front")
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5))
    plt.tight_layout()
    if saving_path is not None:
        saving_path = plotting.check_saving_path(saving_path)
        plt.savefig(saving_path, bbox_inches="tight", dpi=400)

def initialize_population_3d(population_size, shopping_list, J_product):
    population = []
    for i in range(population_size):
        if i < 0.7*population_size:
            order = order_functions.generate_random_order(len(shopping_list))
        elif i < 0.8*population_size:
            order = weight.generate_weightgreedy_random_order(shopping_list, alpha = 0.5)
        elif i < 0.9*population_size:
            order = hardness.generate_hardness_greedy_order(shopping_list, alpha = 0.5)
        elif i < 0.93*population_size:
            order = distance.generate_distancegreedy_random_order(J_product, alpha = 0.5)
        elif i < 0.97*population_size:
            order,_ = distance.GRASP(J_product, compute_neighbours_func=order_functions.compute_neighbours2, alpha = 0.5)
        else:
            order,_ = distance.GRASP(J_product, compute_neighbours_func=order_functions.compute_neighbours2, alpha = 0.1)
        population.append(order)
    return population

def replacement_3d(population_size, ranking, population, pareto_front, pareto_ranks, crowding_distances, weight_costs, hardness_costs, distance_costs):
    # Reihenfolge nach Ranking
    sorted_indices = ranking[:population_size]  # top N indices
    
    # Population kürzen
    population = [population[i] for i in sorted_indices]
    pareto_ranks = [pareto_ranks[i] for i in sorted_indices]
    weight_costs = [weight_costs[i] for i in sorted_indices]
    hardness_costs = [hardness_costs[i] for i in sorted_indices]
    distance_costs = [distance_costs[i] for i in sorted_indices]
    crowding_distances = [crowding_distances[i] for i in sorted_indices]

    # Erste Pareto-Front aktualisieren
    min_rank = min(pareto_ranks)
    pareto_front = [population[i] for i, r in enumerate(pareto_ranks) if r == min_rank]

    # Ranking neu setzen (0..population_size-1)
    ranking = list(range(len(population)))

    return population, pareto_front, pareto_ranks, crowding_distances, ranking, weight_costs, hardness_costs, distance_costs

def evaluate_population_3d(population, shopping_list, J_product):
    # Compute Costs and ranking for population
    weight_costs = [weight.compute_weight_cost(order, shopping_list) for order in population]
    hardness_costs = [hardness.compute_hardness_cost(order, shopping_list) for order in population]
    distance_costs = [distance.compute_timecost_from_middle_indices_order(order, J_product) for order in population]

    ranking, pareto_ranks, crowding_distances = pareto_rank_3_with_crowding(distance_costs, weight_costs, hardness_costs)
    pareto_front_indices = [i for i, r in enumerate(pareto_ranks) if r == min(pareto_ranks)]
    pareto_front = [population[i] for i in pareto_front_indices]
    return ranking, pareto_front, pareto_ranks, crowding_distances, weight_costs, hardness_costs, distance_costs

def evolution_3d(shopping_list:ShoppingList, J_product, population_size = 100, generation_size = 10, patience = 10, mutation_probability = 0.5, max_generations = 200, reference_point = None):
    # Generate initial population
    # strategic Multi-Start-Heuristic
    population = initialize_population_3d(population_size, shopping_list, J_product)
    
    ranking, pareto_front, pareto_ranks, crowding_distances, weight_costs, hardness_costs, distance_costs = evaluate_population_3d(population, shopping_list, J_product)
    
    # Computation and set up of Hypervolume
    if reference_point == None:
        reference_point = (max(distance_costs)*1.1, max(weight_costs)*1.1)
    max_hypervolume = reference_point[0] * reference_point[1] * reference_point[2]
    epsilon = max_hypervolume * 0.001
    hypervolume = hv.hypervolume_3D(distance_costs, weight_costs, reference_point)
    hypervolume_list = [hypervolume]

    termination_criterion = False
    total_rounds = 0
    rounds_without_improvement = 0
    while not termination_criterion:
        if total_rounds == 0:
            plot_pareto_3(pareto_ranks, weight_costs, hardness_costs, distance_costs, xlabel="Weight cost", ylabel="Hardness cost", zlabel="Distance cost", max_legend_ranks=6, plot_high_ranks=True, reference_point=None)

        # Selection
        selected_population = evolution.simple_selection(ranking, population, generation_size)

        # Reproduction
        children = evolution.crossover_reproduction(selected_population)

        # Mutation
        mutation_rcl = [random.random() < mutation_probability for i in range(len(children))]
        children = [
            order_functions.mutation(children[i]) if mutation_rcl[i] else children[i]
            for i in range(len(children))
        ]        
        # Merging
        population = population + children
        population = evolution.remove_duplicates(population)

        # Evaluation
        ranking, pareto_front, pareto_ranks, crowding_distances, weight_costs, hardness_costs, distance_costs = evaluate_population_3d(population, shopping_list, J_product)
        # Replacement
        population, pareto_front, pareto_ranks, crowding_distances, ranking, weight_costs, hardness_costs, distance_costs = replacement_3d(population_size, ranking, population, pareto_front, pareto_ranks, crowding_distances, weight_costs, hardness_costs, distance_costs)
        new_hypervolume = hv.hypervolume_3D(distance_costs, weight_costs, hardness_costs, reference_point)
        # Termination criterion
        if new_hypervolume <= hypervolume + epsilon:
            rounds_without_improvement += 1
        else:
            rounds_without_improvement = 0
        hypervolume = new_hypervolume
        hypervolume_list.append(hypervolume)
        if total_rounds >= max_generations or rounds_without_improvement > patience:
            termination_criterion = True
        total_rounds += 1
        #print(f"[{total_rounds:3}/{max_generations}] - Hypervolume = {int(hypervolume)} - rounds without improvement = {rounds_without_improvement}")
    # Norm hypervolume
    hypervolume_list = [hypervolume/max_hypervolume for hypervolume in hypervolume_list]


    return population, pareto_ranks, ranking, weight_costs, hardness_costs, distance_costs, hypervolume_list, reference_point

def filter_best_pareto_rank(population, pareto_ranks, ranking, weight_costs, hardness_costs, distance_costs):
    # ---- Pareto Rank 1 filtern ----
    best_rank = min(pareto_ranks)
    pareto_indices = [i for i, r in enumerate(pareto_ranks) if r == best_rank]

    population = [population[i] for i in pareto_indices]
    weight_costs = [weight_costs[i] for i in pareto_indices]
    hardness_costs = [hardness_costs[i] for i in pareto_indices]
    distance_costs = [distance_costs[i] for i in pareto_indices]

    pareto_ranks = [pareto_ranks[i] for i in pareto_indices]
    ranking = list(range(len(population)))  # neues Ranking
    return population, pareto_ranks, ranking, weight_costs, hardness_costs, distance_costs