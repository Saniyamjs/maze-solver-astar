from pyamaze import maze, agent, textLabel
from queue import PriorityQueue

def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)

def astar(m):
    start = (m.rows, m.cols)
    goal = (1, 1)

    g_score = {cell: float('inf') for cell in m.grid}
    g_score[start] = 0

    f_score = {cell: float('inf') for cell in m.grid}
    f_score[start] = h(start, goal)

    open_set = PriorityQueue()
    open_set.put((f_score[start], h(start, goal), start))

    came_from = {}

    while not open_set.empty():
        curr_f_score, curr_h_score, curr_cell = open_set.get()

        if curr_cell == goal:
            break

        for d in 'ESNW':
            if m.maze_map[curr_cell][d] == 1:
                if d == 'E':
                    child_cell = (curr_cell[0], curr_cell[1] + 1)
                elif d == 'W':
                    child_cell = (curr_cell[0], curr_cell[1] - 1)
                elif d == 'N':
                    child_cell = (curr_cell[0] - 1, curr_cell[1])
                elif d == 'S':
                    child_cell = (curr_cell[0] + 1, curr_cell[1])

                temp_g_score = g_score[curr_cell] + 1
                temp_f_score = temp_g_score + h(child_cell, goal)

                if temp_f_score < f_score[child_cell]:
                    g_score[child_cell] = temp_g_score
                    f_score[child_cell] = temp_f_score
                    open_set.put((temp_f_score, h(child_cell, goal), child_cell))
                    came_from[child_cell] = curr_cell

    fwd_path = {}
    cell = goal

    if cell not in came_from and cell != start:
        return {}

    while cell != start:
        parent = came_from[cell]
        fwd_path[parent] = cell
        cell = parent

    return fwd_path

if __name__ == '__main__':
    m = maze(10, 10)
    m.CreateMaze()
    path = astar(m)

    a = agent(m, footprints=True, color='red')
    m.tracePath({a: path})

    path_len = len(path) + 1 if path else 0
    textLabel(m, 'A Star Path Length', path_len)

    m.run()



