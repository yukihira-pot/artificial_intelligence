import os
import sys
from math import inf

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from typing import *

sys.setrecursionlimit(10000)

from mini_grid_world_config import MiniGridWorld

from mdpconfig import config


class MiniGridWorldValueIterationSolver:
    def __init__(
        self,
        field: list[str],
        goal_reward: float,
        pit_reward: float,
        living_reward: float,
        error_rate: float,
        gamma: float,
    ) -> None:
        self.mini_grid_world = MiniGridWorld(
            field=field,
            goal_reward=goal_reward,
            pit_reward=pit_reward,
            living_reward=living_reward,
            error_rate=error_rate,
        )
        self.mini_grid_world_mdp = config.MarkovDecisionProcess(
            S=self.mini_grid_world.S,
            A=self.mini_grid_world.A,
            T=self.mini_grid_world.T,
            R=self.mini_grid_world.R,
            gamma=gamma,
            is_const_goal_pit_value=True,
            goal_states=self.mini_grid_world._goal_state_nums,
            pit_states=self.mini_grid_world._pit_state_nums,
            goal_reward=self.mini_grid_world.goal_reward,
            pit_reward=self.mini_grid_world.pit_reward,
        )

        self._field = field
        self._H: int = len(self._field)
        self._W: int = len(self._field[0])

    def solve(self, max_iter=100):
        self.V_val = [[-inf for j in range(self._W)] for i in range(self._H)]
        self.pi_val = [[-inf for j in range(self._W)] for i in range(self._H)]
        for cx in range(self._H):
            for cy in range(self._W):
                current_state_num = self.mini_grid_world.coord_to_state_num(cx, cy)
                if self._field[cx][cy] != "#":
                    self.V_val[cx][cy] = self.mini_grid_world_mdp.V(
                        current_state_num, max_iter
                    )
                    self.pi_val[cx][cy] = self.mini_grid_world_mdp.pi(
                        current_state_num, max_iter
                    )

    def show(self, max_iter=100):
        self.solve(max_iter)
        print("[ original field ]")
        for cx in range(self._H):
            for cy in range(self._W):
                print(f"{self._field[cx][cy] * 3:^10}", end=" ")
            print()
        print()

        print(f"[ V at iteration {max_iter} ]")
        for cx in range(self._H):
            for cy in range(self._W):
                if self.V_val[cx][cy] != -inf:
                    print(f"{self.V_val[cx][cy]:<10.4f}", end=" ")
                else:
                    print("{:<10}".format("undefined"), end=" ")
            print()
        print()

        print(f"[ Pi at iteration {max_iter} ]")
        for cx in range(self._H):
            for cy in range(self._W):
                current_state_num = self.mini_grid_world.coord_to_state_num(cx, cy)
                if current_state_num in self.mini_grid_world._goal_state_nums:
                    print("{:<10}".format("GOAL"), end=" ")
                elif current_state_num in self.mini_grid_world._pit_state_nums:
                    print("{:<10}".format("PIT"), end=" ")
                elif self.pi_val[cx][cy] != -inf:
                    print(f"{self.pi_val[cx][cy]:<10}", end=" ")
                else:
                    print("{:<10}".format("undefined"), end=" ")
            print()


if __name__ == "__main__":
    field = ["...#.", "...#.", "#..+.", "...-."]
    mini_grid_world_value_iteration_solver = MiniGridWorldValueIterationSolver(
        field=field,
        goal_reward=1,
        pit_reward=-1,
        living_reward=0,
        error_rate=0.2,
        gamma=1,
    )
    mini_grid_world_value_iteration_solver.show(max_iter=10)
