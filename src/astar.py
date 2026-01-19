from heapq import heappush, heappop
from supermarket import Grid

def astar(grid:Grid, start, goal):
    rows, cols = grid.grid.shape
    
    def neighbors(r, c):
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols:
                # nur begehbar wenn kein Regal/Wand dazwischen
                if is_passable(grid.grid, r, c, nr, nc):
                    yield nr, nc

    def heuristic(r, c, gr, gc):
        return abs(r-gr) + abs(c-gc)   # Manhattan
    
    (sr, sc) = start
    (gr, gc) = goal

    open_set = []
    heappush(open_set, (0, sr, sc))
    came_from = {}
    g_score = {(sr, sc): 0}

    while open_set:
        _, r, c = heappop(open_set)

        if (r, c) == (gr, gc):
            return reconstruct_path(came_from, start, goal)

        for nr, nc in neighbors(r, c):
            tentative = g_score[(r, c)] + 1
            if (nr, nc) not in g_score or tentative < g_score[(nr, nc)]:
                g_score[(nr, nc)] = tentative
                f = tentative + heuristic(nr, nc, gr, gc)
                heappush(open_set, (f, nr, nc))
                came_from[(nr, nc)] = (r, c)

    return None  # Kein Weg gefunden


def reconstruct_path(came_from, start, goal):
    path = [goal]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


def is_passable(grid, r1, c1, r2, c2):
    """Begehbarkeit: blockiert wenn Wand(1) oder Regal(str) auf der Verbindungsseite."""
    z1 = grid[r1, c1]
    z2 = grid[r2, c2]

    # Richtung bestimmen
    if r2 == r1+1 and c2 == c1:
        # r1,c1 -> r2,c2 = nach unten in Grid-Koordinaten
        return z1.seiten["S"] == 0 and z2.seiten["N"] == 0
    if r2 == r1-1 and c2 == c1:
        return z1.seiten["N"] == 0 and z2.seiten["S"] == 0
    if r2 == r1 and c2 == c1+1:
        return z1.seiten["E"] == 0 and z2.seiten["W"] == 0
    if r2 == r1 and c2 == c1-1:
        return z1.seiten["W"] == 0 and z2.seiten["E"] == 0

    return False
