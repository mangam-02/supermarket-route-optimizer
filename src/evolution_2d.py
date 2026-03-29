import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import plotting
import weight
import distance
import order_functions
from shopping_list import ShoppingList
import hypervolume as hp
import evolution

def pareto_rank_2_with_crowding(cost1, cost2):
    """
    Computes Pareto ranks for two objectives (minimization) and sorts
    solutions within each front by crowding distance (descending).

    Returns:
        - final_ranking: list of indices sorted by Pareto rank and crowding distance
        - ranks: list of Pareto ranks for each solution (rank 0 = best front)
    """
    n = len(cost1)
    assert n == len(cost2)
    
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
                if (cost1[j] <= cost1[i] and cost2[j] <= cost2[i]) and \
                   (cost1[j] < cost1[i] or cost2[j] < cost2[i]):
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
        
        # Sort by each objective
        sorted1 = np.argsort(front_cost1)
        sorted2 = np.argsort(front_cost2)
        
        # Boundaries get infinite distance
        crowding_distances[front[sorted1[0]]] = float('inf')
        crowding_distances[front[sorted1[-1]]] = float('inf')
        crowding_distances[front[sorted2[0]]] = float('inf')
        crowding_distances[front[sorted2[-1]]] = float('inf')
        
        # Normalize ranges
        norm1 = front_cost1.max() - front_cost1.min() or 1.0
        norm2 = front_cost2.max() - front_cost2.min() or 1.0

        # Interior points
        for k in range(1, len(front)-1):
            crowding_distances[front[sorted1[k]]] += (front_cost1[sorted1[k+1]] - front_cost1[sorted1[k-1]]) / norm1
            crowding_distances[front[sorted2[k]]] += (front_cost2[sorted2[k+1]] - front_cost2[sorted2[k-1]]) / norm2

    # Step 3: Produce final ranking (rank ascending, crowding distance descending)
    all_indices = list(range(n))
    final_ranking = sorted(all_indices, key=lambda i: (ranks[i], -crowding_distances[i]))

    return final_ranking, ranks, crowding_distances

def plot_pareto_2(ranks, costx, costy, xlabel = "Cost x", ylabel = "Cost y", max_legend_ranks=5, plot_high_ranks = True, reference_point = None, saving_path = None):
    """
    Uses pareto_rank_2 and plots Pareto fronts.
    
    - First max_legend_ranks fronts get distinct colors + legend entry
    - Remaining fronts are plotted in black with a single legend entry "Rank > max_legend_ranks-1"
    """
    max_rank = max(ranks)
    num_fronts = max_rank

    # Farben nur für die ersten expliziten Fronten erzeugen
    colors = [
        mcolors.hsv_to_rgb((i / max_legend_ranks, 0.85, 0.9))
        for i in range(max_legend_ranks)
    ]

    plt.figure()
    black_plotted = False  # Flag, damit schwarzes Label nur einmal in der Legende erscheint
    for r in range(1,num_fronts+1):
        indices = [i for i in range(len(ranks)) if ranks[i] == r]
        x_vals = [costx[i] for i in indices]
        y_vals = [costy[i] for i in indices]

        if r < max_legend_ranks:
            plt.scatter(
                x_vals,
                y_vals,
                color=colors[r],
                label=f"Rank {r}",
                marker="x"
            )
        elif plot_high_ranks:
            label = f"Rank ≥ {max_legend_ranks}" if not black_plotted else None
            plt.scatter(
                x_vals,
                y_vals,
                color="black",
                marker="x",
                label=label
            )
            black_plotted = True
    if reference_point is not None:
        plt.scatter(
            reference_point[0],
            reference_point[1],
            color="red",
            marker="x",
            s=100,
            label="Reference-point"
        )
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title("Pareto Front")
    plt.legend(
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        borderaxespad=0
        )
    plt.tight_layout()
    if saving_path is not None:
        saving_path = plotting.check_saving_path(saving_path)
        plt.savefig(saving_path, bbox_inches="tight", dpi=300)

def initialize_population_2d(population_size, shopping_list, J_product):
    population, population_label = [], []
    for i in range(population_size):
        if i < 0.7*population_size:
            order = order_functions.generate_random_order(len(shopping_list))
            label = "random"
        elif i < 0.8*population_size:
            order = weight.generate_weightgreedy_random_order(shopping_list, alpha = 0.5)
            label = "weight-greedy"
        elif i < 0.9*population_size:
            order = distance.generate_distancegreedy_random_order(J_product, alpha = 0.5)
            label = "distance-greedy"
        elif i < 0.95*population_size:
            order,_ = distance.GRASP(J_product, compute_neighbours_func=order_functions.compute_neighbours2, alpha = 0.5)
            label = "GRASP (α = 0.5)"
        else:
            order,_ = distance.GRASP(J_product, compute_neighbours_func=order_functions.compute_neighbours2, alpha = 0.1)
            label = "GRASP (α = 0.1)"
        population.append(order)
        population_label.append(label)
    return population, population_label

