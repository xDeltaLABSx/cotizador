# views/client_directory.py
import streamlit as st
from models.client_model import buscar_clientes  # <-- Importamos solo la función de búsqueda

def render_client_directory():
    st.subheader("📂 Cartera de Clientes Registrados")
    st.caption("El sistema muestra los contactos y constructoras guardados automáticamente en tu Google Sheet en la nube.")
    
    # Obtenemos todos los clientes registrados llamando a la función sin filtro
    clientes = buscar_clientes("") 
    
    if not clientes:
        st.info("Aún no hay clientes registrados en tu Google Sheets. Se agregarán automáticamente al generar tu primera cotización.")
        return

    # Si hay clientes, los mostramos en una tabla limpia o formato amigable
    import pandas as pd
    df_clientes = pd.DataFrame(clientes, columns=["Contacto", "Cargo", "Empresa", "Correo", "Teléfono"])
    st.dataframe(df_clientes, use_container_width=True)
