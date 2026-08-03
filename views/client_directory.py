# views/client_directory.py
import streamlit as st
import pandas as pd
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

    if "editando_id" not in st.session_state:
        st.session_state.editando_id = None

    # Si se seleccionó editar un cliente, mostramos un formulario limpio y compacto
    if st.session_state.editando_id:
        c_id = st.session_state.editando_id
        # Buscamos los datos actuales del cliente
        cliente_actual = next((c for c in clientes if c[0] == c_id), None)
        
        if cliente_actual:
            with st.form(key=f"form_edit_compact_{c_id}"):
                st.markdown(f"### ✏️ Editando Cliente: {cliente_actual[3]}")
                ec1, ec2 = st.columns(2)
                with ec1:
                    e_empresa = st.text_input("Empresa", value=cliente_actual[3])
                    e_contacto = st.text_input("Contacto", value=cliente_actual[1])
                    e_cargo = st.text_input("Cargo", value=cliente_actual[2])
                with ec2:
                    e_correo = st.text_input("Correo", value=cliente_actual[4] if cliente_actual[4] else "")
                    e_telefono = st.text_input("Teléfono", value=cliente_actual[5] if cliente_actual[5] else "")
                
                b1, b2 = st.columns(2)
                with b1:
                    if st.form_submit_button("💾 Guardar Cambios", type="primary", use_container_width=True):
                        actualizar_cliente(c_id, e_contacto, e_cargo, e_empresa, e_correo, e_telefono)
                        st.session_state.editando_id = None
                        st.toast("✅ ¡Cliente actualizado con éxito!")
                        st.rerun()
                with b2:
                    if st.form_submit_button("❌ Cancelar Edición", use_container_width=True):
                        st.session_state.editando_id = None
                        st.rerun()
            st.markdown("---")

    st.markdown("### 📋 Listado General")

    # Cabecera de la tabla compacta
    hc = st.columns([2.5, 2.0, 1.5, 1.2, 0.8, 0.8])
    hc[0].markdown("**Empresa / Contacto**")
    hc[1].markdown("**Cargo**")
    hc[2].markdown("**Contacto**")
    hc[3].markdown("**Última Vez**")
    hc[4].markdown("**Editar**")
    hc[5].markdown("**Borrar**")
    st.markdown("---")

    # Filas compactas estilo renglón de tabla
    for c in clientes:
        cliente_id, contacto, cargo, empresa, correo, telefono, ultimo_reg = c
        
        rc = st.columns([2.5, 2.0, 1.5, 1.2, 0.8, 0.8])
        rc[0].markdown(f"**{empresa}**<br><span style='color: gray; font-size: 0.85em;'>👤 {contacto}</span>", unsafe_allow_html=True)
        rc[1].markdown(f"<span style='font-size: 0.9em;'>{cargo if cargo else 'N/D'}</span>", unsafe_allow_html=True)
        rc[2].markdown(f"<span style='font-size: 0.85em;'>✉️ {correo if correo else 'N/D'}<br>📞 {telefono if telefono else 'N/D'}</span>", unsafe_allow_html=True)
        rc[3].caption(str(ultimo_reg)[:10]) # Muestra solo la fecha YYYY-MM-DD para ahorrar espacio
        
        with rc[4]:
            if st.button("✏️", key=f"edit_{cliente_id}", help="Editar cliente"):
                st.session_state.editando_id = cliente_id
                st.rerun()
                
        with rc[5]:
            if st.button("🗑️", key=f"del_{cliente_id}", help="Eliminar cliente"):
                eliminar_cliente(cliente_id)
                st.toast(f"🗑️ Cliente eliminado.")
                st.rerun()
                
        st.markdown("<hr style='margin: 4px 0px; opacity: 0.2;'>", unsafe_allow_html=True)
