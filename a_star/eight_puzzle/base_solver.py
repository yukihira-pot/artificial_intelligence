from settings import *


class BaseEightPuzzleSolver:
    def __init__(
        self, start_state: State, goal_state: State, heuristic_fule=None
    ) -> None:
        self.start_state = start_state
        self.goal_state = goal_state
        self.h = heuristic_fule

    def get_playback_list(self):
        assert self.goal_state.field in self.dist
        res = list()
        cur_field = self.goal_state.field
        while True:
            res.append(cur_field)
            if cur_field == self.start_state.field:
                break
            cur_field = self.prev_field[cur_field]
        res.reverse()
        return res

    def playback(self):
        playback_list = self.get_playback_list()
        for i, e in enumerate(playback_list):
            print(State(e))
            if i != len(playback_list) - 1:
                print("   ↓")
        print(len(playback_list), "turns")

    def get_operation_count(self):
        return len(self.get_playback_list())
