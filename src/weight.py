from shopping_list import ShoppingList
import random

def compute_weight_cost(order, shopping_list: ShoppingList):
    """
    Crushing penalty:
    If a heavier product is packed later (thus lies on top)
    of a lighter product, a penalty proportional to the
    weight difference is added.
    
    Cost = 0  -> perfectly sorted heavy -> light
    """
    assert len(order) == len(shopping_list)

    total_cost = 0
    weights_list = []

    for i in range(len(order)):
        product_idx_bottom = order[i]-1 # -1 because order goes from 1 to n but in products we use the index, which starts with 0
        weight_bottom = shopping_list.products[product_idx_bottom].weight
        weights_list.append(weight_bottom)
        for j in range(i + 1, len(order)):
            product_idx_top = order[j]-1 # -1 because order goes from 1 to n but in products we use the index, which starts with 0
            weight_top = shopping_list.products[product_idx_top].weight

            # crushing condition: heavier on top of lighter
            if weight_top > weight_bottom:
                total_cost += (weight_top - weight_bottom)
    #print(f"Weights: {weights_list}")
    return total_cost

def generate_weightgreedy_random_order(shopping_list: ShoppingList, alpha=0.5):
    products = shopping_list.products
    n = len(products)

    order = []
    remaining_product_indices = list(range(0, n))  # Produkt-Indizes

    for _ in range(n):
        # Gewichte der noch nicht gewählten Produkte
        weights = [products[i].weight for i in remaining_product_indices]

        max_weight = max(weights)
        min_weight = min(weights)

        # Für heavy-first: obere Grenze definieren
        cutoff_value = max_weight - alpha * (max_weight - min_weight)

        # RCL: alle Produkte mit Gewicht >= cutoff
        rcl = [i for i in remaining_product_indices 
               if products[i].weight >= cutoff_value]

        winner = random.choice(rcl)

        order.append(winner+1) # order number is index + 1 (because 0 == start)
        remaining_product_indices.remove(winner)
    return order