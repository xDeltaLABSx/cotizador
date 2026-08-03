cargar_plantillas_iniciales()# app.py
import streamlit as st
from config.settings import COMPANY_INFO
from models.client_model import init_client_db
from views.quote_builder import render_quote_builder
from views.template_manager import render_template_manager
from views.client_directory import render_client_directory
from services.plantillas import cargar_plantillas_iniciales

# ==========================================
# 2. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="DELTA LABS - Cotizador",
    page_icon="🛰️",
    layout="wide"
)

# ==========================================
# 3. INICIALIZAR LAS PLANTILLAS EN MEMORIA
# ==========================================
cargar_plantillas_iniciales()  # <-- ¡AQUÍ ES DONDE DEBE IR!
# =========================================================================
# SECCIÓN 2: SELECCIÓN, EDICIÓN Y VERSIONES DEL SERVICIO
# =========================================================================
st.subheader("2. Selección y Modificación Técnica del Servicio")

# 1. Selector principal
servicio_base = st.selectbox(
    "Seleccione Plantilla Base de Trabajo / Servicio", 
    list(st.session_state["plantillas_dinamicas"].keys())
)

current_data = st.session_state["plantillas_dinamicas"][servicio_base]

# 2. Tarjeta desplegable para editar en tiempo real
with st.expander(f"✏️ Editar Ficha Técnica: {servicio_base}", expanded=True):
    obj_edit = st.text_area("Objetivo Base", value=current_data["objetivo"], height=80)
    met_edit = st.text_area("Metodología", value=current_data["metodología"], height=100)
    eq_edit = st.text_area("Equipo", value=current_data["equipo"], height=70)

    col1, col2 = st.columns(2)
    with col1:
        unidad_edit = st.text_input("Unidad de Medida", value=current_data["unidad"])
    with col2:
        precio_edit = st.number_input("Precio Base Unitario (MXN)", value=float(current_data["precio_base"]), format="%.2f")

    if st.button("💾 Actualizar Plantilla Activa"):
        st.session_state["plantillas_dinamicas"][servicio_base] = {
            "unidad": unidad_edit,
            "precio_base": precio_edit,
            "objetivo": obj_edit,
            "metodología": met_edit,
            "equipo": eq_edit
        }
        st.success("¡Plantilla actualizada para esta sesión!")

# 3. Guardado y carga de versiones personalizadas
with st.expander("📑 Guardar / Cargar Versiones Personalizadas", expanded=False):
    nombre_version = st.text_input("Nombre de esta Versión (ej. 'Cotización Cliente XYZ')", value=f"{servicio_base} - V1")

    if st.button("📥 Guardar como Nueva Versión"):
        version_id = f"{servicio_base} | {nombre_version}"
        st.session_state["historial_versiones"][version_id] = {
            "servicio_base": servicio_base,
            "unidad": unidad_edit, "precio_base": precio_edit,
            "objetivo": obj_edit, "metodología": met_edit, "equipo": eq_edit
        }
        st.success("¡Versión guardada en el historial!")

    if st.session_state["historial_versiones"]:
        ver_sel = st.selectbox("Versiones guardadas:", list(st.session_state["historial_versiones"].keys()))
        if st.button("🔄 Cargar Versión Seleccionada"):
            v_data = st.session_state["historial_versiones"][ver_sel]
            st.session_state["plantillas_dinamicas"][v_data["servicio_base"]] = {
                "unidad": v_data["unidad"], "precio_base": v_data["precio_base"],
                "objetivo": v_data["objetivo"], "metodología": v_data["metodología"], "equipo": v_data["equipo"]
            }
            st.success("¡Versión cargada con éxito!")

# 4. Cálculo de cantidades y costos
col_a, col_b = st.columns(2)
with col_a:
    cantidad_area = st.number_input(f"Cantidad / Área [{unidad_edit}]:", min_value=0.0, value=1.0, format="%.2f")
with col_b:
    subtotal = cantidad_area * precio_edit
    st.metric(label="Subtotal Estimado (MXN)", value=f"${subtotal:,.2f}")
# =========================================================================

# 3. Encabezado institucional
st.title("📐 DELTA Land Aerial Building Surveyors LABS")
st.caption(f"**{COMPANY_INFO['SUBTITLE']}** — *Sistema Profesional de Cotizaciones*")
st.markdown("---")

# 4. Sistema modular de Pestañas
tab_cotizador, tab_plantillas, tab_clientes = st.tabs([
    "📝 1. Cotizador Pro",
    "🛠️ 2. Administrador de Plantillas",
    "📂 3. Cartera de Clientes"
])

with tab_cotizador:
    render_quote_builder()

with tab_plantillas:
    render_template_manager()

with tab_clientes:
    render_client_directory()
