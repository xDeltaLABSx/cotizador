# views/template_manager.py
import streamlit as st
from models.template_model import (
    obtener_catalogo_completo,
    guardar_nueva_plantilla,
    actualizar_plantilla_por_id,
    eliminar_plantilla_por_id
)
from services.plantillas import cargar_plantillas_iniciales

def render_template_manager():
    st.subheader("🛠️ Administración de Catálogo de Servicios")
    st.caption("Aquí puedes visualizar todas las plantillas, editar sus fichas técnicas, entregables, exclusiones, eliminar servicios y crear nuevas opciones.")
    
    # 1. Cargamos el catálogo completo
    catalogo = obtener_catalogo_completo()
    servicios = catalogo.get("servicios", [])
    plantillas_base = cargar_plantillas_iniciales()

    # =========================================================================
    # A. LISTADO COMPLETO CON CAMPOS DE EDICIÓN AMPLIADOS
    # =========================================================================
    st.markdown("### Catálogo Actual de Servicios")
    
    if not servicios:
        st.info("No hay plantillas registradas actualmente en tu catálogo.")
    else:
        for index, s in enumerate(servicios, start=1):
            s_id = s.get("id", f"serv_{index}")
            nombre = s.get("nombre", "Servicio sin nombre")
            unique_key = f"{index}_{s_id}"
            
            # Buscamos respaldos por si el JSON no traía los entregables grabados aún
            info_base = plantillas_base.get(nombre, {})
            ent_val = s.get("entregables") or info_base.get("entregables", "")
            exc_val = s.get("exclusiones") or info_base.get("exclusiones", "")
            
            with st.expander(f"📌 {index}. {nombre}"):
                col1, col2 = st.columns(2)
                with col1:
                    edit_nombre = st.text_input("Nombre de la Plantilla", value=nombre, key=f"nom_{unique_key}")
                    edit_unidad = st.text_input("Unidad por Defecto", value=s.get("unidad_default", "m2"), key=f"uni_{unique_key}")
                with col2:
                    edit_precio = st.number_input(
                        "Precio Base Unitario (MXN)",
                        value=float(s.get("precio_unitario_default", 0.0)),
                        format="%.2f",
                        key=f"pre_{unique_key}"
                    )
                
                edit_obj = st.text_area("Objetivo Base", value=s.get("objetivo", ""), height=70, key=f"obj_{unique_key}")
                edit_met = st.text_area("Metodología Técnica", value=s.get("metodologia", ""), height=90, key=f"met_{unique_key}")
                edit_eq = st.text_area("Equipamiento Desplegado", value=s.get("equipo", ""), height=65, key=f"eq_{unique_key}")
                
                # Nuevos campos de Entregables y Exclusiones editables
                edit_ent = st.text_area("Entregables (Uno por línea)", value=ent_val, height=85, key=f"ent_{unique_key}")
                edit_exc = st.text_area("Exclusiones (Uno por línea)", value=exc_val, height=85, key=f"exc_{unique_key}")

                st.markdown("---")
                
                col_btn_ed, col_btn_del = st.columns([1, 1])
                
                with col_btn_ed:
                    if st.button("💾 Guardar Cambios", key=f"btn_save_{unique_key}", type="primary", use_container_width=True):
                        if actualizar_plantilla_por_id(s_id, edit_nombre, edit_obj, edit_met, edit_eq, edit_unidad, edit_precio, edit_ent, edit_exc):
                            st.success(f"✅ ¡Cambios en '{edit_nombre}' guardados correctamente!")
                            st.rerun()
                        else:
                            st.error("❌ No se pudieron guardar los cambios en el archivo.")
                
                with col_btn_del:
                    if st.button("🗑️ Eliminar Plantilla", key=f"btn_del_{unique_key}", use_container_width=True):
                        if eliminar_plantilla_por_id(s_id):
                            st.warning(f"🗑️ Plantilla '{nombre}' eliminada del catálogo.")
                            st.rerun()
                        else:
                            st.error("❌ No se pudo eliminar la plantilla.")

    st.markdown("---")

    # =========================================================================
    # B. FORMULARIO PARA CREAR UNA NUEVA PLANTILLA DESDE CERO
    # =========================================================================
    st.markdown("### ➕ Añadir Nueva Plantilla de Servicio")
    
    with st.form("form_nueva_plantilla", clear_on_submit=True):
        col_new1, col_new2 = st.columns(2)
        with col_new1:
            nuevo_nombre = st.text_input("Nombre de la Nueva Plantilla *", placeholder="Ej. Fotogrametría - Corredores Viales")
            nueva_unidad = st.text_input("Unidad por Defecto *", placeholder="Ej. ha, km, jornada, m2")
        with col_new2:
            nuevo_precio = st.number_input("Precio Base Unitario (MXN) *", min_value=0.0, value=5000.0, format="%.2f")

        nuevo_obj = st.text_area("Objetivo Base *", placeholder="Redacta el objetivo general del servicio...")
        nueva_met = st.text_area("Metodología Técnica *", placeholder="• Paso 1\n• Paso 2...")
        nuevo_eq = st.text_area("Equipamiento Desplegado *", placeholder="• Estación Total\n• Sistema GNSS RTK...")
        nuevo_ent = st.text_area("Entregables por defecto *", placeholder="• Archivo CAD...\n• Archivo CSV...")
        nuevo_exc = st.text_area("Exclusiones por defecto *", placeholder="• No incluye...")

        submitted = st.form_submit_button("⭐ Crear y Guardar Plantilla en el Catálogo")
        
        if submitted:
            if not nuevo_nombre.strip():
                st.error("⚠️ Debes indicar al menos el Nombre de la Plantilla.")
            else:
                if guardar_nueva_plantilla(nuevo_nombre, nuevo_obj, nueva_met, nuevo_eq, nueva_unidad, nuevo_precio, nuevo_ent, nuevo_exc):
                    st.success(f"✅ ¡Plantilla '{nuevo_nombre}' creada con éxito!")
                    st.rerun()
                else:
                    st.error("❌ Ocurrió un error al intentar escribir en el catálogo.")
