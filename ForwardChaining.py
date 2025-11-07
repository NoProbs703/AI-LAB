def is_variable(x):
    return isinstance(x, str) and x[0].islower()

def occur_check(var, expr):
    if var == expr:
        return True
    elif isinstance(expr, list):
        return any(occur_check(var, subexpr) for subexpr in expr)
    return False

def substitute(expr, subst):
    if isinstance(expr, list):
        return [substitute(e, subst) for e in expr]
    for (var, val) in subst:
        if expr == var:
            return val
    return expr

def unify(x, y, subst=None):
    if subst is None:
        subst = []
    if x == y:
        return subst
    if is_variable(x):
        if occur_check(x, y):
            return None
        subst.append((x, y))
        return subst
    if is_variable(y):
        if occur_check(y, x):
            return None
        subst.append((y, x))
        return subst
    if isinstance(x, list) and isinstance(y, list):
        if x[0] != y[0] or len(x) != len(y):
            return None
        for i in range(1, len(x)):
            subst = unify(substitute(x[i], subst), substitute(y[i], subst), subst)
            if subst is None:
                return None
        return subst
    return None

def fol_fc_ask(KB, query):
    inferred = set()
    new = True

    while new:
        new = set()
        for rule in KB:
            if '=>' in rule:
                idx = rule.index('=>')
                premises = rule[:idx]
                conclusion = rule[idx + 1]

                matches = []
                for premise in premises:
                    for fact in KB:
                        if '=>' not in fact:  
                            s = unify(premise, fact)
                            if s is not None:
                                matches.append(s)

                for s in matches:
                    new_fact = substitute(conclusion, s)
                    if new_fact not in KB and tuple(new_fact) not in new:
                        new.add(tuple(new_fact))
                        if unify(new_fact, query) is not None:
                            return True
        KB.extend([list(n) for n in new])
    return False

KB = [
    ['Parent', 'John', 'Mary'],
    ['Parent', 'Mary', 'Anne'],
    [['Parent', 'x', 'y'], ['Parent', 'y', 'z'], '=>', ['Grandparent', 'x', 'z']]
]

query = ['Grandparent', 'John', 'Anne']

result = fol_fc_ask(KB, query)

print("Query:", query)
print("Entailed?", result)

