# views/quote_builder.py
import streamlit as st
from datetime import datetime
from models.template_model import obtener_catalogo_completo, obtener_servicio_por_id, guardar_nueva_plantilla
from models.client_model import buscar_clientes, guardar_o_actualizar_cliente
from services.doc_engine import generar_cotizacion_docx
from config.settings import COMPANY_INFO

def render_quote_builder():
    st.markdown("### 1. Configuración de Cliente y Proyecto")
    
    # Búsqueda y autocompletado inteligente de clientes
    termino = st.text_input("🔍 Buscar cliente anterior (o escribir nuevo)", placeholder="Ej. Constructora... o Ing. Juan...")
    sugerencias = buscar_clientes(termino) if termino else []
    
    col1, col2 = st.columns(2)
    with col1:
        empresa = st.text_input("Empresa / Constructora *", value=sugerencias[0][2] if sugerencias else "Constructora e Inmobiliaria, S.A. de C.V.")
        atencion = st.text_input("A quién va dirigida (Nombre) *", value=sugerencias[0][0] if sugerencias else "Ing. Juan Pérez")
        cargo = st.text_input("Cargo / Departamento", value=sugerencias[0][1] if sugerencias else "Director de Obra")
    with col2:
        ciudad = st.text_input("Ciudad de Emisión", value=COMPANY_INFO["DEFAULT_CITY"])
        proyecto = st.text_input("Nombre / Referencia del Proyecto *", value="Levantamiento Topográfico en Predio")
        correo = st.text_input("Correo (Opcional)", value=sugerencias[0][3] if sugerencias else "")
        telefono = st.text_input("Teléfono (Opcional)", value=sugerencias[0][4] if sugerencias else "")

    st.markdown("---")
    st.markdown("### 2. Selección y Modificación Técnica del Servicio")
    
    catalogo = obtener_catalogo_completo()
    opciones = {s["nombre"]: s["id"] for s in catalogo["servicios"]}
    
    seleccion_nombre = st.selectbox("Seleccione Plantilla Base de Trabajo", list(opciones.keys()))
    servicio_id = opciones[seleccion_nombre]
    servicio_sel = obtener_servicio_por_id(servicio_id)
    
    # Cuadros de texto EDITABLES AL MOMENTO
    objetivo_mod = st.text_area("Objetivo del Proyecto (Editable)", value=servicio_sel["objetivo"], height=80)
    metodologia_mod = st.text_area("Metodología Técnica (Editable)", value=servicio_sel["metodologia"], height=130)
    equipo_mod = st.text_area("Equipamiento Desplegado (Editable)", value=servicio_sel["equipo"], height=80)
    
    # Opción estrella: Guardar modificación como NUEVA plantilla del catálogo
    guardar_como_nueva = st.checkbox("⭐ ¿Guardar esta modificación como NUEVA plantilla para el futuro?")
    nombre_nueva_plantilla = ""
    if guardar_como_nueva:
        nombre_nueva_plantilla = st.text_input("Nombre de tu nueva plantilla", placeholder="Ej. Vuelo Dron - Corredor Vial")

    st.markdown("---")
    st.markdown("### 3. Propuesta Económica")
    
    col_desc, col_cant, col_monto = st.columns([3, 1, 1.5])
    with col_desc:
        desc_concepto = st.text_input("Descripción del Cobro", value=f"Servicios de Topografía - {seleccion_nombre}")
    with col_cant:
        cant_concepto = st.text_input("Cantidad / Unidad", value=f"1 {servicio_sel.get('unidad_default', 'Lote')}")
    with col_monto:
        precio_base = servicio_sel.get('precio_unitario_default', 15000.0)
        monto_concepto = st.number_input("Importe ($ MXN)", value=float(precio_base), step=500.0)

    st.markdown("---")
    st.markdown("### 4. Entregables, Exclusiones y Términos")
    
    entregables_text = st.text_area("Entregables (Uno por línea)", value="\n".join(catalogo["entregables"]), height=80)
    exclusiones_text = st.text_area("Exclusiones (Uno por línea)", value="\n".join(catalogo["exclusiones"]), height=80)
    
    clausulas_text = st.text_area("Cláusulas de Trabajo y Forma de Pago", value=(
        "• Vigencia de la cotización: 15 días hábiles a partir de la fecha de emisión.\n"
        "• Forma de pago: 50% de anticipo para iniciar trabajos en campo y 50% contra entrega de resultados finales.\n"
        "• Los precios no incluyen I.V.A."
    ), height=80)
    
    saludo_text = st.text_input("Saludo de Cierre", value="Agradeciendo de antemano su confianza, quedamos a su entera disposición para cualquier aclaración técnica.")

    # --- MEMORIA DE SESIÓN PARA EL ARCHIVO ---
    if "doc_generado" not in st.session_state:
        st.session_state.doc_generado = None
    if "doc_nombre" not in st.session_state:
        st.session_state.doc_nombre = ""

    st.markdown("---")
    if st.button("🚀 Generar Cotización Formal (Word)", type="primary", use_container_width=True):
        # 1. Guardar cliente en la base de datos
        guardar_o_actualizar_cliente(atencion, cargo, empresa, correo, telefono)
        
        # 2. Si marcó guardar como nueva plantilla, la registramos
        if guardar_como_nueva and nombre_nueva_plantilla:
            guardar_nueva_plantilla(
                nombre=nombre_nueva_plantilla,
                objetivo=objetivo_mod,
                metodologia=metodologia_mod,
                equipo=equipo_mod,
                unidad=servicio_sel.get('unidad_default', 'Lote'),
                precio_base=monto_concepto
            )
            st.toast("✅ ¡Nueva plantilla guardada en tu catálogo!")

        # 3. Empaquetar datos para el motor editorial
        datos_docx = {
            "ciudad": ciudad,
            "fecha_dt": datetime.now(),
            "cliente_atencion": atencion,
            "cliente_cargo": cargo,
            "cliente_empresa": empresa,
            "nombre_proyecto": proyecto,
            "objetivo": objetivo_mod,
            "metodologia": metodologia_mod,
            "equipo": equipo_mod,
            "conceptos_economicos": [{"desc": desc_concepto, "cant": cant_concepto, "monto": monto_concepto}],
            "entregables": [e.strip() for e in entregables_text.split("\n") if e.strip()],
            "exclusiones": [x.strip() for x in exclusiones_text.split("\n") if x.strip()],
            "clausulas": clausulas_text,
            "saludo_final": saludo_text
        }
        
        # 4. Generar el Word impecable sin saltos rotos
        st.session_state.doc_generado = generar_cotizacion_docx(datos_docx)
        empresa_limpia = empresa.replace(" ", "_").replace(".", "")[:20]
        st.session_state.doc_nombre = f"Cotizacion_{empresa_limpia}.docx"
        st.success("✅ ¡Documento generado con membrete y sin saltos de página mal hechos!")

    # Botón de descarga FUERA del flujo para que no falle en Streamlit Cloud
    if st.session_state.doc_generado:
        st.download_button(
            label="📥 Descargar Documento Word (.docx) Impecable",
            data=st.session_state.doc_generado,
            file_name=st.session_state.doc_nombre,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
