# views/template_manager.py
import streamlit as st
from models.template_model import (
    obtener_catalogo_completo,
    guardar_nueva_plantilla,
    actualizar_plantilla_por_id,
    eliminar_plantilla_por_id
)

def render_template_manager():
    st.subheader("🛠️ Administración de Catálogo de Servicios")
    st.caption("Aquí puedes visualizar todas las plantillas, editar sus fichas técnicas, eliminar servicios y crear nuevas opciones permanentes.")
    
    # 1. Cargamos el catálogo completo (incluyendo las 21 plantillas sincronizadas)
    catalogo = obtener_catalogo_completo()
    servicios = catalogo.get("servicios", [])

    # =========================================================================
    # A. LISTADO COMPLETO CON CAJAS EDITABLES Y BOTONES DE GUARDAR / BORRAR
    # =========================================================================
    st.markdown("### Catálogo Actual de Servicios")
    
    if not servicios:
        st.info("No hay plantillas registradas actualmente en tu catálogo.")
    else:
        for index, s in enumerate(servicios, start=1):
            s_id = s.get("id", f"serv_{index}")
            nombre = s.get("nombre", "Servicio sin nombre")
            
            # Cada servicio se abre en su propia tarjeta desplegable
            with st.expander(f"📌 {index}. {nombre}"):
                col1, col2 = st.columns(2)
                with col1:
                    edit_nombre = st.text_input("Nombre de la Plantilla", value=nombre, key=f"nom_{s_id}")
                    edit_unidad = st.text_input("Unidad por Defecto", value=s.get("unidad_default", "m2"), key=f"uni_{s_id}")
                with col2:
                    edit_precio = st.number_input(
                        "Precio Base Unitario (MXN)",
                        value=float(s.get("precio_unitario_default", 0.0)),
                        format="%.2f",
                        key=f"pre_{s_id}"
                    )
                
                edit_obj = st.text_area("Objetivo Base", value=s.get("objetivo", ""), height=80, key=f"obj_{s_id}")
                edit_met = st.text_area("Metodología Técnica", value=s.get("metodologia", ""), height=110, key=f"met_{s_id}")
                edit_eq = st.text_area("Equipamiento Desplegado", value=s.get("equipo", ""), height=70, key=f"eq_{s_id}")

                st.markdown("---")
                
                # Botones de acción dentro de la misma tarjeta
                col_btn_ed, col_btn_del = st.columns([1, 1])
                
                with col_btn_ed:
                    if st.button("💾 Guardar Cambios", key=f"btn_save_{s_id}", type="primary", use_container_width=True):
                        if actualizar_plantilla_por_id(s_id, edit_nombre, edit_obj, edit_met, edit_eq, edit_unidad, edit_precio):
                            st.success(f"✅ ¡Cambios en '{edit_nombre}' guardados correctamente!")
                            st.rerun()
                        else:
                            st.error("❌ No se pudieron guardar los cambios en data/catalogo_seed.json.")
                
                with col_btn_del:
                    if st.button("🗑️ Eliminar Plantilla", key=f"btn_del_{s_id}", use_container_width=True):
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

        submitted = st.form_submit_button("⭐ Crear y Guardar Plantilla en el Catálogo")
        
        if submitted:
            if not nuevo_nombre.strip():
                st.error("⚠️ Debes indicar al menos el Nombre de la Plantilla.")
            else:
                if guardar_nueva_plantilla(nuevo_nombre, nuevo_obj, nueva_met, nuevo_eq, nueva_unidad, nuevo_precio):
                    st.success(f"✅ ¡Plantilla '{nuevo_nombre}' creada! Ya está disponible en la lista y en el Cotizador.")
                    st.rerun()
                else:
                    st.error("❌ Ocurrió un error al intentar escribir en data/catalogo_seed.json.")
