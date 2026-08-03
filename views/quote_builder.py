# views/quote_builder.py
import streamlit as st
from datetime import datetime
from models.template_model import obtener_catalogo_completo, obtener_servicio_por_id, guardar_nueva_plantilla
from models.client_model import buscar_clientes, guardar_o_actualizar_cliente
from services.doc_engine import generar_cotizacion_docx
from services.pdf_engine import convertir_docx_a_pdf
from services.drive_engine import guardar_en_drive_y_excel
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
    
    catalogo = obtener_catalogo_completo()
    opciones = {s["nombre"]: s["id"] for s in catalogo["servicios"]}
    
    if not opciones:
        st.error("⚠️ No se encontraron plantillas en data/catalogo_seed.json. Verifica que el archivo esté subido en GitHub.")
        return

    seleccion_nombre = st.selectbox("Seleccione Plantilla Base de Trabajo", list(opciones.keys()))
    servicio_id = opciones[seleccion_nombre]
    servicio_sel = obtener_servicio_por_id(servicio_id)
    
    if not servicio_sel:
        st.error("⚠️ Error al cargar la plantilla seleccionada.")
        return
    
    # Cuadros de texto EDITABLES AL MOMENTO
    objetivo_mod = st.text_area("Objetivo del Proyecto (Editable)", value=servicio_sel["objetivo"], height=80)
    metodologia_mod = st.text_area("Metodología Técnica (Editable)", value=servicio_sel["metodologia"], height=130)
    equipo_mod = st.text_area("Equipamiento Desplegado (Editable)", value=servicio_sel["equipo"], height=80)
    
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

    # --- MEMORIA DE SESIÓN PARA LOS ARCHIVOS ---
    if "doc_word" not in st.session_state:
        st.session_state.doc_word = None
    if "doc_pdf" not in st.session_state:
        st.session_state.doc_pdf = None
    if "doc_nombre" not in st.session_state:
        st.session_state.doc_nombre = ""
    if "datos_cache" not in st.session_state:
        st.session_state.datos_cache = None

    st.markdown("---")
    
    if st.button("🚀 Procesar y Generar Archivos (Word + PDF)", type="primary", use_container_width=True):
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
                    unidad=servicio_sel.get('unidad_default', 'Lote'),
                    precio_base=monto_concepto
                )
                st.toast("✅ ¡Nueva plantilla guardada en tu catálogo!")

            # 3. Empaquetar todos los datos incluyendo metadatos
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
            
            # 4. Generar primero el documento Word maestro con la plantilla base y membrete
            st.session_state.doc_word = generar_cotizacion_docx(datos_completos)
            
            # 5. Generar el PDF pasándole los datos limpios de manera nativa y homologada
            st.session_state.doc_pdf = convertir_docx_a_pdf(datos=datos_completos)
            
            st.session_state.doc_nombre = nombre_personalizado.replace(" ", "_")
            st.session_state.datos_cache = datos_completos
            
            st.success("✅ ¡Archivos Word (.docx) y PDF (.pdf) generados con éxito!")
            
        except Exception as error:
            st.error(f"⚠️ Ocurrió un detalle técnico al procesar los archivos: {str(error)}")

    # Botones de descarga y sincronización con Google Drive / Excel
    if st.session_state.doc_word and st.session_state.doc_pdf:
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.download_button(
                label="📥 Descargar Documento Word (.docx)",
                data=st.session_state.doc_word,
                file_name=f"{st.session_state.doc_nombre}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        with col_d2:
            st.download_button(
                label="📥 Descargar Documento PDF (.pdf)",
                data=st.session_state.doc_pdf,
                file_name=f"{st.session_state.doc_nombre}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
        st.markdown("---")
        st.markdown("#### ☁️ Respaldo en Google Drive y Excel (Google Sheets)")
        
        folder_id = st.secrets.get("DRIVE_FOLDER_ID", "PEGA_AQUI_ID_DE_TU_CARPETA_DRIVE")
        sheet_id = st.secrets.get("SHEETS_EXCEL_ID", "PEGA_AQUI_ID_DE_TU_EXCEL")
        
        if st.button("☁️ Subir Word y PDF a Drive y Registrar Fila en Excel", use_container_width=True):
            exito, mensaje = guardar_en_drive_y_excel(
                st.session_state.datos_cache,
                st.session_state.doc_word,
                st.session_state.doc_pdf,
                st.session_state.doc_nombre,
                folder_id,
                sheet_id
            )
            if exito:
                st.success(mensaje)
            else:
                st.warning(mensaje)
