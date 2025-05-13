def metodo_simpson(f, a, b, n):
    if n % 2 != 0:
        raise ValueError("n debe ser par para el método de Simpson")
    h = (b - a) / n
    suma = f(a) + f(b)
    for i in range(1, n):
        coef = 4 if i % 2 != 0 else 2
        suma += coef * f(a + i*h)
    return h * suma / 3
