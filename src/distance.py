import numpy as np
from supermarket import Zelle
from supermarket import Grid
import astar
from shopping_list import ShoppingList
from shopping_list import Product
import order_functions
import random
import distance

def compute_product_types_dict(grid:Grid, start_cell, end_cell):
    """
    Creates a dictionary mapping each product type in the grid to its cell coordinates.

    Keys:
        - "start": The starting cell (start_cell parameter)
        - "end": The ending cell (end_cell parameter)
        - All product types (as strings) found in the grid cells

    Values:
        - For "start" and "end": the coordinates (row, column) of the respective cell
        - For product types: a tuple (row, column) indicating the cell where the product type is located

    Procedure:
        1. Iterates over all cells in the 2D grid.
        2. Checks each side of the cell (N, E, S, W).
        3. If a side contains a product type (string), it is added as a key to the dictionary,
           with the value being the coordinates of the cell.
        4. Start and end cells are added as separate keys.

    Returns:
        - Dictionary containing start, end, and all found product types with their locations.
    """
    dict = {}
    dict["start"] = start_cell
    for (r, c), cell in np.ndenumerate(grid.grid):
        assert type(cell) == Zelle
        seiten = cell.seiten
        products_in_cell = []
        if type(seiten["N"]) == str:
            products_in_cell.append(seiten["N"])
        if type(seiten["E"]) == str:
            products_in_cell.append(seiten["E"])
        if type(seiten["S"]) == str:
            products_in_cell.append(seiten["S"])
        if type(seiten["W"]) == str:
            products_in_cell.append(seiten["W"])
        
        for product in products_in_cell:
            dict[product] = (r,c)
    dict["end"] = end_cell
    return dict

def compute_optimal_trajectories(grid:Grid, start_cell, end_cell):
    """
    Computes the optimal trajectories and their costs between all product types, 
    including the start and end cells, in a grid using the A* algorithm.

    Procedure:
        1. Generates a dictionary of product types and their cell coordinates 
           using `compute_product_types_dict`.
        2. Assigns a unique index to each product type for matrix representation.
        3. Initializes two square matrices:
            - `product_type_cost_matrix`: stores the path length (cost) between each pair of product types
            - `product_type_path_matrix`: stores the actual path (list of cell coordinates) between each pair
        4. Iterates over all pairs of product types (including start and end) and computes the shortest path 
           using the `astar` function.
        5. Stores the path cost and the path itself in the corresponding matrices.

    Returns:
        - product_type_cost_matrix: 2D NumPy array with path lengths between all product types
        - product_type_path_matrix: 2D NumPy array with paths (lists of coordinates) between all product types
        - product_type_indizes: dictionary mapping product type names to their matrix indices
    """
    product_types_dict = compute_product_types_dict(grid, start_cell, end_cell)
    number_of_product_types = len(product_types_dict)
    product_type_cost_matrix = np.empty((number_of_product_types, number_of_product_types), dtype=object)
    product_type_path_matrix = np.empty((number_of_product_types, number_of_product_types), dtype=object)
    product_type_indizes = {}
    i = 0
    for product in product_types_dict:
        product_type_indizes[product] = i
        i += 1
    for product_start in product_types_dict:
        for product_end in product_types_dict:
            path = astar.astar(grid, product_types_dict[product_start], product_types_dict[product_end])
            if path is not None:
                cost = len(path)-1
                product_type_cost_matrix[product_type_indizes[product_start], product_type_indizes[product_end]] = cost
                product_type_path_matrix[product_type_indizes[product_start], product_type_indizes[product_end]] = path
                #print(product_start, product_end, cost)
    return product_type_cost_matrix, product_type_path_matrix, product_type_indizes

