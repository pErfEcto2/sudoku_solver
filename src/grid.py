from cell import Cell


class Grid:
    def _fill_can_be_sets(self, gr: list[list[str]]) -> None:
        tmp = [[] for _ in range(9)]
        for i, row in enumerate(gr):
            for j, el in enumerate(row):
                tmp[i].append(Cell())
                if el != " ":
                    tmp[i][j].can_be = set([el])

        self._cells: list[list[Cell]] = tmp

    def __init__(self, initial_grid: list[list[int]]) -> None:
        if len(initial_grid) != 9:
            raise ValueError("initial grid must be 9x9")
        for row in initial_grid:
            if len(row) != 9:
                raise ValueError("initial grid must be 9x9")

        self._grid: list[list[str]] = [[str(x) if x != 0 else " " for x in row] for row in initial_grid]
        self._fill_can_be_sets(self._grid)

        self._move_made: bool = False

    def _val_can_be_in_row(self, val: str, i: int) -> bool:
        return val not in self._grid[i]

    def _val_can_be_in_col(self, val: str, j: int) -> bool:
        return val not in [self._grid[i][j] for i in range(9)]

    def _val_can_be_in_square(self, val: str, i: int, j: int) -> bool:
        sq_i = (i // 3) * 3
        sq_j = (j // 3) * 3

        for i in range(sq_i, sq_i + 3):
            for j in range(sq_j, sq_j + 3):
                if self._grid[i][j] == val:
                    return False
        return True

    def _val_can_be_at_pos(self, val: str, i: int, j: int) -> bool:
        return self._val_can_be_in_row(val, i) and self._val_can_be_in_col(val, j) and self._val_can_be_in_square(val, i, j)

    def _reduce_avail_in_cell(self, i: int, j: int) -> None:
        for val in map(str, range(1, 10)):
            if not self._val_can_be_at_pos(val, i, j):
                self._cells[i][j].can_be.discard(val)

    def _naive_reduce_avail_in_cells(self) -> None:
        for i, row in enumerate(self._grid):
            for j, val in enumerate(row):
                if val != " ":
                    continue
                self._reduce_avail_in_cell(i, j)

    def _reduce_by_checking_square(self, i: int, j: int) -> None:
        sq_i = (i // 3) * 3
        sq_j = (j // 3) * 3

        avail_vals = self._cells[i][j].can_be.copy()

        for ii in range(sq_i, sq_i + 3):
            for jj in range(sq_j, sq_j + 3):
                if i == ii and j == jj:
                    continue
                avail_vals -= self._cells[ii][jj].can_be

        if len(avail_vals) >= 1:
            self._cells[i][j].can_be = avail_vals

    def _reduce_by_checking_squares(self) -> None:
        for i, row in enumerate(self._grid):
            for j, val in enumerate(row):
                if val != " ":
                    continue
                self._reduce_by_checking_square(i, j)

    def _recursive_solver(self, gr: list[list[str]]) -> list[list[str]] | None:

        return

    def _fill(self) -> None:
        for i, row in enumerate(self._grid):
            for j, val in enumerate(row):
                if val != " ":
                    continue
                if len(self._cells[i][j].can_be) != 1:
                    continue
                self._grid[i][j] = list(self._cells[i][j].can_be)[0]
                self._move_made = True

    def _step(self) -> None:
        self._move_made = False
        self._naive_reduce_avail_in_cells()
        self._reduce_by_checking_squares()
        self._fill()

    def _is_solved(self) -> bool:
        for row in self._cells:
            for cell in row:
                if len(cell.can_be) != 1:
                    return False

        return True

    def solve(self) -> list[list[str]] | None:
        while not self._is_solved():
            self._step()
            # self.print_board()
            # self.print_sets()
            # print()
            # input()
            if not self._move_made:
                if (solved := self._recursive_solver(self._grid)) is None:
                    return

                return solved

        return self._grid

    def _print_row(self, i: int) -> None:
        print(f"| {' '.join(self._grid[i][0:3])} | {' '.join(self._grid[i][3:6])} | {' '.join(self._grid[i][6:9])} |")

    def print_board(self) -> None:
        print("board state:")
        for i, _ in enumerate(self._grid):
            if i % 3 == 0:
                print("-" * 25)
            self._print_row(i)

        print("-" * 25)

    def _print_row_sets(self, i: int) -> None:
        for j, cell in enumerate(self._cells[i]):
            if j % 3 == 0:
                print("| ", end="")
            print(f"{cell} ", end="")
        print("|", end="")
        print()

    def print_sets(self) -> None:
        print("possible values (or 'A' if more than one value is possible):")
        for i, _ in enumerate(self._grid):
            if i % 3 == 0:
                print("-" * 25)
            self._print_row_sets(i)

        print("-" * 25)



