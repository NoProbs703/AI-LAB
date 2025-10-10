from collections import deque

GOAL_STATE = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)

MOVES = {
    'UP': -3,
    'DOWN': 3,
    'LEFT': -1,
    'RIGHT': 1
}

def is_valid_move(blank_idx, move):
    if move == 'UP' and blank_idx < 3:
        return False
    if move == 'DOWN' and blank_idx > 5:
        return False
    if move == 'LEFT' and blank_idx % 3 == 0:
        return False
    if move == 'RIGHT' and blank_idx % 3 == 2:
        return False
    return True

def apply_move(state, move):
    blank_idx = state.index(0)
    if not is_valid_move(blank_idx, move):
        return None
    target_idx = blank_idx + MOVES[move]
    new_state = list(state)
    new_state[blank_idx], new_state[target_idx] = new_state[target_idx], new_state[blank_idx]
    return tuple(new_state)

def dls(state, depth_limit, path, visited):
    if state == GOAL_STATE:
        return path

    if depth_limit == 0:
        return None

    visited.add(state)

    for move in MOVES:
        next_state = apply_move(state, move)
        if next_state and next_state not in visited:
            result = dls(next_state, depth_limit - 1, path + [move], visited)
            if result:
                return result

    return None

def iddfs(start_state, max_depth=30):
    for depth in range(max_depth):
        visited = set()
        result = dls(start_state, depth, [], visited)
        if result is not None:
            return result
    return None

def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

start_state = (1, 2, 3,
               4, 0, 6,
               7, 5, 8)

print("Initial State:")
print_state(start_state)

solution = iddfs(start_state)

if solution:
    print(f"Solution found in {len(solution)} moves:")
    print(solution)

    current = start_state
    for move in solution:
        current = apply_move(current, move)
        print(f"Move: {move}")
        print_state(current)
else:
    print("No solution found.")