def replacement_2d(population_size, ranking, population, pareto_front, pareto_ranks, crowding_distances, weight_costs, distance_costs):
    # Reihenfolge nach Ranking
    sorted_indices = ranking[:population_size]  # top N indices
    
    # Population kürzen
    population = [population[i] for i in sorted_indices]
    pareto_ranks = [pareto_ranks[i] for i in sorted_indices]
    weight_costs = [weight_costs[i] for i in sorted_indices]
    distance_costs = [distance_costs[i] for i in sorted_indices]
    crowding_distances = [crowding_distances[i] for i in sorted_indices]

    # Erste Pareto-Front aktualisieren
    min_rank = min(pareto_ranks)
    pareto_front = [population[i] for i, r in enumerate(pareto_ranks) if r == min_rank]

    # Ranking neu setzen (0..population_size-1)
    ranking = list(range(len(population)))

    return population, pareto_front, pareto_ranks, crowding_distances, ranking, weight_costs, distance_costs

def evaluate_population_2d(population, shopping_list, J_product):
    # Compute Costs and ranking for population
    weight_costs = [weight.compute_weight_cost(order, shopping_list) for order in population]
    distance_costs = [distance.compute_timecost_from_middle_indices_order(order, J_product) for order in population]
    ranking, pareto_ranks, crowding_distances = pareto_rank_2_with_crowding(distance_costs, weight_costs)
    pareto_front_indices = [i for i, r in enumerate(pareto_ranks) if r == min(pareto_ranks)]
    pareto_front = [population[i] for i in pareto_front_indices]
    return ranking, pareto_front, pareto_ranks, crowding_distances, weight_costs, distance_costs

def evolution_2d(shopping_list:ShoppingList, J_product, population_size = 100, generation_size = 10, patience = 10, mutation_probability = 0.5, max_generations = 200, reference_point = None, history=False):
    if history:
        history_list = []
    # Generate initial population
    # strategic Multi-Start-Heuristic
    population, _ = initialize_population_2d(population_size, shopping_list, J_product)
    
    ranking, pareto_front, pareto_ranks, crowding_distances, weight_costs, distance_costs = evaluate_population_2d(population, shopping_list, J_product)
    if history:
        history_list.append({
            "pareto_ranks": pareto_ranks.copy(),
            "weight_costs": weight_costs.copy(),
            "distance_costs": distance_costs.copy()
        })


    # Computation and set up of Hypervolume
    if reference_point == None:
        reference_point = (max(distance_costs)*1.1, max(weight_costs)*1.1)
    max_hypervolume = reference_point[0] * reference_point[1]
    epsilon = max_hypervolume * 0.001
    hypervolume = hp.hypervolume_2D(distance_costs, weight_costs, reference_point)
    hypervolume_list = [hypervolume]

    termination_criterion = False
    total_rounds = 0
    rounds_without_improvement = 0
    while not termination_criterion:
        if total_rounds == 0:
            plot_pareto_2(pareto_ranks, distance_costs, weight_costs, xlabel="Distance cost", ylabel="Weight cost", max_legend_ranks=6, plot_high_ranks=True, reference_point=None, saving_path="initial_pareto_plot.jpg")

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
        ranking, pareto_front, pareto_ranks, crowding_distances, weight_costs, distance_costs = evaluate_population_2d(population, shopping_list, J_product)

        # Replacement
        population, pareto_front, pareto_ranks, crowding_distances, ranking, weight_costs, distance_costs = replacement_2d(population_size, ranking, population, pareto_front, pareto_ranks, crowding_distances, weight_costs, distance_costs)

        if history:
            history_list.append({
                "pareto_ranks": pareto_ranks.copy(),
                "weight_costs": weight_costs.copy(),
                "distance_costs": distance_costs.copy()
            })

        new_hypervolume = hp.hypervolume_2D(distance_costs, weight_costs, reference_point)
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

    if history:
        return population, pareto_ranks, weight_costs, distance_costs, hypervolume_list, reference_point, history_list
    else:
        return population, pareto_ranks, weight_costs, distance_costs, hypervolume_list, reference_point
    
