import math

funciones_disponibles = [
    {"desc": "f(x) = x^2", "f": lambda x: x**2},
    {"desc": "f(x) = sin(x)", "f": math.sin},
    {"desc": "f(x) = exp(-x^2)", "f": lambda x: math.exp(-x**2)},
    {"desc": "f(x) = ln(x + 1)", "f": lambda x: math.log(x + 1)}
]
