import matplotlib.pyplot as plt
import numpy as np


def generate_nqueens_distribution(input_file):
    try:
        with open(input_file, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"error: file '{input_file}' not found.")
        return

    if not lines or "solutions for N=" not in lines[0]:
        print(
            "error: invalid file format. first line should contain 'solutions for N='."
        )
        return

    try:
        n = int(lines[0].strip().split("=")[1])
    except ValueError:
        print("error: could not parse N from the header.")
        return

    solutions = []
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) != n:
            continue

        try:
            solution = [int(x) for x in parts]
            if all(0 <= val < n for val in solution):
                solutions.append(solution)
        except ValueError:
            continue

    total_solutions = len(solutions)
    if total_solutions == 0:
        print("no valid solutions found.")
        return

    distribution = [[0 for _ in range(n)] for _ in range(n)]

    for sol in solutions:
        for col, row in enumerate(sol):
            distribution[row][col] += 1

    data = np.array(distribution)

    plt.figure(figsize=(max(6, n), max(6, n)))
    plt.imshow(data, cmap="YlOrRd", interpolation="nearest", origin="upper")

    plt.title(
        f"N-Queens solution distribution (N={n}, Total solutions={total_solutions})"
    )
    plt.xlabel("Column")
    plt.ylabel("Row")

    plt.xticks(np.arange(n), np.arange(n))
    plt.yticks(np.arange(n), np.arange(n))

    ax = plt.gca()
    ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which="minor", color="black", linestyle="-", linewidth=1)
    ax.tick_params(which="minor", size=0)

    cbar = plt.colorbar()
    cbar.set_label("Number of queens placed")

    for row in range(n):
        for col in range(n):
            plt.text(
                col,
                row,
                str(data[row, col]),
                ha="center",
                va="center",
                color="black" if data[row, col] < np.max(data) / 2 else "white",
            )

    output_file = f"nqueens_heatmap.png"
    plt.savefig(output_file, bbox_inches="tight", dpi=300)
    plt.close()

    print(f"chessboard heatmap saved as '{output_file}'")


generate_nqueens_distribution("nqueens_solutions.txt")
