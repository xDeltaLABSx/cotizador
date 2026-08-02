# views/template_manager.py
import streamlit as st
from models.template_model import obtener_catalogo_completo, guardar_nueva_plantilla

def render_template_manager():
    st.markdown("### 🛠️ Administración de Catálogo de Servicios")
    st.write("Aquí puedes visualizar todas las plantillas que el sistema tiene cargadas y añadir nuevas de forma permanente.")
    
    catalogo = obtener_catalogo_completo()
    
    st.markdown("#### Catálogo Actual de Servicios")
    for serv in catalogo["servicios"]:
        with st.expander(f"📌 {serv['nombre']}"):
            st.markdown(f"**Objetivo Base:** {serv['objetivo']}")
            st.markdown(f"**Metodología:**\n{serv['metodologia']}")
            st.markdown(f"**Equipo:**\n{serv['equipo']}")
            st.caption(f"Unidad por defecto: {serv.get('unidad_default', 'N/A')} | Precio base: ${serv.get('precio_unitario_default', 0):,.2f} MXN")

    st.markdown("---")
    st.markdown("#### ➕ Crear una Plantilla Nueva Directamente")
    with st.form("form_nueva_plantilla"):
        nombre = st.text_input("Nombre del Servicio / Plantilla", placeholder="Ej. Nivelación Diferencial para Carretera")
        objetivo = st.text_area("Objetivo")
        metodologia = st.text_area("Metodología")
        equipo = st.text_area("Equipo Técnico")
        unidad = st.text_input("Unidad (ej. km, m2, lote)", value="km")
        precio = st.number_input("Precio Base Unitario ($ MXN)", value=5000.0, step=500.0)
        
        if st.form_submit_button("Guardar Plantilla en el Catálogo"):
            if nombre and objetivo:
                guardar_nueva_plantilla(nombre, objetivo, metodologia, equipo, unidad, precio)
                st.success("✅ ¡Plantilla agregada a tu catálogo para futuras cotizaciones!")
                st.rerun()
            else:
                st.warning("Por favor ingresa al menos un Nombre y un Objetivo.")
