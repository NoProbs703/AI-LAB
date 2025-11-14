TREE = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F", "G"],
    "D": ["H", "I"],
    "E": ["J", "K"],
    "F": ["L", "M"],
    "G": ["N", "O"],

    "H": [41, 5],
    "I": [12, 90],
    "J": [101, 80],
    "K": [20, 30],
    "L": [34, 80],
    "M": [36, 35],
    "N": [50, 36],
    "O": [25, 3],
}

def is_terminal(node):
    """Returns True if node is a leaf."""
    return isinstance(TREE[node][0], int)

def max_value(node, alpha, beta):
    if is_terminal(node):
        return max(TREE[node])

    v = float("-inf")
    for child in TREE[node]:
        v = max(v, min_value(child, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def min_value(node, alpha, beta):
    if is_terminal(node):
        return min(TREE[node])

    v = float("inf")
    for child in TREE[node]:
        v = min(v, max_value(child, alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

def alpha_beta_search(root):
    """Returns the best move from root."""
    best_value = float("-inf")
    best_action = None
    alpha, beta = float("-inf"), float("inf")

    print("Evaluating moves from A...\n")

    for child in TREE[root]:
        value = min_value(child, alpha, beta)
        print(f"Move {root} → {child} gives value {value}")
        if value > best_value:
            best_value = value
            best_action = child
        alpha = max(alpha, best_value)

    return best_action, best_value

if __name__ == "__main__":
    move, value = alpha_beta_search("A")
    
    print(f"\nBest move from A: {move}")
    print(f"Root node (A) value: {value}")
