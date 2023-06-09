import sys
from enum import Enum
from functools import lru_cache
from math import inf
from typing import Callable

sys.setrecursionlimit(10000)


class MarkovDecisionProcessActions(Enum):
    pass


class MarkovDecisionProcess:
    def __init__(
        self,
        S: set[int],
        A: set[MarkovDecisionProcessActions],
        T: Callable[[int, MarkovDecisionProcessActions, int], float],
        R: Callable[[int, MarkovDecisionProcessActions, int], float],
        gamma: float,
        is_const_goal_pit_value: bool,
        goal_states: set[int],
        pit_states: set[int],
        goal_reward: float,
        pit_reward: float,
    ) -> None:
        # 状態集合
        self.S = S
        # 行動集合
        self.A = A
        # 遷移関数
        self.T = T
        # 報酬関数
        self.R = R
        # 報酬の割引率
        self.gamma = gamma
        # ゴール状態や落とし穴状態で V を R で固定するか
        self.is_const_goal_pit_value = is_const_goal_pit_value
        # ゴール状態集合
        self.goal_states = goal_states
        # ゴール時の報酬
        self.goat_reward = goal_reward
        # 落とし穴状態集合
        self.pit_states = pit_states
        # 落とし穴時の報酬
        self.pit_reward = pit_reward

    @lru_cache
    def V(self, s: int, k: int) -> float:
        """
        k ステップ目における状態 s の価値を求める
        Args:
            s: 現在の状態
            k: 現在のステップ数
        """
        if k == 0:
            return 0

        if self.is_const_goal_pit_value:
            if s in self.goal_states:
                return self.goat_reward
            elif s in self.pit_states:
                return self.pit_reward

        result_value = -inf

        for a in self.A:
            result_per_action = 0.0
            for s_sub in self.S:
                result_per_action += self.T(s, a, s_sub) * (
                    self.R(s, a, s_sub) + self.gamma * self.V(s_sub, k - 1)
                )
            result_value = max(result_value, result_per_action)

        return result_value

    def pi(self, s: int, k: int) -> MarkovDecisionProcessActions:
        """
        k ステップ目において、状態 s からの行動価値を最大にするような方策を求める
        """
        result_action: MarkovDecisionProcessActions = next(iter(self.A))
        pi_val = -inf
        for a in self.A:
            pi_val_per_action = 0.0
            for s_sub in self.S:
                pi_val_per_action += self.T(s, a, s_sub) * (
                    self.R(s, a, s_sub) + self.gamma * self.V(s_sub, k)
                )
            if pi_val < pi_val_per_action:
                pi_val = pi_val_per_action
                result_action = a

        return result_action
