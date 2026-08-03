# views/client_directory.py
import streamlit as st
from models.client_model import obtener_todos_los_clientes, eliminar_cliente

def render_client_directory():
    st.subheader("📂 Cartera de Clientes Registrados")
    st.caption("Administra tu base de datos local de constructoras y contactos guardados automáticamente.")
    
    # Obtenemos todos los clientes de SQLite
    clientes = obtener_todos_los_clientes()
    
    if not clientes:
        st.info("Aún no hay clientes registrados. Se agregarán automáticamente al generar tu primera cotización en la pestaña 1.")
        return

    st.markdown("### Listado de Clientes y Contactos")
    
    # Mostramos cada cliente con su botón individual para eliminar
    for c in clientes:
        cliente_id, contacto, cargo, empresa, correo, telefono, ultimo_reg = c
        
        with st.container():
            col1, col2, col3 = st.columns([3, 3, 1])
            with col1:
                st.markdown(f"**🏢 Empresa:** {empresa}")
                st.markdown(f"👤 **Contacto:** {contacto} ({cargo})")
            with col2:
                st.markdown(f"📧 **Correo:** {correo if correo else 'N/D'}")
                st.markdown(f"📞 **Teléfono:** {telefono if telefono else 'N/D'}")
                st.caption(f"Última interacción: {ultimo_reg}")
            with col3:
                # Botón de eliminación con clave única
                if st.button("🗑️ Borrar", key=f"del_client_{cliente_id}", type="secondary"):
                    eliminar_cliente(cliente_id)
                    st.toast(f"🗑️ Cliente {empresa} eliminado con éxito.")
                    st.rerun()
            st.divider()
