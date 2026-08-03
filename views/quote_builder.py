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
    # =========================================================================
    # 1. CONFIGURACIÓN DE CLIENTE Y PROYECTO
    # =========================================================================
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

    # =========================================================================
    # 2. SELECCIÓN Y MODIFICACIÓN TÉCNICA DEL SERVICIO
    # =========================================================================
    st.markdown("### 2. Selección y Modificación Técnica del Servicio")
    
    # 1. Leer el catálogo oficial desde models.template_model (conectado a tu Administrador de Plantillas)
    catalogo = obtener_catalogo_completo()
    
    # --- SINCRONIZACIÓN AUTOMÁTICA CON LAS 21 PLANTILLAS TÉCNICAS ---
    plantillas_base = cargar_plantillas_iniciales()
    
    if not catalogo:
        catalogo = {"servicios": [], "entregables": [], "exclusiones": []}
    if "servicios" not in catalogo:
        catalogo["servicios"] = []
        
    nombres_existentes = {s["nombre"] for s in catalogo["servicios"]}
    for nombre, s_data in plantillas_base.items():
        if nombre not in nombres_existentes:
            catalogo["servicios"].append({
                "id": nombre.lower().replace(" - ", "_").replace(" ", "_").replace("(", "").replace(")", "").replace("&", "y"),
                "nombre": nombre,
                "objetivo": s_data.get("objetivo", ""),
                "metodologia": s_data.get("metodología", s_data.get("metodologia", "")),
                "equipo": s_data.get("equipo", ""),
                "unidad_default": s_data.get("unidad", "m2"),
                "precio_unitario_default": s_data.get("precio_base", 10.0),
                "area_min": s_data.get("area_min", 1.0),
                "precio_min": s_data.get("precio_min", 10.0),
                "precio_extra": s_data.get("precio_extra", 0.0)
            })
    # -----------------------------------------------------------------

    opciones = {s["nombre"]: s["id"] for s in catalogo["servicios"]}
    
    if not opciones:
        st.error("⚠️ No se encontraron plantillas en tu catálogo ni en services/plantillas.py.")
        return

    seleccion_nombre = st.selectbox("Seleccione Plantilla Base de Trabajo", list(opciones.keys()))
    servicio_id = opciones[seleccion_nombre]
    
    # Buscamos la ficha seleccionada en el catálogo vinculado
    servicio_sel = next((s for s in catalogo["servicios"] if s["id"] == servicio_id or s["nombre"] == seleccion_nombre), None)
    
    if not servicio_sel:
        st.error("⚠️ Error al cargar la plantilla seleccionada.")
        return
    
    # Cuadros de texto EDITABLES AL MOMENTO (conectados con tu ficha técnica)
    objetivo_mod = st.text_area("Objetivo del Proyecto (Editable)", value=servicio_sel.get("objetivo", ""), height=80)
    metodologia_mod = st.text_area("Metodología Técnica (Editable)", value=servicio_sel.get("metodologia", ""), height=130)
    equipo_mod = st.text_area("Equipamiento Desplegado (Editable)", value=servicio_sel.get("equipo", ""), height=80)
    
    # Opción: Guardar modificación como NUEVA plantilla del catálogo (Se vinculará a tu Administrador de Plantillas)
    guardar_como_nueva = st.checkbox("⭐ ¿Guardar esta modificación como NUEVA plantilla para el futuro?")
    nombre_nueva_plantilla = ""
    if guardar_como_nueva:
        nombre_nueva_plantilla = st.text_input("Nombre de tu nueva plantilla", placeholder="Ej. Vuelo Dron - Corredor Vial")
    
    st.markdown("---")

    # =========================================================================
    # 3. PROPUESTA ECONÓMICA (Cálculo Dinámico según m2, ha, jornada, lote o semana)
    # =========================================================================
    st.markdown("### 3. Propuesta Económica")
    
    # 1. Obtenemos los parámetros exactos de tu tabla oficial
    area_min = float(servicio_sel.get("area_min", 1.0))
    precio_min = float(servicio_sel.get("precio_min", 1000.0))
    precio_extra = float(servicio_sel.get("precio_extra", 0.0))
    unidad_act = str(servicio_sel.get("unidad_default", servicio_sel.get("unidad", "m2"))).strip().lower()
    
    # 2. Configuración dinámica del título y comportamiento según la unidad
    config_unidades = {
        "m2": {
            "etiqueta": "Área del Proyecto [m2]:",
            "paso": 50.0,
            "ayuda": "Superficie total a levantar en metros cuadrados."
        },
        "ha": {
            "etiqueta": "Superficie del Proyecto [ha]:",
            "paso": 1.0,
            "ayuda": "Superficie total en hectáreas."
        },
        "jornada": {
            "etiqueta": "Número de Jornadas [jornadas]:",
            "paso": 1.0,
            "ayuda": "Días o jornadas operativas de trabajo en campo/gabinete."
        },
        "lote": {
            "etiqueta": "Cantidad de Lotes / Puntos [lotes]:",
            "paso": 1.0,
            "ayuda": "Número de lotes, vértices o líneas base a procesar."
        },
        "semana": {
            "etiqueta": "Tiempo de Asignación [semanas]:",
            "paso": 1.0,
            "ayuda": "Semanas completas de renta o asignación de brigada."
        }
    }

    cfg = config_unidades.get(unidad_act, {
        "etiqueta": f"Cantidad / Volumen [{unidad_act}]:",
        "paso": 1.0,
        "ayuda": f"Ingrese la cantidad total en {unidad_act}."
    })
    
    # 3. Captura dinámica con el título y unidad correctos
    col_cant, col_info_calc = st.columns([1, 2])
    with col_cant:
        cantidad_area = st.number_input(
            label=cfg["etiqueta"],
            min_value=0.0,
            value=float(max(1.0, area_min)),
            step=cfg["paso"],
            format="%.2f",
            help=cfg["ayuda"],
            key=f"input_cant_{servicio_id}"
        )
        
    # 4. Lógica de cálculo automática respetando el mínimo de tu tabla
    if cantidad_area <= area_min:
        estimado_auto = precio_min
        excedente_qty = 0.0
        costo_excedente = 0.0
        detalle_texto = f"Aplica **Tarifa Mínima Base**: **${precio_min:,.2f} MXN** (cubre hasta {area_min:,.2f} {unidad_act})."
    else:
        excedente_qty = cantidad_area - area_min
        costo_excedente = excedente_qty * precio_extra
        estimado_auto = precio_min + costo_excedente
        detalle_texto = (
            f"**Tarifa Mínima Base** (${precio_min:,.2f} MXN por los primeros {area_min:,.2f} {unidad_act}) + "
            f"**Excedente** ({excedente_qty:,.2f} {unidad_act} × ${precio_extra:,.2f} MXN = ${costo_excedente:,.2f} MXN)."
        )

    with col_info_calc:
        st.info(f"💡 **Cálculo Sugerido según Tabla DELTA LABS:**\n{detalle_texto}\n\n**Total Sugerido:** `${estimado_auto:,.2f} MXN`")

    st.markdown("---")

    # 5. Ajuste final modificable por el usuario
    col_desc, col_monto, col_iva = st.columns([2, 1.2, 1])
    with col_desc:
        desc_concepto = st.text_input("Descripción del Cobro", value=f"Servicios de Topografía - {seleccion_nombre}")
    
    with col_monto:
        monto_concepto = st.number_input(
            "Importe Final a Cotizar ($ MXN) *", 
            value=float(estimado_auto), 
            min_value=0.0,
            step=500.0,
            format="%.2f",
            help="Puedes modificar o redondear libremente el monto antes de generar tu Word."
        )
        
    with col_iva:
        incluye_iva = st.checkbox("Incluir IVA (16%)", value=False)
        if incluye_iva:
            total_calc = monto_concepto * 1.16
            st.metric(label="Total con IVA", value=f"${total_calc:,.2f}")
        else:
            st.metric(label="Importe Netto", value=f"${monto_concepto:,.2f}")

    st.markdown("---")

