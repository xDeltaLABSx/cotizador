# views/client_directory.py
import streamlit as st
import sqlite3
import pandas as pd
from models.client_model import DB_PATH

def render_client_directory():
    st.markdown("### 📂 Cartera de Clientes Registrados")
    st.write("El sistema guarda automáticamente las constructoras y contactos con los que cotizas para autocompletarlos después.")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT nombre_atencion AS Contacto, cargo_departamento AS Cargo, empresa AS Empresa, correo AS Correo, telefono AS Teléfono, ultimo_registro AS Última_Cotización FROM clientes ORDER BY ultimo_registro DESC", conn)
        conn.close()
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Aún no tienes clientes guardados. Se crearán al generar tu primera cotización.")
    except Exception:
        st.info("La base de datos se inicializará cuando crees tu primera cotización en la Pestaña 1.")
