import time
from settings import *
from a_star import (
    AstarSolver,
    mismatched_tiles_heuristic_rule,
    manhattan_heuristic_rule,
)
from bfs import BreadthFirstSearchSolver

import numpy as np

if __name__ == "__main__":
    sample_size = 1000
    state_generator = RandomStateGenerator(sample_size)
    random_state_list = state_generator.get_random_state_list()

    bfs_elapsed_times = dict()
    astar_mismatched_elapsed_times = dict()
    astar_manhattan_elapsed_times = dict()

    for i in range(0, 100, 5):
        bfs_elapsed_times[i] = list()
        astar_mismatched_elapsed_times[i] = list()
        astar_manhattan_elapsed_times[i] = list()

    goal_state = State("123456780")
    for i, start_state in enumerate(random_state_list):
        if i % 100 == 0:
            print(i, "th iteration has started...")
        bfs_solver = BreadthFirstSearchSolver(start_state, goal_state)
        astar_solver_mismatched_rule = AstarSolver(
            start_state, goal_state, mismatched_tiles_heuristic_rule
        )
        astar_solver_manhattan_rule = AstarSolver(
            start_state, goal_state, manhattan_heuristic_rule
        )

        start_time = time.time()
        bfs_solver.solve()
        bfs_time = time.time() - start_time

        start_time = time.time()
        astar_solver_mismatched_rule.solve()
        astar_mismatched_time = time.time() - start_time

        start_time = time.time()
        astar_solver_manhattan_rule.solve()
        astar_manhattan_time = time.time() - start_time

        assert (
            bfs_solver.get_operation_count()
            == astar_solver_mismatched_rule.get_operation_count()
            == astar_solver_manhattan_rule.get_operation_count()
        )

        bfs_time *= 1000
        astar_mismatched_time *= 1000
        astar_manhattan_time *= 1000

        operation_count_clipped = bfs_solver.get_operation_count() // 5 * 5
        bfs_elapsed_times[operation_count_clipped].append(bfs_time)
        astar_mismatched_elapsed_times[operation_count_clipped].append(
            astar_mismatched_time
        )
        astar_manhattan_elapsed_times[operation_count_clipped].append(
            astar_manhattan_time
        )

        # print(
        #     "{:.3f} {:.3f} {:.3f}".format(
        #         bfs_time, astar_mismatched_time, astar_manhattan_time
        #     )
        # )

    total_elapsed_times = [
        bfs_elapsed_times,
        astar_mismatched_elapsed_times,
        astar_manhattan_elapsed_times,
    ]

    print("sample size: ", sample_size)
    for elapsed_times in total_elapsed_times:
        for i in range(0, 100, 5):
            if len(elapsed_times[i]) == 0:
                print(i, "is missing")
            else:
                print(i, "size:", len(elapsed_times[i]))

    for elapsed_times in total_elapsed_times:
        for i in range(0, 100, 5):
            if len(elapsed_times[i]) == 0:
                continue
            print(
                # i,
                # ",".join(
                #     str(e) for e in np.percentile(elapsed_times[i], [0, 25, 50, 100])
                # ),
                sum(elapsed_times[i]) / len(elapsed_times[i]),
            )
        print()
