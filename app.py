# app.py
import streamlit as st
from config.settings import COMPANY_INFO
from models.client_model import init_client_db
from views.quote_builder import render_quote_builder
from views.template_manager import render_template_manager
from views.client_directory import render_client_directory

# 1. Configurar navegador (icono de regla y título profesional)
st.set_page_config(
    page_title=f"Cotizador | {COMPANY_INFO['NAME']}",
    page_icon="📐",
    layout="centered"
)

# 2. Inicializar la base de datos local de clientes
init_client_db()

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
