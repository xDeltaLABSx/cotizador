# models/client_model.py
import streamlit as st
from datetime import datetime

try:
    from services.drive_engine import get_gspread_client
except ImportError:
    get_gspread_client = None

SHEET_ID_CONFIG = "1UjSc9_tCWfw5dsn4Vu_0R5UTTlrnRNUZHDDiUqoMhv4"

def _obtener_hoja_clientes():
    """Conecta con la primera pestaña activa de tu Google Sheet maestro."""
    if not get_gspread_client:
        st.error("⚠️ No se pudo importar 'get_gspread_client' desde services.drive_engine")
        return None
    try:
        gc = get_gspread_client()
        doc = gc.open_by_key(SHEET_ID_CONFIG)
        
        # Seleccionamos siempre la primera hoja (índice 0)
        worksheet = doc.get_worksheet(0)
        
        # Validamos si la hoja está completamente vacía para poner los encabezados
        try:
            vals = worksheet.get_all_values()
            if not vals or len(vals) == 0:
                worksheet.append_row(["Contacto", "Cargo", "Empresa", "Correo", "Teléfono", "Último Registro"])
        except Exception:
            worksheet.append_row(["Contacto", "Cargo", "Empresa", "Correo", "Teléfono", "Último Registro"])
            
        return worksheet
    except Exception as e:
        st.error(f"⚠️ Error de permisos o conexión con Google Sheets: {e}")
        return None

def init_client_db():
    pass

def guardar_o_actualizar_cliente(nombre_atencion, cargo, empresa, correo="", telefono=""):
    """Guarda o actualiza un cliente directamente en Google Sheets."""
    try:
        worksheet = _obtener_hoja_clientes()
        if not worksheet:
            return False

        registros = worksheet.get_all_records()
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        encontrado = False
        fila_indice = None
        
        for idx, row in enumerate(registros, start=2):
            row_empresa = str(row.get("Empresa", "")).strip().lower()
            row_contacto = str(row.get("Contacto", "")).strip().lower()
            
            if row_empresa == str(empresa).strip().lower() and row_contacto == str(nombre_atencion).strip().lower():
                encontrado = True
                fila_indice = idx
                break
        
        if encontrado and fila_indice:
            worksheet.update_cell(fila_indice, 2, cargo)
            worksheet.update_cell(fila_indice, 4, correo)
            worksheet.update_cell(fila_indice, 5, telefono)
            worksheet.update_cell(fila_indice, 6, fecha_actual)
        else:
            worksheet.append_row([
                str(nombre_atencion),
                str(cargo),
                str(empresa),
                str(correo),
                str(telefono),
                fecha_actual
            ])
        return True
    except Exception as e:
        print(f"Error al guardar cliente: {e}")
        return False

def buscar_clientes(termino=""):
    """Busca clientes en Google Sheets y muestra avisos si hay problemas."""
    try:
        worksheet = _obtener_hoja_clientes()
        if not worksheet:
            return []

        registros = worksheet.get_all_records()
        termino_lower = str(termino).strip().lower()
        
        resultados = []
        for row in registros:
            contacto = str(row.get("Contacto", ""))
            cargo = str(row.get("Cargo", ""))
            empresa = str(row.get("Empresa", ""))
            correo = str(row.get("Correo", ""))
            telefono = str(row.get("Teléfono", ""))
            
            if not termino_lower or termino_lower in empresa.lower() or termino_lower in contacto.lower():
                resultados.append((contacto, cargo, empresa, correo, telefono))
                
        return resultados[:10]
    except Exception as e:
        print(f"Error buscando clientes: {e}")
        return []
