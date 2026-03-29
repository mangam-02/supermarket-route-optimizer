import random
from shopping_list import ShoppingList
def get_complete_order(middle_indices_order):
        return [0]+list(middle_indices_order)+[int(max(middle_indices_order)+1)]

def get_path_from_middle_indices_order(order, product_path_matrix):
    order = get_complete_order(order)
    path = []
    for i in range(len(order)-1):
        path.append(product_path_matrix[order[i], order[i+1]])
    return path

def generate_random_order(number_of_products:int):
    order = list(range(1, number_of_products+1))
    random.shuffle(order)
    return order

def compute_neighbours1(order):
    neighbour_orders = []
    for i in range(len(order)-1):
        # For each neighbour switch two products which are next to each other
        # n being number of products on shopping list
        # n-1 neighbours -> O(n)
        new_order = order.copy()
        new_order[i], new_order[i+1] = new_order[i+1], new_order[i]
        neighbour_orders.append(new_order)
    return neighbour_orders

def compute_neighbours2(order):
    neighbour_orders = []
    for i in range(len(order)-1):
        for j in range(i,len(order)-1):
            # For each neighbour switch two products (must not be next to each other)
            # n being number of products on shopping list
            # -> (n-1)+(n-2)+...+1 = (n-1)*n/2 neighbours -> O(n^2)
            new_order = order.copy()
            new_order[i], new_order[j] = new_order[j], new_order[i]
            neighbour_orders.append(new_order)
    return neighbour_orders

def mutation(order):
    i = random.randint(0,len(order)-1)
    j = random.randint(0,len(order)-1)
    order[i], order[j] = order[j], order[i]
    return order

