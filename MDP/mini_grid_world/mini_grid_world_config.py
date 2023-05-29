import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from typing import *

from mdpconfig import config


class Actions(config.MarkovDecisionProcessActions):
    L = (0, -1)
    R = (0, 1)
    U = (-1, 0)
    D = (1, 0)


class MiniGridWorld:
    def __init__(
        self, field: list[str], goal_reward, pit_reward, living_reward, error_rate
    ) -> None:
        """
        mini grid world を 文字列のリストで表現
        例:["...#.",
            "...#.",
            "#..+.",
            "...-."]
        のように、壁を # で、ゴールマスを + で、落とし穴マスを - で表現
        """
        self.directions: set[Actions] = { action for action in Actions }
        self._field: list[list[str]] = field
        self.goal_reward: float = goal_reward
        self.pit_reward: float = pit_reward
        self._living_reward: float = living_reward
        self._error_rate: float = error_rate

        self._H: int = len(field)
        self._W: int = len(field[0])

        (
            self._S,
            self._coord_to_state_num,
            self._state_num_to_coord,
            self._goal_state_nums,
            self._pit_state_nums,
        ) = self.set_states_config()

        self._connections: list[set[int]] = self.set_connections()

        self.R = self._R
        self.T = self._T

    def set_states_config(
        self,
    ) -> tuple[ list[list[int]], list[tuple[int, int]], set[int], set[int] ]:
        """
        ( 状態集合, 座標 -> 状態番号のリスト, 状態番号 -> 座標のリスト, ゴール状態集合, 落とし穴状態集合 ) を構築
        """
        # 状態集合
        _S: set[int] = set()
        # 座標 -> 状態番号 のリスト
        _coord_to_state_num: list[list[int]] = [
            [-1 for j in range(self._W)] for i in range(self._H)
        ]
        # 状態番号 -> 座標 のリスト
        _state_num_to_coord: list[tuple[int, int]] = [
            (0, 0) for _ in range(self._H * self._W)
        ]
        # ゴール状態集合
        _goal_state_nums: set[int] = set()
        # 落とし穴状態集合
        _pit_state_nums: set[int] = set()

        # 現在の状態番号: 1 ずつインクリメント
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

                    _S.add(state_num)
                    state_num += 1
        return (
            _S,
            _coord_to_state_num,
            _state_num_to_coord,
            _goal_state_nums,
            _pit_state_nums,
        )

    def set_connections(self) -> list[set[int]]:
        """
        self._connections[current_state_num] = { current_state_num 番の状態から遷移できる状態の集合 }
        となるように、self._conections を構築

        Returns:
            self._connections
        """
        _connections: list[set[int]] = [set() for _ in range(self._H * self._W)]

        for cx in range(self._H):
            for cy in range(self._W):
                current_state_num = self._coord_to_state_num[cx][cy]
                for direction in self.directions:
                    dx, dy = direction.value
                    nx, ny = cx + dx, cy + dy
                    if (
                        0 <= nx < self._H
                        and 0 <= ny < self._W
                        and self._field[nx][ny] != "#"
                    ):
                        connected_state_num = self._coord_to_state_num[nx][ny]
                        _connections[current_state_num].add(connected_state_num)
        return _connections

    @property
    def S(self) -> set[int]:
        """状態数"""
        return self._S

    @property
    def A(self) -> Actions:
        """行動集合"""
        return self.directions

    def get_next_state_num(self, s: int, a: Actions):
        """行動 a にしたがって状態 s から遷移した先の状態を返す"""
        s_coord: int = self._state_num_to_coord[s]
        s_sub_coord_x, s_sub_coord_y = s_coord[0] + a.value[0], s_coord[1] + a.value[1]
        if 0 <= s_sub_coord_x < self._H and 0 <= s_sub_coord_y < self._W:
            return self._coord_to_state_num[s_sub_coord_x][s_sub_coord_y]

    def is_connected(self, s: int, s_sub: int) -> bool:
        """s から s_sub に移動できるかどうかを返す"""
        return s_sub in self._connections[s]

    def _T(self, s: int, a: Actions, s_sub: int) -> float:
        """行動 a にしたがって状態 s から s_sub に遷移する確率"""
        # ゴール状態または落とし穴状態であれば、確率 1 で同じ状態に遷移
        if s in self._goal_state_nums or s in self._pit_state_nums:
            if s == s_sub:
                return 1.0
            else:
                return 0.0
        # s から 1 手で s_sub にたどり着けなければ 0 
        if not self.is_connected(s, s_sub):
            return 0.0
        # 確率: 1 - エラー率 で正しい状態に遷移
        elif self.get_next_state_num(s, a) == s_sub:
            return 1.0 - self._error_rate
        else:
            return self._error_rate

    def _R(self, s: int, a: Actions, s_sub: int) -> float:
        """行動 a にしたがって状態 s から s_sub に遷移したときの報酬"""
        # 生存報酬を初期値とする
        reward: float = self._living_reward
        # ゴール状態または落とし穴状態にいるとき、即時報酬を与える
        if s in self._goal_state_nums:
            reward += self.goal_reward
        elif s in self._pit_state_nums:
            reward += self.pit_reward
        return reward
