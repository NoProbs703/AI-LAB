import heapq

class PuzzleState:
    def __init__(self, board, moves=0, previous=None):
        self.board = board
        self.moves = moves
        self.previous = previous
        self.zero_index = board.index(0)

    def __lt__(self, other):
        return (self.moves + self.heuristic()) < (other.moves + other.heuristic())

    def heuristic(self):
        goal = [1, 2, 3,
                8, 0, 4,
                7, 6, 5]

        misplaced = 0
        for i, value in enumerate(self.board):
            if value != 0 and value != goal[i]:
                misplaced += 1
        return misplaced

    def is_goal(self):
        spiral_goal = [1, 2, 3,
                       8, 0, 4,
                       7, 6, 5]
        return self.board == spiral_goal

    def get_neighbors(self):
        neighbors = []
        x, y = divmod(self.zero_index, 3)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_index = new_x * 3 + new_y
                new_board = self.board[:]
                new_board[self.zero_index], new_board[new_index] = new_board[new_index], new_board[self.zero_index]
                neighbors.append(PuzzleState(new_board, self.moves + 1, self))
        return neighbors


def solve_puzzle(start_board):
    start_state = PuzzleState(start_board)
    frontier = []
    heapq.heappush(frontier, start_state)
    explored = set()

    while frontier:
        current = heapq.heappop(frontier)

        if tuple(current.board) in explored:
            continue
        explored.add(tuple(current.board))

        if current.is_goal():
            return reconstruct_path(current)

        for neighbor in current.get_neighbors():
            if tuple(neighbor.board) not in explored:
                heapq.heappush(frontier, neighbor)

    return None


def reconstruct_path(state):
    path = []
    while state:
        path.append(state.board)
        state = state.previous
    return path[::-1]


if __name__ == "__main__":
    start_board = [2, 8, 3,
                   1, 6, 4,
                   0, 7, 5]

    solution = solve_puzzle(start_board)

    if solution:
        print("Solution found in", len(solution) - 1, "moves:")
        for step in solution:
            for i in range(0, 9, 3):
                print(step[i:i+3])
            print()
    else:
        print("No solution exists for this puzzle.")
