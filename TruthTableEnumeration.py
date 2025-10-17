from itertools import product

def TT_ENTAILS(KB, alpha):
    """
    KB: a knowledge base, list of sentences (propositional logic expressions)
    alpha: the query sentence
    returns: True if KB entails alpha, False otherwise
    """

    symbols = get_symbols(KB) | get_symbols([alpha])
    symbols = list(symbols)
    
    return TT_CHECK_ALL(KB, alpha, symbols, {})

def TT_CHECK_ALL(KB, alpha, symbols, model):
    """
    KB: knowledge base (list of sentences)
    alpha: query sentence
    symbols: list of proposition symbols to assign
    model: current partial assignment dict {symbol: True/False}
    """
    if not symbols:
        if PL_TRUE(KB, model):
            return PL_TRUE([alpha], model)
        else:
            return True
    else:
        P = symbols[0]
        rest = symbols[1:]

        return (TT_CHECK_ALL(KB, alpha, rest, {**model, P: True}) and
                TT_CHECK_ALL(KB, alpha, rest, {**model, P: False}))

def PL_TRUE(sentences, model):
    """
    Check if all sentences in the knowledge base are true under the given model.
    Sentences are propositional logic expressions (strings).
    model: dict mapping symbols to True/False
    """
    for sentence in sentences:
        if not evaluate(sentence, model):
            return False
    return True

def get_symbols(sentences):
    """
    Extract propositional symbols from the list of sentences.
    Assume symbols are uppercase letters or multi-letter variables (alphanumeric).
    """
    import re
    symbols = set()
    for sentence in sentences:
        tokens = re.findall(r'\b[A-Za-z][A-Za-z0-9_]*\b', sentence)
        for token in tokens:
            if token.lower() not in ['and', 'or', 'not', 'implies', 'iff', 'true', 'false']:
                symbols.add(token)
    return symbols

def evaluate(expr, model):
    """
    Evaluate a propositional logic expression under a given model.
    Supports: and, or, not, parentheses.
    Variables replaced by their True/False values from model.
    """

    for symbol, value in model.items():
        expr = replace_symbol(expr, symbol, str(value))

    expr = expr.replace('∧', ' and ')
    expr = expr.replace('∨', ' or ')
    expr = expr.replace('¬', ' not ')
    expr = expr.replace('→', ' <= ')  
    expr = expr.replace('↔', ' == ')  

    try:
        return bool(eval(expr, {"__builtins__":None}, {}))
    except Exception as e:
        print(f"Error evaluating expression '{expr}': {e}")
        return False

def replace_symbol(expr, symbol, value):
    """
    Replace all occurrences of symbol as a whole word in expr with value.
    """
    import re
    pattern = r'\b' + re.escape(symbol) + r'\b'
    return re.sub(pattern, value, expr)


KB = [
    "(P ∨ Q)",
    "(¬P ∨ R)",
    "(¬Q ∨ R)"
]

alpha = "R"

result = TT_ENTAILS(KB, alpha)
print(f"Does KB entail alpha? {result}")