# =========================================================================
    # 4. ENTREGABLES, EXCLUSIONES Y TÉRMINOS (Con actualización automática por servicio)
    # =========================================================================
    st.markdown("### 4. Entregables, Exclusiones y Términos")
    
    # 1. Detectamos si el usuario cambió de servicio en el selectbox superior
    if "ultimo_servicio_seleccionado" not in st.session_state or st.session_state["ultimo_servicio_seleccionado"] != servicio_id:
        st.session_state["ultimo_servicio_seleccionado"] = servicio_id
        # Limpiamos las memorias temporales para forzar la carga de los nuevos textos del servicio
        for k in ["cache_entregables", "cache_exclusiones"]:
            if k in st.session_state:
                del st.session_state[k]

    # 2. Obtenemos los textos oficiales definidos en el servicio activo
    entregables_default = servicio_sel.get("entregables", (
        "Archivos CAD (DWG / DXF) con planimetría, retícula UTM y curvas de nivel.\n"
        "Archivo de Coordenadas (CSV compatible con Trimble Coordinate Manager y Excel).\n"
        "Memoria Técnica Descriptiva y Reporte Fotográfico del proyecto."
    ))
    
    exclusiones_default = servicio_sel.get("exclusiones", (
        "No incluye brechas, tala, roza ni desmonte de vegetación para apertura de líneas de vista.\n"
        "No incluye pago de permisos, derechos de paso ni gestiones municipales para accesos a predios privados.\n"
        "El cliente garantizará el libre acceso y condiciones de seguridad para la brigada técnica en la zona de trabajo."
    ))

    # 3. Inicializamos los valores en session_state si no existen para este servicio
    if "cache_entregables" not in st.session_state:
        st.session_state["cache_entregables"] = entregables_default
    if "cache_exclusiones" not in st.session_state:
        st.session_state["cache_exclusiones"] = exclusiones_default

    # 4. Cajas de texto conectadas al estado para que cambien al instante
    entregables_text = st.text_area(
        "Entregables (Uno por línea)", 
        value=st.session_state["cache_entregables"], 
        height=95,
        key="box_entregables_dinamico"
    )
    
    exclusiones_text = st.text_area(
        "Exclusiones (Uno por línea)", 
        value=st.session_state["cache_exclusiones"], 
        height=95,
        key="box_exclusiones_dinamico"
    )
    
    clausulas_text = st.text_area("Cláusulas de Trabajo y Forma de Pago", value=(
        "• Vigencia de la cotización: 15 días hábiles a partir de la fecha de emisión.\n"
        "• Forma de pago: 50% de anticipo para iniciar trabajos en campo y 50% contra entrega de resultados finales.\n"
        "• Los precios no incluyen I.V.A."
    ), height=80, key="box_clausulas_dinamico")
    
    saludo_text = st.text_input(
        "Saludo de Cierre", 
        value="Agradeciendo de antemano su confianza, quedamos a su entera disposición para cualquier aclaración técnica.",
        key="box_saludo_dinamico"
    )

    # --- MEMORIA DE SESIÓN PARA EL ARCHIVO WORD ---
    if "doc_word" not in st.session_state:
        st.session_state.doc_word = None
    if "doc_nombre" not in st.session_state:
        st.session_state.doc_nombre = ""

    st.markdown("---")
    
    # =========================================================================
    # 5. EMISIÓN DE COTIZACIÓN Y RESPALDO
    # =========================================================================
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
                    unidad=servicio_sel.get('unidad_default', 'm2'),
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
                "conceptos_economicos": [{"desc": desc_concepto, "cant": cantidad_area, "monto": monto_concepto}],
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
