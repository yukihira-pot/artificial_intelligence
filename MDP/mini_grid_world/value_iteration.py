import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from typing import *

from mdpconfig import config
from mini_grid_world_config import MiniGridWorld


if __name__ == "__main__":
    field = ["...#.", "...#.", "#..+.", "...-."]
    mini_grid_world = MiniGridWorld(
        field=field, 
        goal_reward=10, 
        pit_reward=-10, 
        living_reward=0, 
        error_rate=0.1
    )

    mini_grid_world_mdp = config.MarkovDecisionProcess(
        S = mini_grid_world.S, 
        A = mini_grid_world.A, 
        T = mini_grid_world.T, 
        R = mini_grid_world.R, 
        gamma=0.5
    )

    for s in mini_grid_world.S:
        print(mini_grid_world_mdp.V(s, 500))
