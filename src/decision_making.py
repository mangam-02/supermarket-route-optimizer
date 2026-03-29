import numpy as np

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

