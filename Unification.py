def is_variable(x):
    """Check if x is a variable (starts with lowercase letter)."""
    return isinstance(x, str) and x[0].islower()


def occur_check(var, expr):
    """Check if variable 'var' occurs in expression 'expr'."""
    if var == expr:
        return True
    elif isinstance(expr, list):
        return any(occur_check(var, subexpr) for subexpr in expr)
    return False


def substitute(expr, subst):
    """Apply a substitution set to an expression."""
    if isinstance(expr, list):
        return [substitute(e, subst) for e in expr]
    for (var, val) in subst:
        if expr == var:
            return val
    return expr


def unify(x, y, subst=None):
    """Unify two expressions x and y."""
    if subst is None:
        subst = []

    if x == y:
        return subst

    if is_variable(x):
        if occur_check(x, y):
            return None  
        else:
            subst.append((x, y))
            return subst

    if is_variable(y):
        if occur_check(y, x):
            return None 
        else:
            subst.append((y, x))
            return subst

    if isinstance(x, list) and isinstance(y, list):
        if x[0] != y[0]:
            return None  

        if len(x) != len(y):
            return None 

        for i in range(1, len(x)):
            s = unify(substitute(x[i], subst), substitute(y[i], subst), subst)
            if s is None:
                return None
            subst = s

        return subst

    return None 

expr1 = ['Knows', 'John', ['Father', 'x']]
expr2 = ['Knows', 'John', ['Father', 'Jack']]

result = unify(expr1, expr2)

print("Expression 1:", expr1)
print("Expression 2:", expr2)
if result:
    print("Unification Successful. Substitution Set:", result)
else:
    print("Unification Failed.")
