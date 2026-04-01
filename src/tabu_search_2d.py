import order_functions
import distance
import weight
import simulated_annealing_2d as sa
import random
from collections import deque


def generate_swap_neighbours(solution, n_samples=30):
    neighbors = []
    n = len(solution)

    for _ in range(n_samples):
        i, j = random.sample(range(n), 2)
        new_sol = solution.copy()
        new_sol[i], new_sol[j] = new_sol[j], new_sol[i]

        move = ("swap", min(i, j), max(i, j))
        neighbors.append((new_sol, move))

    return neighbors


def tabu_search_2d(
    shopping_list,
    J_product,
    initial_solution=None,
    tabu_tenure=100,
    max_iterations=1000,
    n_neighbors=30,
):
    if initial_solution is not None:
        current_solution = initial_solution.copy()
    else:
        current_solution = order_functions.generate_random_order(len(shopping_list))

    current_distance_cost = distance.compute_timecost_from_middle_indices_order(
        current_solution, J_product
    )
    current_weight_cost = weight.compute_weight_cost(current_solution, shopping_list)

    history_list = [(current_solution.copy(), current_distance_cost, current_weight_cost)]
    pareto_archive = [(current_solution.copy(), current_distance_cost, current_weight_cost)]

    tabu_list = deque(maxlen=tabu_tenure)

    for iteration in range(max_iterations):
        neighbors = generate_swap_neighbours(current_solution, n_neighbors)
        candidate_list = []

        for neighbor_solution, move in neighbors:
            neighbor_distance_cost = distance.compute_timecost_from_middle_indices_order(
                neighbor_solution, J_product
            )
            neighbor_weight_cost = weight.compute_weight_cost(
                neighbor_solution, shopping_list
            )

            is_tabu = move in tabu_list

            improves = sa.a_dominates_b(
                neighbor_weight_cost, current_weight_cost,
                neighbor_distance_cost, current_distance_cost
            )

            if not is_tabu or improves:
                candidate_list.append(
                    (neighbor_solution, neighbor_distance_cost, neighbor_weight_cost, move)
                )

        if not candidate_list:
            break

        dominating_candidates = [
            c for c in candidate_list
            if sa.a_dominates_b(c[2], current_weight_cost, c[1], current_distance_cost)
        ]

        if dominating_candidates:
            next_solution, next_distance_cost, next_weight_cost, chosen_move = random.choice(
                dominating_candidates
            )
        else:
            next_solution, next_distance_cost, next_weight_cost, chosen_move = min(
                candidate_list,
                key=lambda x: x[1] + x[2]
            )

        current_solution = next_solution
        current_distance_cost = next_distance_cost
        current_weight_cost = next_weight_cost

        history_list.append(
            (current_solution.copy(), current_distance_cost, current_weight_cost)
        )

        tabu_list.append(chosen_move)

        pareto_archive.append(
            (current_solution.copy(), current_distance_cost, current_weight_cost)
        )
        pareto_archive = [
            a for a in pareto_archive
            if not any(
                a != b and sa.a_dominates_b(b[2], a[2], b[1], a[1])
                for b in pareto_archive
            )
        ]

    return history_list, pareto_archive