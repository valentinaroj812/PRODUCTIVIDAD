from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Productividad por Oficina</title>
    <style>
        body { font-family: Arial; padding: 2em; }
        table, th, td { border: 1px solid black; border-collapse: collapse; padding: 0.5em; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h2>Productividad por Oficina</h2>
    <form method="POST" enctype="multipart/form-data">
        <p>Sube el archivo Excel:</p>
        <input type="file" name="file" accept=".xlsx" required>
        <input type="submit" value="Procesar">
    </form>
    {% if data %}
    <h3>Resultados:</h3>
    <table>
        <tr><th>Oficina</th><th>Productividad (Precio Cierre)</th></tr>
        {% for row in data %}
        <tr><td>{{ row[0] }}</td><td>{{ "{:,.2f}".format(row[1]) }}</td></tr>
        {% endfor %}
    </table>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_excel(file, sheet_name=0)
            df_grouped = df.groupby('OFICINA COLOCADOR')['Precio Cierre'].sum().reset_index()
            df_grouped = df_grouped.sort_values(by='Precio Cierre', ascending=False)
            data = df_grouped.values.tolist()
    return render_template_string(TEMPLATE, data=data)

if __name__ == '__main__':
    app.run(debug=True)
