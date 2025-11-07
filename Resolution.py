def is_variable(x):
    return isinstance(x, str) and x[0].islower()


def substitute(expr, subst):
    """Apply a substitution mapping to an expression."""
    if isinstance(expr, list):
        return [substitute(e, subst) for e in expr]
    for (var, val) in subst.items():
        if expr == var:
            return val
    return expr


def unify(x, y, subst=None):
    """Unification algorithm."""
    if subst is None:
        subst = {}
    if x == y:
        return subst
    if is_variable(x):
        return unify_var(x, y, subst)
    if is_variable(y):
        return unify_var(y, x, subst)
    if isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y) or x[0] != y[0]:
            return None
        for i in range(1, len(x)):
            subst = unify(substitute(x[i], subst), substitute(y[i], subst), subst)
            if subst is None:
                return None
        return subst
    return None


def unify_var(var, x, subst):
    if var in subst:
        return unify(subst[var], x, subst)
    elif isinstance(x, str) and x in subst:
        return unify(var, subst[x], subst)
    elif occur_check(var, x, subst):
        return None
    else:
        subst[var] = x
        return subst


def occur_check(var, x, subst):
    """Check if variable occurs in expression (to prevent infinite loops)."""
    if var == x:
        return True
    elif isinstance(x, list):
        return any(occur_check(var, xi, subst) for xi in x)
    elif x in subst:
        return occur_check(var, subst[x], subst)
    return False

def negate(literal):
    """Return negation of a literal."""
    if literal[0] == '¬':
        return literal[1:]  # remove negation
    return '¬' + literal


def resolve(ci, cj):
    """Resolve two clauses."""
    resolvents = []
    for di in ci:
        for dj in cj:
            if di == negate(dj):
                new_clause = list(set(ci + cj))
                new_clause.remove(di)
                new_clause.remove(dj)
                resolvents.append(new_clause)
    return resolvents


def pl_resolution(KB, query):
    """Resolution algorithm: returns True if KB ⊨ query."""
    clauses = KB + [[negate(query)]]  
    new = set()

    while True:
        pairs = [(clauses[i], clauses[j]) for i in range(len(clauses))
                 for j in range(i + 1, len(clauses))]
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if [] in resolvents:
                return True  
            for r in resolvents:
                new.add(tuple(sorted(r)))
        if new.issubset(set(tuple(sorted(c)) for c in clauses)):
            return False  
        for c in new:
            if list(c) not in clauses:
                clauses.append(list(c))


# ---------------------------------------------------------------
# Example Knowledge Base
# ---------------------------------------------------------------
# KB:
# 1. P ⇒ Q  → represented as [¬P, Q]
# 2. L ∧ M ⇒ P → represented as [¬L, ¬M, P]
# 3. L
# 4. M
# Query: Q

KB = [
    ['¬P', 'Q'],
    ['¬L', '¬M', 'P'],
    ['L'],
    ['M']
]

query = 'Q'

result = pl_resolution(KB, query)

print("Query:", query)
print("Entailed?", result)
