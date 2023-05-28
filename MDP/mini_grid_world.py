from typing import *
from random import random
from enum import Enum

class Actions(Enum):
    L = (0, -1)
    R = (0, 1)
    U = (-1, 0)
    D = (1, 0)

class MiniGridWorld:

    def __init__(self, field: list[str], goal_reward, pit_reward, living_reward, error_rate) -> None:
        """
        mini grid world を 文字列のリストで表現
        例:["...#.",
            "...#.",
            "#..+.",
            "...-."]
        のように、壁を # で、ゴールマスを + で、落とし穴マスを - で表現
        """
        self.directions = [ action.value for action in Actions ]
        self._field: list[list[str]] = field
        self.goal_reward: float = goal_reward
        self.pit_reward: float = pit_reward
        self._living_reward: float = living_reward
        self._error_rate: float = error_rate
    
        self._H: int = len(field)
        self._W: int = len(field[0])

        self._coord_to_state_num, self._state_num_to_coord,\
        self._goal_state_nums, self._pit_state_nums = self.set_states_config()
        self._connections: list[set[int]] = self.set_connections()

        self.R = self._R
        self.T = self._T

    def set_states_config(self) -> tuple[list[list[int]], list[tuple[int, int]], set[int], set[int]]:
        _coord_to_state_num: list[list[int]] = [ [-1 for j in range(self._W)] for i in range(self._H) ]
        _state_num_to_coord: list[tuple[int, int]] = [(0, 0) for _ in range(self._H * self._W)]
        _goal_state_nums: set[int] = set()
        _pit_state_nums: set[int] = set()
        state_num = 0
        for cx in range(self._H):
            for cy in range(self._W):
                if self._field[cx][cy] != "#":
                    _coord_to_state_num[cx][cy] = state_num
                    _state_num_to_coord[state_num] = (cx, cy)
                    if self._field[cx][cy] == "+":
                        _goal_state_nums.add(state_num)
                    elif self._field[cx][cy] == "-":
                        _pit_state_nums.add(state_num)
                    state_num += 1
        return _coord_to_state_num, _state_num_to_coord, _goal_state_nums, _pit_state_nums

    def set_connections(self) -> list[set[int]]:
        """
        self._connections[current_state_num] = { current_state_num 番の状態から遷移できる状態の集合 }
        とし、self._conections を構築
        """
        _connections: list[set[int]] = [ set() for _ in range(self._H * self._W) ]

        for cx in range(self._H):
            for cy in range(self._W):
                current_state_num = self._coord_to_state_num[cx][cy]
                for (dx, dy) in self.directions:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < self._H and 0 <= ny < self._W and self._field[nx][ny] != '#':
                        connected_state_num = self._coord_to_state_num[nx][ny]
                        _connections[current_state_num].add(connected_state_num)
        return _connections
    
    @property
    def S(self) -> Literal[0]:
        """状態数"""
        return self._S
    
    @property
    def A(self) -> Actions:
        """行動集合"""
        return self._actions
    @A.setter
    def A(self) -> Actions:
        self._actions = Actions()
        return self._actions
    
    def get_next_state_num(self, s: int, a: Actions):
        s_coord: int = self._state_num_to_coord[s]
        s_sub_coord_x, s_sub_coord_y = s_coord[0] + a[0], s_coord[1] + a[1]
        if 0 <= s_sub_coord_x < self._H and 0 <= s_sub_coord_y < self._W:
            return self._coord_to_state_num[s_sub_coord_x][s_sub_coord_y]
    
    def is_connected(self, s: int, s_sub: int) -> bool:
        """s から s' に移動できるかどうかを返す"""
        return s_sub in self._connections[s]

    def _T(self, s: int, a: Actions, s_sub: int) -> float:
        if not self.is_connected(s, s_sub):
            return 0
        elif self.get_next_state_num(s, a) == s_sub:
            return 1 - self._error_rate
        else:
            return self._error_rate
    
    def _R(self, s: int, a: Actions, s_sub: int) -> float:
        reward: float = -1.0
        if s in self._goal_state_nums:
            reward += self.goal_reward
        elif s in self._pit_state_nums:
            reward += self.pit_reward
        return reward
    

if __name__ == "__main__":
    # テスト
    field = [
        "...#.",
        "...#.",
        "#..+.",
        "...-."
    ]
    mini_grid_world = MiniGridWorld(field, 10, -10, -0.1, 0.1)
    for i in range(17):
        for j in range(17):
            for action in [ action.value for action in Actions ]:
                print(i, action, j, mini_grid_world.T(i, action, j) * mini_grid_world.R(i, action, j))