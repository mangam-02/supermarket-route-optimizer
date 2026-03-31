import numpy as np
import order_functions
import weight
import distance
import evolution_2d

def a_dominates_b(weight_cost_a, weight_cost_b, distance_cost_a, distance_cost_b):
    return (weight_cost_a < weight_cost_b and distance_cost_a <= distance_cost_b) or (weight_cost_a <= weight_cost_b and distance_cost_a < distance_cost_b)

def simulated_annealing_2d(shopping_list, J_product, initial_solution = None, initial_temperature=1000, cooling_rate=0.95, max_iterations=1000):
    if initial_solution:
        current_solution = initial_solution
    else:
        current_solution = order_functions.generate_random_order(len(shopping_list))
    current_distance_cost = distance.compute_timecost_from_middle_indices_order(current_solution, J_product)
    current_weight_cost = weight.compute_weight_cost(current_solution, shopping_list)
    history_list = [(current_solution, current_distance_cost, current_weight_cost)]

    temperature = initial_temperature
    for iteration in range(max_iterations):
        # Generate a neighboring solution
        neighbor_solution = order_functions.generate_random_neighbour(order_functions.compute_neighbours2, current_solution)

        # Calculate the cost of the neighboring solution
        neighbor_distance_cost = distance.compute_timecost_from_middle_indices_order(neighbor_solution, J_product)
        neighbor_weight_cost = weight.compute_weight_cost(neighbor_solution, shopping_list)
        
        # Decide whether to accept the neighboring solution
        p = np.exp(min([current_distance_cost - neighbor_distance_cost, current_weight_cost-neighbor_weight_cost]) / temperature)
        if a_dominates_b(neighbor_weight_cost, current_weight_cost, neighbor_distance_cost, current_distance_cost) or np.random.rand() < p:
            current_solution = neighbor_solution
            current_distance_cost = neighbor_distance_cost
            current_weight_cost = neighbor_weight_cost
            history_list.append((current_solution, current_distance_cost, current_weight_cost))

        # Cool down the temperature
        temperature *= cooling_rate

    return history_list