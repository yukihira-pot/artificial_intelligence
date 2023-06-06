import heapq
import math

from base_solver import BaseEightPuzzleSolver
from settings import *


class AstarSolver(BaseEightPuzzleSolver):
    def __init__(self, start_state: State, goal_state: State, heuristic_rule):
        self.start_state = start_state
        self.goal_state = goal_state
        self.h = heuristic_rule

    def solve(self):
        self.dist = dict()
        self.prev_field = dict()
        que = list()
        heapq.heapify(que)

        start_field = self.start_state.field
        goal_field = self.goal_state.field
        self.dist[start_field] = 0
        heapq.heappush(que, (0, start_field))

        while len(que) > 0:
            cur_dist, cur_field = heapq.heappop(que)
            if cur_field == goal_field:
                break

            nxt_states = State(cur_field).get_adjacent_states()
            for nxt_state in nxt_states:
                nxt_field = nxt_state.field
                if (
                    nxt_field not in self.dist
                    or self.dist[nxt_field] > self.dist[cur_field] + 1
                ):
                    self.dist[nxt_field] = self.dist[cur_field] + 1
                    heapq.heappush(
                        que,
                        (
                            self.dist[nxt_field] + self.h(nxt_field, goal_field),
                            nxt_field,
                        ),
                    )
                    self.prev_field[nxt_field] = cur_field


def eucledian_heuristic_rule(cur_field, goal_field):
    res = 0
    field_size = 3
    cur_pos = [None] * (field_size * field_size)
    goal_pos = [None] * (field_size * field_size)
    for i in range(field_size):
        for j in range(field_size):
            cur_pos[int(cur_field[i * field_size + j])] = (i, j)
            goal_pos[int(goal_field[i * field_size + j])] = (i, j)
    for i in range(field_size * field_size):
        cur_x, cur_y = cur_pos[i]
        goal_x, goal_y = goal_pos[i]
        res += math.dist(cur_x - goal_x, cur_y - goal_y)
    return res - 1


def manhattan_heuristic_rule(cur_field, goal_field):
    res = 0
    field_size = 3
    cur_pos = [None] * (field_size * field_size)
    goal_pos = [None] * (field_size * field_size)
    for i in range(field_size):
        for j in range(field_size):
            cur_pos[int(cur_field[i * field_size + j])] = (i, j)
            goal_pos[int(goal_field[i * field_size + j])] = (i, j)
    for i in range(field_size * field_size):
        cur_x, cur_y = cur_pos[i]
        goal_x, goal_y = goal_pos[i]
        res += abs(cur_x - goal_x) + abs(cur_y - goal_y)
    return res - 1


def mismatched_tiles_heuristic_rule(cur_field, goal_field):
    res = 0
    for cur_tile, goal_tile in zip(cur_field, goal_field):
        res += cur_tile != goal_tile
    return res - 1


if __name__ == "__main__":
    state_generator = RandomStateGenerator(20)
    for start_state in state_generator.get_random_state_list():
        goal_state = State("123456780")
        astar_solver = AstarSolver(
            start_state, goal_state, mismatched_tiles_heuristic_rule
        )
        astar_solver.solve()
        # astar_solver.playback()
        print(astar_solver.get_operation_count())
