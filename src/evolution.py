def simple_selection(ranking, population, generation_size):
    ranking = ranking[:generation_size*2]
    parents = [population[rank] for rank in ranking]
    return parents

def crossover_reproduction(selected_population:list):
    # s = len(selected population) = g/2
    # O(g * n)
    number_of_products = len(selected_population[0])
    crossover_line = int(number_of_products/2)
    children = []
    for i in range(0,len(selected_population),2):
        male, female = selected_population[i], selected_population[i+1]
        child = male[:crossover_line]
        while len(child) < len(male):
            child.append(next(product for product in female if (product not in child)))
        children.append(child)
    return children

def remove_duplicates(population):
    seen = set()
    new_pop = []
    for ind in population:
        key = tuple(ind)
        if key not in seen:
            seen.add(key)
            new_pop.append(ind)
    return new_pop