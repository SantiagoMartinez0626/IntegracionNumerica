import numpy as np

def metodo_romberg(f, a, b, tol=1e-6, max_iter=10):
    R = np.zeros((max_iter, max_iter))
    h = b - a
    R[0, 0] = 0.5 * h * (f(a) + f(b))
    for i in range(1, max_iter):
        h /= 2
        suma = sum(f(a + (2*k - 1)*h) for k in range(1, 2**(i-1)+1))
        R[i, 0] = 0.5 * R[i-1, 0] + h * suma
        for k in range(1, i+1):
            R[i, k] = R[i, k-1] + (R[i, k-1] - R[i-1, k-1]) / (4**k - 1)
        if i > 1 and abs(R[i, i] - R[i-1, i-1]) < tol:
            return R[i, i]
    return R[max_iter-1, max_iter-1]
