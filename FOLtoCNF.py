"""
Example input:
    (forall x) (exists y) (P(x) -> Q(y))
"""

import itertools

class Var:
    def __init__(self, name): self.name = name
    def __repr__(self): return self.name

class Func:
    def __init__(self, name, args=[]):
        self.name, self.args = name, args
    def __repr__(self): return f"{self.name}({', '.join(map(str,self.args))})"

class Pred:
    def __init__(self, name, args=[]):
        self.name, self.args = name, args
    def __repr__(self): return f"{self.name}({', '.join(map(str,self.args))})"

class Not:
    def __init__(self, f): self.f = f
    def __repr__(self): return f"¬{self.f}"

class And:
    def __init__(self, left, right): self.left, self.right = left, right
    def __repr__(self): return f"({self.left} ∧ {self.right})"

class Or:
    def __init__(self, left, right): self.left, self.right = left, right
    def __repr__(self): return f"({self.left} ∨ {self.right})"

class Forall:
    def __init__(self, var, f): self.var, self.f = var, f
    def __repr__(self): return f"∀{self.var}.{self.f}"

class Exists:
    def __init__(self, var, f): self.var, self.f = var, f
    def __repr__(self): return f"∃{self.var}.{self.f}"

def eliminate_implications(f):
    if isinstance(f, Pred): return f
    if isinstance(f, Not): return Not(eliminate_implications(f.f))

    if isinstance(f, And): 
        return And(eliminate_implications(f.left), eliminate_implications(f.right))
    if isinstance(f, Or): 
        return Or(eliminate_implications(f.left), eliminate_implications(f.right))
    if isinstance(f, Forall): 
        return Forall(f.var, eliminate_implications(f.f))
    if isinstance(f, Exists): 
        return Exists(f.var, eliminate_implications(f.f))

    if isinstance(f, tuple) and f[0] == "IMP":
        a, b = eliminate_implications(f[1]), eliminate_implications(f[2])
        return Or(Not(a), b)

    raise ValueError("Unknown formula type")

def nnf(f):
    if isinstance(f, Pred): return f
    if isinstance(f, And): return And(nnf(f.left), nnf(f.right))
    if isinstance(f, Or): return Or(nnf(f.left), nnf(f.right))
    if isinstance(f, Forall): return Forall(f.var, nnf(f.f))
    if isinstance(f, Exists): return Exists(f.var, nnf(f.f))
    if isinstance(f, Not):
        g = f.f
        if isinstance(g, Pred): return f
        if isinstance(g, Not): return nnf(g.f)
        if isinstance(g, And): return Or(nnf(Not(g.left)), nnf(Not(g.right)))
        if isinstance(g, Or): return And(nnf(Not(g.left)), nnf(Not(g.right)))
        if isinstance(g, Forall): return Exists(g.var, nnf(Not(g.f)))
        if isinstance(g, Exists): return Forall(g.var, nnf(Not(g.f)))
    return f

counter = itertools.count()

def standardize(f, env=None):
    if env is None: env = {}

    if isinstance(f, Var):
        return env.get(f.name, f)

    if isinstance(f, Pred):
        return Pred(f.name, [standardize(a, env) for a in f.args])

    if isinstance(f, And): return And(standardize(f.left, env), standardize(f.right, env))
    if isinstance(f, Or): return Or(standardize(f.left, env), standardize(f.right, env))

    if isinstance(f, Not): return Not(standardize(f.f, env))

    if isinstance(f, Forall) or isinstance(f, Exists):
        new_var = Var(f"{f.var.name}_{next(counter)}")
        new_env = env.copy()
        new_env[f.var.name] = new_var
        return type(f)(new_var, standardize(f.f, new_env))

def skolemize(f, scope_vars=None):
    if scope_vars is None: scope_vars = []

    if isinstance(f, Pred): return f
    if isinstance(f, Not): return Not(skolemize(f.f, scope_vars))
    if isinstance(f, And): return And(skolemize(f.left, scope_vars), skolemize(f.right, scope_vars))
    if isinstance(f, Or): return Or(skolemize(f.left, scope_vars), skolemize(f.right, scope_vars))

    if isinstance(f, Forall):
        return Forall(f.var, skolemize(f.f, scope_vars + [f.var]))

    if isinstance(f, Exists):
        sk_name = f"Sk{next(counter)}"
        sk_term = Func(sk_name, scope_vars)
        return skolemize(substitute(f.f, {f.var.name: sk_term}), scope_vars)

def substitute(f, sub):
    if isinstance(f, Var): return sub.get(f.name, f)
    if isinstance(f, Pred): return Pred(f.name, [substitute(a, sub) for a in f.args])
    if isinstance(f, Func): return Func(f.name, [substitute(a, sub) for a in f.args])
    if isinstance(f, Not): return Not(substitute(f.f, sub))
    if isinstance(f, And): return And(substitute(f.left, sub), substitute(f.right, sub))
    if isinstance(f, Or): return Or(substitute(f.left, sub), substitute(f.right, sub))
    if isinstance(f, Forall) or isinstance(f, Exists):
        return type(f)(f.var, substitute(f.f, sub))

def drop_universal(f):
    if isinstance(f, Forall): return drop_universal(f.f)
    if isinstance(f, And): return And(drop_universal(f.left), drop_universal(f.right))
    if isinstance(f, Or): return Or(drop_universal(f.left), drop_universal(f.right))
    if isinstance(f, Not): return f
    return f

def distribute(f):
    if isinstance(f, Or):
        A, B = distribute(f.left), distribute(f.right)
        if isinstance(A, And):
            return And(distribute(Or(A.left, B)), distribute(Or(A.right, B)))
        if isinstance(B, And):
            return And(distribute(Or(A, B.left)), distribute(Or(A, B.right)))
        return Or(A, B)
    if isinstance(f, And):
        return And(distribute(f.left), distribute(f.right))
    return f

def to_cnf(f):
    print("Original:", f)
    f = eliminate_implications(f)
    print("No → :", f)
    f = nnf(f)
    print("NNF:", f)
    f = standardize(f)
    print("Standardized:", f)
    f = skolemize(f)
    print("Skolemized:", f)
    f = drop_universal(f)
    print("Dropped ∀:", f)
    f = distribute(f)
    print("CNF:", f)
    return f

formula = Forall(
    Var("x"),
    Exists(
        Var("y"),
        ("IMP", Pred("P", [Var("x")]), Pred("Q", [Var("y")]))
    )
)

cnf_formula = to_cnf(formula)
