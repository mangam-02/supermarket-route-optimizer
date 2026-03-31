import numpy as np
import shopping_list
import evolution
import order_functions


def normalize_cost(cost_list):
    min_cost = min(cost_list)
    max_cost = max(cost_list)

    # vermeiden von Division durch 0
    if max_cost == min_cost:
        return [0.0 for _ in cost_list]

    normalized = [(c - min_cost) / (max_cost - min_cost) for c in cost_list]
    return normalized

def weighted_sum(normalized_costs: list, weights: list):  
    return np.array(normalized_costs) @ np.array(weights)

def weighted_sum_for_list(cost_lists: list, weights:list):
    return (np.array(weights) @ np.array(cost_lists)).tolist()

def summarize_results(population, pareto_ranks, ranking, weight_costs, hardness_costs, distance_costs, weights, P_product, grid, shopping_list):
    # Filter Pareto-Rank 1
    population, pareto_ranks, ranking, weight_costs, hardness_costs, distance_costs = evolution.filter_best_pareto_rank(population, pareto_ranks, ranking, weight_costs, hardness_costs, distance_costs)


    # Normalize Costs
    norm_distance_costs = normalize_cost(distance_costs)
    norm_weight_costs = normalize_cost(weight_costs)
    norm_hardness_costs = normalize_cost(hardness_costs)

    # Weighted sum
    scores = weighted_sum_for_list(cost_lists = [norm_distance_costs, norm_weight_costs, norm_hardness_costs], weights=weights)
    ind = scores.index(min(scores))
    #print(min(scores))

    # Order & Costs
    order = population[ind]
    distance_cost, norm_distance_cost = distance_costs[ind], norm_distance_costs[ind]
    weight_cost, norm_weight_cost = weight_costs[ind], norm_weight_costs[ind]
    hardness_cost, norm_hardness_cost = hardness_costs[ind], norm_hardness_costs[ind]
    print(f"ORDER COSTS: Distance = {distance_cost} ({round(norm_distance_cost,2)}) | Weight = {weight_cost} ({round(norm_weight_cost,2)}) | Hardness = {hardness_cost} ({round(norm_hardness_cost,2)})")

    # Products
    index_to_product = {v: k for k, v in shopping_list.product_indizes.items()}
    products_in_order = [index_to_product[i] for i in order]
    print(products_in_order)

    # Weight and Hardness
    # Mapping Name -> Produktobjekt
    product_lookup = {p.name: p for p in shopping_list.products}

    # Hardness und Weight in der gleichen Reihenfolge wie die Route
    weights_in_order = [product_lookup[name].weight for name in products_in_order]
    hardness_in_order = [product_lookup[name].hardness for name in products_in_order]

    label_width = 35  # Breite der Labels für Ausrichtung
    print(f"{'Weights in order:':<{label_width}} {weights_in_order}")
    print(f"{'Hardness in order:':<{label_width}} {hardness_in_order}")

    #Path
    path = order_functions.get_path_from_middle_indices_order(order, P_product)
    #print(path)

    # Mean path length
    path_length_between_each_step = [len(x)-1 for x in path]
    print(f"{'Distance between products:':<{label_width}} {path_length_between_each_step}")
    print(f"Mean path length between each step: {np.mean(path_length_between_each_step)}")

    # Plot
    saving_path = f"path_3d_d{distance_cost}_w{weight_cost}_h{hardness_cost}-d{weights[0]}_w{weights[1]}_h{weights[2]}.jpg"
    grid.plot(path, saving_path=saving_path)
