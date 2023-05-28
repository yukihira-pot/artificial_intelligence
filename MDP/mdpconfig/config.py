from abc import abstractmethod
from typing import Protocol
from enum import Enum

class MarkovDecisionProcessActions(Enum):
    pass

class MarkovDecisionProcess(Protocol):
    S: set[int]
    A: MarkovDecisionProcessActions
    T: callable
    R: callable

    @abstractmethod
    def V(self, s: int) -> float:
        pass