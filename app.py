import streamlit as st
import pandas as pd

st.title("📊 Productividad Total por Oficina (Colocador + Captador)")

uploaded_file = st.file_uploader("Sube un archivo Excel (.xlsx)", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name=0)
        if 'OFICINA COLOCADOR' in df.columns and 'OFICINA CAPTADOR' in df.columns and 'Precio Cierre' in df.columns:
            # Combinar colocador y captador
            colocadores = df[['OFICINA COLOCADOR', 'Precio Cierre']].rename(columns={'OFICINA COLOCADOR': 'OFICINA'})
            captadores = df[['OFICINA CAPTADOR', 'Precio Cierre']].rename(columns={'OFICINA CAPTADOR': 'OFICINA'})
            oficinas = pd.concat([colocadores, captadores], axis=0)
            oficinas = oficinas.dropna(subset=['OFICINA'])

            # Agrupar por oficina
            df_grouped = oficinas.groupby('OFICINA')['Precio Cierre'].sum().reset_index()
            df_grouped = df_grouped.sort_values(by='Precio Cierre', ascending=False)

            st.success("✅ Productividad total calculada con éxito")
            st.dataframe(df_grouped, use_container_width=True)
        else:
            st.error("❌ El archivo debe contener las columnas: 'OFICINA COLOCADOR', 'OFICINA CAPTADOR' y 'Precio Cierre'")
    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
else:
    st.info("📁 Esperando que subas un archivo Excel.")
