# models/client_model.py
import streamlit as st
import requests
from datetime import datetime

SHEET_ID_CONFIG = "1UjSc9_tCWfw5dsn4Vu_0R5UTTlrnRNUZHDDiUqoMhv4"

def init_client_db():
    """Función de compatibilidad."""
    pass

def guardar_o_actualizar_cliente(nombre_atencion, cargo, empresa, correo="", telefono=""):
    """
    Envía los datos del cliente al Apps Script para que los registre en el Google Sheet maestro.
    """
    try:
        if "APPS_SCRIPT_URL" not in st.secrets:
            return False
            
        url_script = st.secrets["APPS_SCRIPT_URL"]
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Estructura de datos para que el Webhook identifique que es un registro de cliente
        payload = {
            "action": "guardar_cliente",
            "contacto": str(nombre_atencion),
            "cargo": str(cargo),
            "empresa": str(empresa),
            "correo": str(correo),
            "telefono": str(telefono),
            "ultimo_registro": fecha_actual
        }
        
        response = requests.post(url_script, json=payload, timeout=15)
        return True
    except Exception as e:
        print(f"Error al enviar cliente al script: {e}")
        return False

def buscar_clientes(termino=""):
    """
    Consulta la lista de clientes. (Nota: Como el almacenamiento principal es web, 
    retorna una lista local en sesión o vacía hasta que se sincronicen desde el script).
    """
    try:
        # Si tienes una caché en session_state para agilizar la búsqueda localmente:
        if "clientes_cache" not in st.session_state:
            st.session_state.clientes_cache = []
            
        termino_lower = str(termino).strip().lower()
        if not termino_lower:
            return st.session_state.clientes_cache[:10]
            
        resultados = []
        for cliente in st.session_state.clientes_cache:
            contacto, cargo, empresa, correo, telefono = cliente
            if termino_lower in empresa.lower() or termino_lower in contacto.lower():
                resultados.append(cliente)
                
        return resultados[:10]
    except Exception as e:
        print(f"Error buscando clientes: {e}")
        return []
