import numpy as np


diff = ["data/very_easy_solution.npy", "data/easy_solution.npy", "data/medium_solution.npy", "data/hard_solution.npy"]

for D in diff:
    puzzle = np.load(D)


    for i in range(15):
        print(D, " ", i, "th puzzle")
        print(puzzle[i])

    print("\n")
