from flask import Flask, render_template_string, request
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

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Integración Numérica</title>
    <!-- Importar Tailwind CSS vía CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        html, body {
            height: 100%;
            margin: 0;
        }
        body {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .content {
            flex: 1 0 auto;
            padding-bottom: 60px;
        }
        footer {
            flex-shrink: 0;
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #1f2937;
            color: white;
            text-align: center;
            padding: 1rem 0;
            z-index: 1000;
        }
        .graph-container {
            max-height: 250px;
            overflow: hidden;
        }
        .result-box {
            min-height: 100px;
        }
    </style>
</head>
<body class="bg-gray-100 font-sans">
    <!-- Encabezado -->
    <header class="bg-blue-600 text-white py-6 text-center">
        <h1 class="text-3xl font-bold">Calculadora de Integración Numérica</h1>
        <p class="mt-2 text-lg">Aplica métodos numéricos como Trapecio, Simpson, Romberg y Cuadratura para resolver integrales.</p>
    </header>

    <!-- Navegación de pestañas -->
    <div class="container mx-auto px-4">
        <div class="flex justify-center border-b border-gray-300 mb-4">
            <button class="tab-link px-4 py-2 font-medium text-gray-700 hover:text-blue-600 focus:outline-none {% if request.path == '/' or request.path == '/trapecio' %}border-b-2 border-blue-600 text-blue-600{% endif %}" onclick="window.location.href='/'">Trapecio</button>
            <button class="tab-link px-4 py-2 font-medium text-gray-700 hover:text-blue-600 focus:outline-none {% if request.path == '/simpson' %}border-b-2 border-blue-600 text-blue-600{% endif %}" onclick="window.location.href='/simpson'">Simpson</button>
            <button class="tab-link px-4 py-2 font-medium text-gray-700 hover:text-blue-600 focus:outline-none {% if request.path == '/romberg' %}border-b-2 border-blue-600 text-blue-600{% endif %}" onclick="window.location.href='/romberg'">Romberg</button>
            <button class="tab-link px-4 py-2 font-medium text-gray-700 hover:text-blue-600 focus:outline-none {% if request.path == '/cuadratura' %}border-b-2 border-blue-600 text-blue-600{% endif %}" onclick="window.location.href='/cuadratura'">Cuadratura</button>
        </div>

        <!-- Contenido principal -->
        <div class="content flex flex-col md:flex-row gap-6 mb-6">
            <!-- Formulario (izquierda) -->
            <div class="md:w-1/2 w-full">
                {% if request.path == '/' or request.path == '/trapecio' %}
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <h2 class="text-2xl font-semibold text-gray-800 mb-4 text-center">Método del Trapecio</h2>
                        <form method="post" action="/">
                            <div class="space-y-4">
                                <div>
                                    <label for="funcion" class="block text-sm font-medium text-gray-700">Función (en x):</label>
                                    <input type="text" name="funcion" value="{{ request.form.get('funcion', 'x**2') }}"
                                           class="mt-1 w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                </div>
                                <div>
                                    <label for="a" class="block text-sm font-medium text-gray-700">Límite inferior (a):</label>
                                    <input type="text" name="a" value="{{ request.form.get('a', '0') }}"
                                           class="mt-1 w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                </div>
                                <div>
                                    <label for="b" class="block text-sm font-medium text-gray-700">Límite superior (b):</label>
                                    <input type="text" name="b" value="{{ request.form.get('b', '1') }}"
                                           class="mt-1 w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                </div>
                                <div>
                                    <label for="n" class="block text-sm font-medium text-gray-700">Número de subintervalos (n):</label>
                                    <input type="text" name="n" value="{{ request.form.get('n', '10') }}"
                                           class="mt-1 w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                </div>
                                <div class="text-center">
                                    <input type="submit" value="Calcular"
                                           class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 cursor-pointer transition duration-200">
                                </div>
                            </div>
                        </form>
                    </div>
                {% elif request.path == '/simpson' %}
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <h2 class="text-2xl font-semibold text-gray-800 mb-4 text-center">Método de Simpson</h2>
                        <form method="post" action="/simpson">
                            <div class="space-y-4">
                                <div>
                                    <label for="funcion" class="block text-sm font-medium text-gray-700">Función (en x):</label>
                                    <input type="text" name="funcion" value="{{ request.form.get('funcion', 'x**2') }}"
                                           class="mt-1 w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                </div>
                                <div>
                                    <label for="a" class="block text-sm font-medium text-gray-700">Límite inferior (a):</label>
                                    <input type="text" name="a" value="{{ request.form.get('a', '0') }}"
                                           class="mt-1 w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                </div>
                                <div>
                                    <label for="b" class="block text-sm font-medium text-gray-700">Límite superior (b):</label>
                                    <input type="text" name="b" value="{{ request.form.get('b', '1') }}"
                                           class="mt-1 w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                </div>
                                <div>
                                    <label for="n" class="block text-sm font-medium text-gray-700">Número de subintervalos (n):</label>
                                    <input type="text" name="n" value="{{ request.form.get('n', '10') }}"
                                           class="mt-1 w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                </div>
                                <div class="text-center">
                                    <input type="submit" value="Calcular"
                                           class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 cursor-pointer transition duration-200">
                                </div>
                            </div>
                        </form>
                    </div>
                {% elif request.path == '/romberg' %}
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <h2 class="text-2xl font-semibold text-gray-800 mb-4 text-center">Método de Romberg</h2>
                        <form method="post" action="/romberg">
                            <div class="space-y-4">
                                <div>
                                    <label for="funcion" class="block text-sm font-medium text-gray-700">Función (en x):</label>
                                    <input type="text" name="funcion" value="{{ request.form.get('funcion', 'x**2') }}"
                                           class="mt-1 w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                </div>
                                <div>
                                    <label for="a" class="block text-sm font-medium text-gray-700">Límite inferior (a):</label>
                                    <input type="text" name="a" value="{{ request.form.get('a', '0') }}"
                                           class="mt-1 w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                </div>
                                <div>
                                    <label for="b" class="block text-sm font-medium text-gray-700">Límite superior (b):</label>
                                    <input type="text" name="b" value="{{ request.form.get('b', '1') }}"
                                           class="mt-1 w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                </div>
                                <div class="text-center">
                                    <input type="submit" value="Calcular"
                                           class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 cursor-pointer transition duration-200">
                                </div>
                            </div>
                        </form>
                    </div>
                {% elif request.path == '/cuadratura' %}
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <h2 class="text-2xl font-semibold text-gray-800 mb-4 text-center">Método de Cuadratura</h2>
                        <form method="post" action="/cuadratura">
                            <div class="space-y-4">
                                <div>
                                    <label for="funcion" class="block text-sm font-medium text-gray-700">Función (en x):</label>
                                    <input type="text" name="funcion" value="{{ request.form.get('funcion', 'x**2') }}"
                                           class="mt-1 w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                </div>
                                <div>
                                    <label for="a" class="block text-sm font-medium text-gray-700">Límite inferior (a):</label>
                                    <input type="text" name="a" value="{{ request.form.get('a', '0') }}"
                                           class="mt-1 w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                </div>
                                <div>
                                    <label for="b" class="block text-sm font-medium text-gray-700">Límite superior (b):</label>
                                    <input type="text" name="b" value="{{ request.form.get('b', '1') }}"
                                           class="mt-1 w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                </div>
                                <div>
                                    <label for="n" class="block text-sm font-medium text-gray-700">Número de subintervalos (n):</label>
                                    <input type="text" name="n" value="{{ request.form.get('n', '10') }}"
                                           class="mt-1 w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                </div>
                                <div class="text-center">
                                    <input type="submit" value="Calcular"
                                           class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 cursor-pointer transition duration-200">
                                </div>
                            </div>
                        </form>
                    </div>
                {% endif %}
            </div>

            <!-- Sección de resultado y gráfico (derecha) -->
            <div class="md:w-1/2 w-full">
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h3 class="text-xl font-semibold text-gray-800 mb-4">Resultado:</h3>
                    {% if resultado is not none %}
                        <div class="result-box bg-green-100 p-4 rounded-lg mb-4">
                            <p class="text-green-800 font-medium text-lg">
                                {% if resultado is string %}
                                    {{ resultado }}
                                {% else %}
                                    {{ "%.6f"|format(resultado) }}
                                {% endif %}
                            </p>
                        </div>
                        {% if plot_url %}
                        <div class="graph-container mt-4">
                            <img src="data:image/png;base64,{{ plot_url }}" alt="Gráfica de la integración" class="w-full">
                        </div>
                        {% endif %}
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <!-- Pie de página -->
    <footer class="bg-gray-800 text-white text-center py-4">
        <p>© 2025 Calculadora de Integración Numérica. Todos los derechos reservados.</p>
    </footer>
</body>
</html>
"""

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
    return render_template_string(HTML, resultado=resultado, plot_url=plot_url, request=request)

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

    return render_template_string(HTML, resultado=resultado, plot_url=plot_url, request=request)

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
    return render_template_string(HTML, resultado=resultado, plot_url=plot_url, request=request)

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
    return render_template_string(HTML, resultado=resultado, plot_url=plot_url, request=request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)