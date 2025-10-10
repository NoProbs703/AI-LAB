import random

def generate_initial_state(n):
    return [random.randint(0, n-1) for _ in range(n)]

def calculate_conflicts(state):
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j]:
                conflicts += 1
            if abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def get_best_neighbor(state):
    n = len(state)
    best_state = state[:]
    best_conflicts = calculate_conflicts(state)
    
    for col in range(n):
        original_row = state[col]
        for row in range(n):
            if row == original_row:
                continue
            
            new_state = state[:]
            new_state[col] = row
            current_conflicts = calculate_conflicts(new_state)
            
            if current_conflicts < best_conflicts:
                best_conflicts = current_conflicts
                best_state = new_state
                
    return best_state, best_conflicts

def hill_climbing(n, max_restarts=100):
    for restart in range(max_restarts):
        current_state = generate_initial_state(n)
        current_conflicts = calculate_conflicts(current_state)
        
        while True:
            next_state, next_conflicts = get_best_neighbor(current_state)
            if next_conflicts >= current_conflicts:
                # No improvement, local maxima reached
                break
            current_state = next_state
            current_conflicts = next_conflicts
        
        if current_conflicts == 0:
            print(f"Solution found after {restart + 1} restarts!")
            return current_state
    
    print("Failed to find a solution")
    return None

def print_board(state):
    if state is None:
        print("No solution to print.")
        return
    
    n = len(state)
    for row in range(n):
        line = ""
        for col in range(n):
            if state[col] == row:
                line += " Q "
            else:
                line += " . "
        print(line)

n = 8
solution = hill_climbing(n)
print_board(solution)
