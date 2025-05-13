from numpy.polynomial.legendre import leggauss

def metodo_cuadratura(f, a, b, n=3):
    [x, w] = leggauss(n)
    # Transformar de [-1,1] a [a,b]
    t = 0.5 * ((b - a) * x + (b + a))
    return 0.5 * (b - a) * sum(w[i] * f(t[i]) for i in range(n))
