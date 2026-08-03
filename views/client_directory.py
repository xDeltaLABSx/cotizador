# views/client_directory.py
import streamlit as st
import pandas as pd
from models.client_model import obtener_todos_los_clientes, eliminar_cliente

def render_client_directory():
    st.subheader("📂 Cartera de Clientes Registrados")
    st.caption("Administra tu base de datos local de constructoras y contactos guardados automáticamente.")
    
    # Obtenemos todos los clientes de SQLite
    clientes = obtener_todos_los_clientes()
    
    if not clientes:
        st.info("Aún no hay clientes registrados. Se agregarán automáticamente al generar tu primera cotización en la pestaña 1.")
        return

    st.markdown("### Listado de Clientes y Contactos")
    
    # Transformamos los datos a una estructura de tabla limpia
    lista_datos = []
    for c in clientes:
        cliente_id, contacto, cargo, empresa, correo, telefono, ultimo_reg = c
        lista_datos.append({
            "ID": cliente_id,
            "Empresa": empresa,
            "Contacto": contacto,
            "Cargo": cargo,
            "Correo": correo if correo else "N/D",
            "Teléfono": telefono if telefono else "N/D",
            "Última Interacción": ultimo_reg
        })
    
    df_clientes = pd.DataFrame(lista_datos)
    
    # Mostramos la tabla principal sin la columna ID para mayor limpieza visual
    st.dataframe(df_clientes.drop(columns=["ID"]), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### 🗑️ Eliminar un Cliente Registrado")
    
    # Selector rápido para elegir y borrar un cliente por su empresa y contacto de forma segura
    opciones_borrar = {f"{row['Empresa']} — {row['Contacto']} (ID: {row['ID']})": row['ID'] for row in lista_datos}
    
    col_sel, col_btn = st.columns([3, 1])
    with col_sel:
        cliente_seleccionado_label = st.selectbox("Selecciona el cliente a eliminar", list(opciones_borrar.keys()), key="select_borrar_cliente")
    
    with col_btn:
        st.write("") # Espaciador vertical
        st.write("")
        if st.button("🗑️ Borrar Cliente", type="primary", use_container_width=True):
            id_a_borrar = opciones_borrar[cliente_seleccionado_label]
            eliminar_cliente(id_a_borrar)
            st.toast("🗑️ Cliente eliminado correctamente de la base de datos.")
            st.rerun()
