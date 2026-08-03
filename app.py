# app.py

# ==========================================
# 1. IMPORTACIONES
# ==========================================
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
    layout="centered"
)

# ==========================================
# 3. INICIALIZACIÓN EN MEMORIA
# ==========================================
init_client_db()
cargar_plantillas_iniciales()

# ==========================================
# 4. ENCABEZADO INSTITUCIONAL
# ==========================================
st.title("📐 DELTA Land Aerial Building Surveyors LABS")
st.caption(f"**{COMPANY_INFO['SUBTITLE']}** — *Sistema Profesional de Cotizaciones*")
st.markdown("---")

# ==========================================
# 5. SISTEMA MODULAR DE PESTAÑAS
# ==========================================
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
