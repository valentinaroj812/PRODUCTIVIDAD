import streamlit as st
import pandas as pd
from io import BytesIO
import xlsxwriter

st.title("📊 Reporte de Productividad por Oficina")

uploaded_file = st.file_uploader("Sube un archivo Excel (.xlsx)", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name=0)

        if all(col in df.columns for col in ['OFICINA COLOCADOR', 'OFICINA CAPTADOR', 'Precio Cierre']):
            st.header("🔹 Productividad por Rol")

            # Colocador
            colocador = df[['OFICINA COLOCADOR', 'Precio Cierre']].dropna(subset=['OFICINA COLOCADOR'])
            colocador = colocador.rename(columns={'OFICINA COLOCADOR': 'OFICINA'})
            colocador_grouped = colocador.groupby('OFICINA')['Precio Cierre'].sum().reset_index()
            colocador_grouped = colocador_grouped.sort_values(by='Precio Cierre', ascending=False)
            st.subheader("🟦 Colocador")
            st.dataframe(colocador_grouped, use_container_width=True)

            # Captador
            captador = df[['OFICINA CAPTADOR', 'Precio Cierre']].dropna(subset=['OFICINA CAPTADOR'])
            captador = captador.rename(columns={'OFICINA CAPTADOR': 'OFICINA'})
            captador_grouped = captador.groupby('OFICINA')['Precio Cierre'].sum().reset_index()
            captador_grouped = captador_grouped.sort_values(by='Precio Cierre', ascending=False)
            st.subheader("🟩 Captador")
            st.dataframe(captador_grouped, use_container_width=True)

            # Total (Colocador + Captador)
            st.header("🔹 Productividad Total por Oficina (Colocador + Captador)")
            oficinas_combined = pd.concat([colocador, captador], axis=0)
            total_grouped = oficinas_combined.groupby('OFICINA')['Precio Cierre'].sum().reset_index()
            total_grouped = total_grouped.sort_values(by='Precio Cierre', ascending=False)
            st.dataframe(total_grouped, use_container_width=True)

            # Número de operaciones
            st.header("🔹 Número de Operaciones por Oficina")
            colocador_ops = df['OFICINA COLOCADOR'].value_counts().rename_axis('OFICINA').reset_index(name='Operaciones Colocador')
            captador_ops = df['OFICINA CAPTADOR'].value_counts().rename_axis('OFICINA').reset_index(name='Operaciones Captador')
            total_ops = pd.merge(colocador_ops, captador_ops, on='OFICINA', how='outer').fillna(0)
            total_ops['Operaciones Totales'] = total_ops['Operaciones Colocador'] + total_ops['Operaciones Captador']
            total_ops = total_ops.sort_values(by='Operaciones Totales', ascending=False)
            st.dataframe(total_ops, use_container_width=True)

            # Exportar a Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                colocador_grouped.to_excel(writer, index=False, sheet_name='Colocador')
                captador_grouped.to_excel(writer, index=False, sheet_name='Captador')
                total_grouped.to_excel(writer, index=False, sheet_name='Total')
                total_ops.to_excel(writer, index=False, sheet_name='Operaciones')

            st.download_button(
                label="📥 Descargar reporte completo en Excel",
                data=output.getvalue(),
                file_name="productividad_oficinas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        else:
            st.error("❌ El archivo debe contener las columnas: 'OFICINA COLOCADOR', 'OFICINA CAPTADOR' y 'Precio Cierre'.")

    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
else:
    st.info("📁 Esperando que subas un archivo Excel.")
