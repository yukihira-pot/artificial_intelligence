from collections import deque

from base_solver import BaseEightPuzzleSolver
from settings import *


class BreadthFirstSearchSolver(BaseEightPuzzleSolver):
    def __init__(self, start_state: State, goal_state: State) -> None:
        self.start_state = start_state
        self.goal_state = goal_state

    def solve(self):
        self.dist = dict()
        self.prev_field = dict()
        que = deque()

        self.dist[self.start_state.field] = 0
        que.append(self.start_state)

        while len(que) > 0:
            cur_state = que.popleft()
            if cur_state.field == self.goal_state.field:
                break
            nxt_states = cur_state.get_adjacent_states()
            for nxt_state in nxt_states:
                if not nxt_state.field in self.dist:
                    self.dist[nxt_state.field] = self.dist[cur_state.field] + 1
                    self.prev_field[nxt_state.field] = cur_state.field
                    que.append(nxt_state)


if __name__ == "__main__":
    start_state = State("845320671")
    goal_state = State("123456780")
    bfs_solver = BreadthFirstSearchSolver(start_state, goal_state)
    bfs_solver.solve()
    bfs_solver.playback()
