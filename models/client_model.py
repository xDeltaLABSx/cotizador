# models/client_model.py
import streamlit as st
import os
from datetime import datetime

# Nota: Importamos el motor de Google Drive/Sheets que ya utilizas en tu app
try:
    from services.drive_engine import get_gspread_client
except ImportError:
    get_gspread_client = None

SHEET_ID_CONFIG = "1UjSc9_tCWfw5dsn4Vu_0R5UTTlrnRNUZHDDiUqoMhv4"  # Tu ID de Google Sheets maestro

def _obtener_hoja_clientes():
    """Conecta directamente con la primera pestaña activa de tu Google Sheet maestro."""
    if not get_gspread_client:
        return None
    try:
        gc = get_gspread_client()
        doc = gc.open_by_key(SHEET_ID_CONFIG)
        
        # Selecciona siempre la primera pestaña del documento (índice 0)
        worksheet = doc.get_worksheet(0)
        
        # Verificamos si la primera fila está vacía para poner los encabezados automáticamente
        vals = worksheet.get_all_values()
        if not vals or len(vals[0]) == 0:
            worksheet.append_row(["Contacto", "Cargo", "Empresa", "Correo", "Teléfono", "Último Registro"])
            
        return worksheet
    except Exception as e:
        print(f"Error conectando a la hoja en Google Sheets: {e}")
        return None

def init_client_db():
    """Función de compatibilidad para inicializar la estructura si es necesario."""
    pass

def guardar_o_actualizar_cliente(nombre_atencion, cargo, empresa, correo="", telefono=""):
    """
    Guarda un nuevo cliente o actualiza su última fecha de interacción directamente en Google Sheets.
    """
    try:
        worksheet = _obtener_hoja_clientes()
        if not worksheet:
            return None

        registros = worksheet.get_all_records()
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        encontrado = False
        fila_indice = None
        
        # Buscamos si ya existe la combinación empresa + contacto en el Excel
        for idx, row in enumerate(registros, start=2): # start=2 porque la fila 1 son headers
            row_empresa = str(row.get("Empresa", "")).strip().lower()
            row_contacto = str(row.get("Contacto", "")).strip().lower()
            
            if row_empresa == str(empresa).strip().lower() and row_contacto == str(nombre_atencion).strip().lower():
                encontrado = True
                fila_indice = idx
                break
        
        if encontrado and fila_indice:
            # Actualizamos los datos existentes en la fila correspondiente
            worksheet.update_cell(fila_indice, 2, cargo)       # Columna Cargo
            worksheet.update_cell(fila_indice, 4, correo)      # Columna Correo
            worksheet.update_cell(fila_indice, 5, telefono)    # Columna Teléfono
            worksheet.update_cell(fila_indice, 6, fecha_actual) # Columna Último Registro
        else:
            # Agregamos un nuevo registro al final de la hoja de Google Sheets
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
        print(f"Error al guardar cliente en Google Sheets: {e}")
        return False

def buscar_clientes(termino=""):
    """
    Búsqueda inteligente directamente en tu Google Sheet maestro en la nube.
    """
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
            ultimo_reg = str(row.get("Último Registro", ""))
            
            # Filtramos si coincide con la empresa o el nombre de atención
            if termino_lower in empresa.lower() or termino_lower in contacto.lower():
                # Formato esperado por la app: (nombre_atencion, cargo_departamento, empresa, correo, telefono)
                resultados.append((contacto, cargo, empresa, correo, telefono))
                
        # Ordenamos de manera simulada por fecha más reciente y limitamos a 10
        resultados = resultados[:10]
        return resultados
    except Exception as e:
        print(f"Error buscando clientes en Google Sheets: {e}")
        return []