def create_product_cost_path_matrix(shopping_list: ShoppingList, product_type_cost_matrix, product_type_path_matrix, product_type_indizes):
    """
    Creates cost and path matrices specifically for the products in a shopping list, 
    including the start and end points, by mapping from the full product type matrices.

    Procedure:
        1. Adds "start" and "end" to the shopping list.
        2. Initializes empty matrices for:
            - product_cost_matrix: stores the path length (cost) between each pair of shopping list items
            - product_path_matrix: stores the actual path (list of coordinates) between each pair
        3. Creates a mapping from shopping list item names to their indices in the matrices.
        4. Fills the matrices by looking up the costs and paths in the full product type matrices 
           using the corresponding product type indices.

    Parameters:
        - shopping_list: ShoppingList object containing Product instances
        - product_type_cost_matrix: full cost matrix for all product types (from compute_optimal_trajectories)
        - product_type_path_matrix: full path matrix for all product types
        - product_type_indizes: dictionary mapping product types to their indices in the full matrices

    Returns:
        - product_cost_matrix: 2D NumPy array with path lengths between shopping list items
        - product_path_matrix: 2D NumPy array with paths (lists of coordinates) between shopping list items
        - product_indizes: dictionary mapping shopping list item names to their indices in the returned matrices
    """
    # Add start and end as pseudo-products
    products = [Product("start", "start", 0, 0)] + shopping_list.products + [Product("end", "end", 0, 0)]

    number_of_products = len(products)
    product_cost_matrix = np.empty((number_of_products, number_of_products), dtype=object)
    product_path_matrix = np.empty((number_of_products, number_of_products), dtype=object)


    
    for i_start, prod_start in enumerate(products):
        for i_end, prod_end in enumerate(products):
            i_type_start = product_type_indizes[prod_start.category]
            i_type_end = product_type_indizes[prod_end.category]
            product_cost_matrix[i_start, i_end] = product_type_cost_matrix[i_type_start, i_type_end]
            product_path_matrix[i_start, i_end] = product_type_path_matrix[i_type_start, i_type_end]

    return product_cost_matrix, product_path_matrix

def compute_timecost_from_middle_indices_order(middle_indices_order, product_cost_matrix):
    # O(n)
    order = order_functions.get_complete_order(middle_indices_order)
    total_cost = 0
    for i in range(len(order)-1):
        total_cost += product_cost_matrix[order[i], order[i+1]]
    return total_cost

def generate_distancegreedy_random_order(J_product, alpha):
    J = J_product.copy()
    number_of_products = J.shape[0] - 2
    end_index = number_of_products + 1

    order = []
    current_index = 0
    for i in range(number_of_products):
        J_without_invalid_values = [J[current_index][j] for j in range(len(J[current_index])) if (j not in order) and (j != 0 and j != end_index)]# and (j != end_index)]
        minimum_cost = min(J_without_invalid_values)
        maximum_cost = max(J_without_invalid_values)
        cutoff_value = minimum_cost + alpha * (maximum_cost-minimum_cost)

        RCL_template = J[current_index] <= cutoff_value
        indizes = [j for j in range(len(RCL_template)) if RCL_template[j] and (j not in order) and (j != 0 and j != end_index)]# and (j != end_index)]
        winner_index = random.choice(indizes)

        order.append(winner_index)
        current_index = order[-1]
    return order

def local_search(J_product, printing = False, compute_neighbours_func = order_functions.compute_neighbours1, start_order = None):
    if printing:
        print("Starting local search:")
    number_of_products = J_product.shape[0]-2

    # If no start-order is given, create a random start-order
    if start_order is None:
        best_order = order_functions.generate_random_order(number_of_products)
        #best_order = get_complete_order(best_order, 0, number_of_products + 1)
    else:
        best_order = start_order
        #if best_order[0] != 0:
            #best_order = get_complete_order(best_order, 0, number_of_products + 1)
    
    no_better_order = True
    epoch = 1
    while no_better_order:
        # print(f"Epoch: {epoch}")
        # print(best_order)
        epoch += 1
        best_order_cost = compute_timecost_from_middle_indices_order(best_order, J_product)
        neighbours = compute_neighbours_func(best_order)
        #print(neighbours)
        neighbours_cost = [compute_timecost_from_middle_indices_order(neighbour, J_product) for neighbour in neighbours]
        best_neighbour_cost = min(neighbours_cost)
        if best_neighbour_cost < best_order_cost:
            best_neighbour_index = neighbours_cost.index(best_neighbour_cost)
            best_order = neighbours[best_neighbour_index]
            best_order_cost = best_neighbour_cost
        else:
            no_better_order = False
            if printing:
                print(f"No better neighbour found after {epoch} epochs")
                print(f"Best Order: {best_order}")
                print(f"Best Cost: {best_order_cost}")
                print()
    return best_order, best_order_cost

def GRASP(J_product, compute_neighbours_func, alpha = 0.5):
    start_order = distance.generate_distancegreedy_random_order(J_product, alpha)
    best_order, best_order_cost = local_search(J_product, compute_neighbours_func=compute_neighbours_func, start_order=start_order)
    return best_order, best_order_cost