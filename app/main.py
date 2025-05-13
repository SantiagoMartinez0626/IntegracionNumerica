from flask import Flask, render_template, request
from app.integracion.trapecio import metodo_trapecio
from app.integracion.romberg import metodo_romberg
from app.integracion.cuadratura import metodo_cuadratura
from scipy.integrate import simpson
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

def generate_plot(x, y, title, method):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', label='Función')
    
    if method == 'trapecio':
        for i in range(len(x)-1):
            plt.fill_between([x[i], x[i+1]], [y[i], y[i+1]], alpha=0.3)
    elif method == 'simpson':
        plt.plot(x, y, 'r--', alpha=0.5)
    elif method == 'romberg':
        plt.scatter(x, y, color='red', s=50)
    elif method == 'cuadratura':
        plt.scatter(x, y, color='green', s=50)
    
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.legend()
    
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url

@app.route('/', methods=['GET', 'POST'])
def trapecio():
    resultado = None
    plot_url = None
    if request.method == 'POST':
        try:
            funcion_str = request.form['funcion']
            a = float(request.form['a'])
            b = float(request.form['b'])
            n = int(request.form['n'])
            f = lambda x: eval(funcion_str, {"x": x, "np": np})
            x = np.linspace(a, b, 100)
            y = np.array([f(xi) for xi in x])
            resultado = metodo_trapecio(f, a, b, n)
            plot_url = generate_plot(x, y, f'Método del Trapecio - Resultado: {resultado:.6f}', 'trapecio')
        except Exception as e:
            resultado = f"Error: {str(e)}"
    return render_template('index.html', resultado=resultado, plot_url=plot_url, request=request)

@app.route('/simpson', methods=['GET', 'POST'])
def simpson_route():
    resultado = None
    plot_url = None

    if request.method == 'POST':
        try:
            funcion_str = request.form['funcion']
            a = float(request.form['a'])
            b = float(request.form['b'])
            n = int(request.form['n'])

            if n % 2 != 0:
                n += 1

            f = lambda x: eval(funcion_str, {"x": x, "np": np})

            x = np.linspace(a, b, 100 * n // 10)
            y = np.array([f(xi) for xi in x])

            if len(x) != len(y):
                raise ValueError("Longitudes de x e y no coinciden")

            resultado = simpson(y, x)
            plot_url = generate_plot(x, y, f'Método de Simpson - Resultado: {resultado:.6f}', 'simpson')
        
        except Exception as e:
            resultado = f"Error: {str(e)}"
            plot_url = None

    return render_template('index.html', resultado=resultado, plot_url=plot_url, request=request)

@app.route('/romberg', methods=['GET', 'POST'])
def romberg():
    resultado = None
    plot_url = None
    if request.method == 'POST':
        try:
            funcion_str = request.form['funcion']
            a = float(request.form['a'])
            b = float(request.form['b'])
            f = lambda x: eval(funcion_str, {"x": x, "np": np})
            x = np.linspace(a, b, 100)
            y = np.array([f(xi) for xi in x])
            resultado = metodo_romberg(f, a, b)
            plot_url = generate_plot(x, y, f'Método de Romberg - Resultado: {resultado:.6f}', 'romberg')
        except Exception as e:
            resultado = f"Error: {str(e)}"
    return render_template('index.html', resultado=resultado, plot_url=plot_url, request=request)

@app.route('/cuadratura', methods=['GET', 'POST'])
def cuadratura():
    resultado = None
    plot_url = None
    if request.method == 'POST':
        try:
            funcion_str = request.form['funcion']
            a = float(request.form['a'])
            b = float(request.form['b'])
            n = int(request.form['n'])
            f = lambda x: eval(funcion_str, {"x": x, "np": np})
            x = np.linspace(a, b, 100)
            y = np.array([f(xi) for xi in x])
            resultado = metodo_cuadratura(f, a, b, n)
            plot_url = generate_plot(x, y, f'Método de Cuadratura - Resultado: {resultado:.6f}', 'cuadratura')
        except Exception as e:
            resultado = f"Error: {str(e)}"
    return render_template('index.html', resultado=resultado, plot_url=plot_url, request=request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)