from typing import *
import random


class State:
    def __init__(self, field: str):
        """
        ex.
        |1|4|2|
        |3|0|5|
        |6|7|8|
        の状態は
        "142305678" で表す
        """
        self.field = field
        for i, e in enumerate(self.field):
            if e == "0":
                self._zero_tile = i

    @property
    def zero_tile(self):
        """0 が入っている場所"""
        return self._zero_tile

    def get_adjacent_tiles(self):
        """
        マスを
        |0|1|2|
        |3|4|5|
        |6|7|8|
        と番号付けした場合に、
        state のどのマスが 0 かによって swap できるマスを返す
        """
        match self.zero_tile:
            case 0:
                return (1, 3)
            case 1:
                return (0, 2, 4)
            case 2:
                return (1, 5)
            case 3:
                return (0, 4, 6)
            case 4:
                return (1, 3, 5, 7)
            case 5:
                return (2, 4, 8)
            case 6:
                return (3, 7)
            case 7:
                return (4, 6, 8)
            case 8:
                return (5, 7)

    def get_adjacent_states(self):
        res = list()
        for adj_tile in self.get_adjacent_tiles():
            adj_state = list(self.field)
            adj_state[self.zero_tile], adj_state[adj_tile] = (
                adj_state[adj_tile],
                adj_state[self.zero_tile],
            )
            res.append(State("".join(str(e) for e in adj_state)))
        return res

    def __str__(self):
        return (
            f"|{self.field[0]}|{self.field[1]}|{self.field[2]}|\n"
            + f"|{self.field[3]}|{self.field[4]}|{self.field[5]}|\n"
            + f"|{self.field[6]}|{self.field[7]}|{self.field[8]}|"
        )


class RandomStateGenerator:
    def __init__(self, sample_size) -> None:
        self.sample_size = sample_size

    def get_random_state_list(self):
        res = list()
        for _ in range(self.sample_size):
            state = State("123456780")
            for i in range(random.randint(0, 100)):
                adjacent_states = state.get_adjacent_states()
                random_adjacent_state = adjacent_states[
                    random.randint(0, len(adjacent_states) - 1)
                ]
                state = random_adjacent_state
            res.append(state)
        return res
