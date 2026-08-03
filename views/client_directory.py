# views/client_directory.py
import streamlit as st
import sqlite3
import os

DB_PATH = os.path.join("data", "cotizaciones_delta.db")

def obtener_todos_los_clientes():
    """Retorna todos los clientes registrados."""
    if not os.path.exists(DB_PATH):
        return []
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre_atencion, cargo_departamento, empresa, correo, telefono, ultimo_registro FROM clientes ORDER BY ultimo_registro DESC')
    res = cursor.fetchall()
    conn.close()
    return res

def actualizar_cliente(cliente_id, contacto, cargo, empresa, correo, telefono):
    """Actualiza los datos de un cliente existente."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clientes 
        SET nombre_atencion = ?, cargo_departamento = ?, empresa = ?, correo = ?, telefono = ?
        WHERE id = ?
    ''', (contacto, cargo, empresa, correo, telefono, cliente_id))
    conn.commit()
    conn.close()

def eliminar_cliente(cliente_id):
    """Elimina un cliente."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
    conn.commit()
    conn.close()

def render_client_directory():
    st.subheader("📂 Cartera de Clientes Registrados")
    st.caption("Administra, edita o elimina las constructoras y contactos de tu base de datos local.")
    
    clientes = obtener_todos_los_clientes()
    
    if not clientes:
        st.info("Aún no hay clientes registrados. Se agregarán automáticamente al generar tu primera cotización.")
        return

    # Control de edición en sesión
    if "editando_id" not in st.session_state:
        st.session_state.editando_id = None

    st.markdown("### Listado General de Clientes")

    # Encabezados de la tabla personalizada
    header_cols = st.columns([2.2, 1.8, 1.5, 1.2, 1.2, 1.3])
    header_cols[0].markdown("**Empresa**")
    header_cols[1].markdown("**Contacto (Cargo)**")
    header_cols[2].markdown("**Correo / Tel.**")
    header_cols[3].markdown("**Última Interacción**")
    header_cols[4].markdown("**Editar**")
    header_cols[5].markdown("**Borrar**")
    st.markdown("---")

    for c in clientes:
        cliente_id, contacto, cargo, empresa, correo, telefono, ultimo_reg = c
        
        # Si este cliente está en modo edición, mostramos el formulario de edición en lugar de la fila normal
        if st.session_state.editando_id == cliente_id:
            with st.form(key=f"form_edit_{cliente_id}"):
                st.markdown(f"#### ✏️ Editando Cliente ID: {cliente_id}")
                e_empresa = st.text_input("Empresa", value=empresa)
                e_contacto = st.text_input("Contacto", value=contacto)
                e_cargo = st.text_input("Cargo", value=cargo)
                e_correo = st.text_input("Correo", value=correo if correo else "")
                e_telefono = st.text_input("Teléfono", value=telefono if telefono else "")
                
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.form_submit_button("💾 Guardar Cambios", type="primary", use_container_width=True):
                        actualizar_cliente(cliente_id, e_contacto, e_cargo, e_empresa, e_correo, e_telefono)
                        st.session_state.editando_id = None
                        st.toast("✅ ¡Cliente actualizado con éxito!")
                        st.rerun()
                with col_cancel:
                    if st.form_submit_button("❌ Cancelar", use_container_width=True):
                        st.session_state.editando_id = None
                        st.rerun()
            st.markdown("---")
            continue

        # Fila normal con datos y botones
        row_cols = st.columns([2.2, 1.8, 1.5, 1.2, 1.2, 1.3])
        row_cols[0].write(empresa)
        row_cols[1].write(f"{contacto}\n\n*({cargo})*")
        row_cols[2].write(f"✉️ {correo if correo else 'N/D'}\n📞 {telefono if telefono else 'N/D'}")
        row_cols[3].caption(ultimo_reg)
        
        with row_cols[4]:
            if st.button("✏️ Editar", key=f"btn_edit_{cliente_id}", use_container_width=True):
                st.session_state.editando_id = cliente_id
                st.rerun()
                
        with row_cols[5]:
            if st.button("🗑️ Borrar", key=f"btn_del_{cliente_id}", type="secondary", use_container_width=True):
                eliminar_cliente(cliente_id)
                st.toast(f"🗑️ Cliente {empresa} eliminado.")
                st.rerun()
                
        st.markdown("---")
