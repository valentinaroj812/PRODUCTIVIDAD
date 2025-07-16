# Productividad por Oficina (Streamlit App)

Esta es una aplicación web en Streamlit que calcula la productividad de cada oficina a partir de un archivo Excel.

## Requisitos

- Python 3.7+
- pip

## Instalación

```bash
git clone https://github.com/tu-usuario/productividad-app-streamlit.git
cd productividad-app-streamlit
pip install -r requirements.txt
streamlit run app.py
```

Luego abre tu navegador en la URL que te indica el terminal (por defecto http://localhost:8501)

## Uso

1. Sube un archivo Excel con una hoja que contenga las columnas `OFICINA COLOCADOR` y `Precio Cierre`.
2. Verás una tabla con la suma de productividad por oficina.

## Licencia

MIT
