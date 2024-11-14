from flask import Flask, request, jsonify, render_template
from sympy import Matrix, symbols

app = Flask(__name__)

# Definir variables de contexto para cálculos simbólicos
x, y, z = symbols('x y z')
variables = {'x': x, 'y': y, 'z': z}

# Ruta principal que renderiza el archivo HTML
@app.route("/")
def index():
    return render_template("index.html")  # Carga el archivo HTML desde la carpeta templates

# Ruta para crear la transformación
@app.route("/calcular_transformacion", methods=["POST"])
def calcular_transformacion():
    data = request.get_json()
    entradas_fx = data.get("entradas_fx", [])
    matriz = []

    try:
        for expr in entradas_fx:
            f = eval(expr, {}, variables)  # Evalúa cada expresión
            fila = [f.coeff(var) for var in [x, y, z]]
            matriz.append(fila)

        matriz = Matrix(matriz)

        # Cálculo del núcleo y la imagen
        ker = matriz.nullspace()
        dim_ker = len(ker)
        base_ker = [[float(val) for val in vec] for vec in ker]  # Convertir a float para serialización

        rango = matriz.rank()
        dim_img = rango
        base_img = [[float(val) for val in vec] for vec in matriz.columnspace()]  # Convertir a float para serialización

        # Inyectividad y sobreyectividad
        inyectiva = "Sí" if dim_ker == 0 else "No"
        sobreyectiva = "Sí" if rango == matriz.rows else "No"
        biyectiva = "Sí" if inyectiva == "Sí" and sobreyectiva == "Sí" else "No"

        resultado = {
            "dim_ker": dim_ker,
            "base_ker": base_ker,
            "dim_img": dim_img,
            "base_img": base_img,
            "inyectiva": inyectiva,
            "sobreyectiva": sobreyectiva,
            "biyectiva": biyectiva
        }
        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": f"Error en el cálculo: {e}"})

# Ruta para evaluar f(x, y, z)
@app.route("/evaluar_funcion", methods=["POST"])
def evaluar_funcion():
    data = request.get_json()
    entradas_fx = data.get("entradas_fx", [])
    valores = data.get("valores", [])
    
    matriz = []
    try:
        for expr in entradas_fx:
            f = eval(expr, {}, variables)
            fila = [f.coeff(var) for var in [x, y, z]]
            matriz.append(fila)

        matriz = Matrix(matriz)
        resultado_f = matriz * Matrix(valores)
        resultado_f = [float(round(val, 2)) for val in resultado_f]  # Convertir a float

        return jsonify({"resultado": resultado_f})

    except Exception as e:
        return jsonify({"error": f"Error al evaluar f(x, y, z): {e}"})

# Ruta para evaluar la inversa f^-1(x, y, z)
@app.route("/evaluar_inversa", methods=["POST"])
def evaluar_inversa():
    data = request.get_json()
    entradas_fx = data.get("entradas_fx", [])
    valores = data.get("valores", [])
    
    matriz = []
    try:
        for expr in entradas_fx:
            f = eval(expr, {}, variables)
            fila = [f.coeff(var) for var in [x, y, z]]
            matriz.append(fila)

        matriz = Matrix(matriz)
        if not matriz.is_square or matriz.det() == 0:
            return jsonify({"error": "La matriz no es invertible"})

        matriz_inv = matriz.inv()
        resultado_f_inv = matriz_inv * Matrix(valores)
        resultado_f_inv = [float(round(val, 2)) for val in resultado_f_inv]  # Convertir a float

        return jsonify({"resultado": resultado_f_inv})

    except Exception as e:
        return jsonify({"error": f"Error al evaluar f^-1(x, y, z): {e}"})

if __name__ == "__main__":
    app.run(debug=True)
