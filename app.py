import streamlit as st
import pandas as pd

st.title("📊 Productividad por Oficina")

uploaded_file = st.file_uploader("Sube un archivo Excel (.xlsx)", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name=0)
        if 'OFICINA COLOCADOR' in df.columns and 'Precio Cierre' in df.columns:
            df_grouped = df.groupby('OFICINA COLOCADOR')['Precio Cierre'].sum().reset_index()
            df_grouped = df_grouped.sort_values(by='Precio Cierre', ascending=False)

            st.success("✅ Productividad calculada con éxito")
            st.dataframe(df_grouped, use_container_width=True)
        else:
            st.error("❌ El archivo no contiene las columnas necesarias: 'OFICINA COLOCADOR' y 'Precio Cierre'")
    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
else:
    st.info("📁 Esperando que subas un archivo Excel.")
