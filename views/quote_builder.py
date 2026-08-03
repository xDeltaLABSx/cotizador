# views/quote_builder.py
import streamlit as st
from datetime import datetime
from models.template_model import obtener_catalogo_completo, obtener_servicio_por_id, guardar_nueva_plantilla
from models.client_model import buscar_clientes, guardar_o_actualizar_cliente
from services.doc_engine import generar_cotizacion_docx
from services.drive_engine import guardar_en_drive_y_excel
from services.plantillas import cargar_plantillas_iniciales
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
        ciudad = st.text_input("Ciudad de Emisión", value=COMPANY_INFO.get("DEFAULT_CITY", "Ciudad de México"))
        proyecto = st.text_input("Nombre / Referencia del Proyecto *", value="Levantamiento Topográfico en Predio")
        correo = st.text_input("Correo (Opcional)", value=sugerencias[0][3] if sugerencias else "")
        telefono = st.text_input("Teléfono (Opcional)", value=sugerencias[0][4] if sugerencias else "")

    # --- BLOQUE: METADATOS DE WINDOWS Y NOMBRES DE ARCHIVO ---
    with st.expander("🏷️ Personalizar Nombre de Archivo y Propiedades Word (Metadatos)"):
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            nombre_personalizado = st.text_input("Nombre de Archivo (Sin extensión)", value=f"Cotizacion_{empresa.replace(' ', '_')[:15]}")
            autor_meta = st.text_input("Autor del Documento", value="DELTA")
        with col_meta2:
            titulo_meta = st.text_input("Título / Código de Proyecto", value="32826 - TIJ - RSR Trazo")
            etiquetas_meta = st.text_input("Etiquetas / Keywords", value="32826 - TIJ - RSR Trazo, Topografía, Geodesia")

    st.markdown("---")
    st.markdown("### 2. Selección y Modificación Técnica del Servicio")
    
    # Nos aseguramos de que las plantillas externas estén cargadas sin ensuciar la vista
    if "plantillas_dinamicas" not in st.session_state or not st.session_state["plantillas_dinamicas"]:
        cargar_plantillas_iniciales()
        
    opciones = st.session_state.get("plantillas_dinamicas", {})
    
    if not opciones:
        st.error("⚠️ No se pudieron cargar las plantillas desde services/plantillas.py.")
        return

    seleccion_nombre = st.selectbox("Seleccione Plantilla Base de Trabajo", list(opciones.keys()))
    servicio_sel = opciones[seleccion_nombre]
    
    # Cuadros de texto EDITABLES AL MOMENTO (cargados limpios desde tu archivo externo)
    objetivo_mod = st.text_area("Objetivo del Proyecto (Editable)", value=servicio_sel.get("objetivo", ""), height=80)
    metodologia_mod = st.text_area("Metodología Técnica (Editable)", value=servicio_sel.get("metodología", ""), height=130)
    equipo_mod = st.text_area("Equipamiento Desplegado (Editable)", value=servicio_sel.get("equipo", ""), height=80)
    
    # Opción: Guardar modificación como NUEVA plantilla del catálogo
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
        cant_concepto = st.text_input("Cantidad / Unidad", value=f"1 {servicio_sel.get('unidad', 'Lote')}")
    with col_monto:
        precio_base = servicio_sel.get('precio_base', 15000.0)
        monto_concepto = st.number_input("Importe ($ MXN)", value=float(precio_base), step=500.0)

    st.markdown("---")
    st.markdown("### 4. Entregables, Exclusiones y Términos")
    
    entregables_text = st.text_area("Entregables (Uno por línea)", value=(
        "Archivos CAD (DWG / DXF) con planimetría, retícula UTM y curvas de nivel.\n"
        "Archivo de Coordenadas (CSV compatible con Trimble Coordinate Manager y Excel).\n"
        "Memoria Técnica Descriptiva y Reporte Fotográfico del proyecto."
    ), height=80)
    
    exclusiones_text = st.text_area("Exclusiones (Uno por línea)", value=(
        "No incluye brechas, tala, roza ni desmonte de vegetación para apertura de líneas de vista.\n"
        "No incluye pago de permisos, derechos de paso ni gestiones municipales para accesos a predios privados.\n"
        "El cliente garantizará el libre acceso y condiciones de seguridad para la brigada técnica en la zona de trabajo."
    ), height=80)
    
    clausulas_text = st.text_area("Cláusulas de Trabajo y Forma de Pago", value=(
        "• Vigencia de la cotización: 15 días hábiles a partir de la fecha de emisión.\n"
        "• Forma de pago: 50% de anticipo para iniciar trabajos en campo y 50% contra entrega de resultados finales.\n"
        "• Los precios no incluyen I.V.A."
    ), height=80)
    
    saludo_text = st.text_input("Saludo de Cierre", value="Agradeciendo de antemano su confianza, quedamos a su entera disposición para cualquier aclaración técnica.")

    # --- MEMORIA DE SESIÓN PARA EL ARCHIVO WORD ---
    if "doc_word" not in st.session_state:
        st.session_state.doc_word = None
    if "doc_nombre" not in st.session_state:
        st.session_state.doc_nombre = ""

    st.markdown("---")
    
    if st.button("🚀 Generar Word y Subir a Google Drive en Automático", type="primary", use_container_width=True):
        try:
            # 1. Guardar cliente en la base de datos local
            guardar_o_actualizar_cliente(atencion, cargo, empresa, correo, telefono)
            
            # 2. Registrar nueva plantilla si el usuario lo marcó
            if guardar_como_nueva and nombre_nueva_plantilla:
                guardar_nueva_plantilla(
                    nombre=nombre_nueva_plantilla,
                    objetivo=objetivo_mod,
                    metodologia=metodologia_mod,
                    equipo=equipo_mod,
                    unidad=servicio_sel.get('unidad', 'Lote'),
                    precio_base=monto_concepto
                )
                st.toast("✅ ¡Nueva plantilla guardada en tu catálogo!")

            # 3. Empaquetar datos incluyendo metadatos
            datos_completos = {
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
                "saludo_final": saludo_text,
                "autor_meta": autor_meta,
                "titulo_meta": titulo_meta,
                "etiquetas_meta": etiquetas_meta
            }
            
            # 4. Generar el documento Word maestro basado en tu plantilla oficial
            doc_bytes = generar_cotizacion_docx(datos_completos)
            nombre_archivo = nombre_personalizado.replace(" ", "_")
            
            st.session_state.doc_word = doc_bytes
            st.session_state.doc_nombre = nombre_archivo
            
            # 5. SUBIDA AUTOMÁTICA A GOOGLE DRIVE EN SEGUNDO PLANO
            folder_id = st.secrets.get("DRIVE_FOLDER_ID", "1l0AxPvFgqbqc-brpuqZDj1o1k50Qd3UT")
            sheet_id = st.secrets.get("SHEETS_EXCEL_ID", "")
            
            exito, mensaje = guardar_en_drive_y_excel(
                datos_completos,
                doc_bytes,
                None,  # Sin PDF
                nombre_archivo,
                folder_id,
                sheet_id
            )
            
            if exito:
                st.success("✅ ¡Documento Word generado y respaldado en Google Drive en automático!")
            else:
                st.success("✅ ¡Documento Word generado con éxito!")
                st.warning(f"Aviso de Drive: {mensaje}")
            
        except Exception as error:
            st.error(f"⚠️ Ocurrió un detalle técnico al procesar el archivo: {str(error)}")

    # Botón de descarga directa del Word para tu uso inmediato
    if st.session_state.doc_word:
        st.download_button(
            label="📥 Descargar Documento Word (.docx)",
            data=st.session_state.doc_word,
            file_name=f"{st.session_state.doc_nombre}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
