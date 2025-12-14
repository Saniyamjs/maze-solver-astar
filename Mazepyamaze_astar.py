# Safe color version - works in old pyamaze

from pyamaze import maze, agent, textLabel
from queue import PriorityQueue

def h(cell1, cell2):
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

def astar(m):
    start = (m.rows, m.cols)
    goal = (1, 1)

    g_score = {cell: float('inf') for cell in m.grid}
    g_score[start] = 0

    f_score = {cell: float('inf') for cell in m.grid}
    f_score[start] = h(start, goal)

    from queue import PriorityQueue
    open_set = PriorityQueue()
    open_set.put((f_score[start], start))

    came_from = {}

    while not open_set.empty():
        _, curr = open_set.get()

        if curr == goal:
            break

        for d in 'ESNW':
            if m.maze_map[curr][d] == 1:
                if d == 'E':
                    child = (curr[0], curr[1] + 1)
                elif d == 'W':
                    child = (curr[0], curr[1] - 1)
                elif d == 'N':
                    child = (curr[0] - 1, curr[1])
                else:
                    child = (curr[0] + 1, curr[1])

                new_g = g_score[curr] + 1
                new_f = new_g + h(child, goal)

                if new_f < f_score[child]:
                    g_score[child] = new_g
                    f_score[child] = new_f
                    open_set.put((new_f, child))
                    came_from[child] = curr

    path = {}
    cell = goal
    if cell not in came_from:
        return {}

    while cell != start:
        parent = came_from[cell]
        path[parent] = cell
        cell = parent

    return path


if __name__ == "__main__":
    m = maze(10, 10)

    # Allowed colors only
    m.theme = {
        "background": "white",
        "wall": "red",      # closest to pink
        "cell": "white",
        "goal": "red"
    }

    m.CreateMaze()

    path = astar(m)

    # Use RED agent (closest to pink)
    a = agent(m, footprints=True, color="red", shape='circle')

    m.tracePath({a: path})

    textLabel(m, "A* Path Length", len(path) + 1 if path else 0)

    m.run()



