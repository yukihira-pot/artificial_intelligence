import sys
from enum import Enum
from functools import lru_cache
from math import inf
from typing import Callable

sys.setrecursionlimit(10000)


class MarkovDecisionProcessActions(Enum):
    pass


class MarkovDecisionProcess:
    def __init__(self, S, A, T, R, gamma) -> None:
        # 状態集合
        self.S: set[int] = S
        # 行動集合
        self.A: set[MarkovDecisionProcessActions] = A
        # 遷移関数
        self.T: Callable[[int, MarkovDecisionProcessActions, int], float] = T
        # 報酬関数
        self.R: Callable[[int, MarkovDecisionProcessActions, int], float] = R
        # 報酬の割引率
        self.gamma: float = gamma

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

        result_value = -inf
        for a in self.A:
            result_per_action = 0.0
            for s_sub in self.S:
                result_per_action += self.T(s, a, s_sub) * (
                    self.R(s, a, s_sub) + self.gamma * self.V(s_sub, k - 1)
                )
            result_value = max(result_value, result_per_action)

        return result_value

    def pi(self, s: int, k: int):
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
