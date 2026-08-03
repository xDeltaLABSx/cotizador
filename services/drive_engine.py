# services/drive_engine.py
import os
import io
import base64
import requests
import streamlit as st

def guardar_en_drive_y_excel(datos, doc_bytes, pdf_bytes, nombre_archivo, folder_id, sheet_id=None):
    try:
        if "APPS_SCRIPT_URL" not in st.secrets:
            return False, "⚠️ Falta configurar la URL del Webhook en los secretos."
            
        url_script = st.secrets["APPS_SCRIPT_URL"]
        
        # Convertir el archivo Word a Base64
        b64_file = base64.b64encode(doc_bytes).decode("utf-8")
        
        payload = {
            "filename": f"{nombre_archivo}.docx",
            "mimetype": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "file_base64": b64_file
        }
        
        # Enviar petición POST al Webhook
        response = requests.post(url_script, json=payload, timeout=30)
        
        # Verificar si Google devolvió HTML (error de permisos o ejecución) en lugar de JSON
        if "application/json" not in response.headers.get("Content-Type", ""):
            return False, f"⚠️ Error de Google Apps Script (HTML devuelto): {response.text[:200]}"
            
        resultado = response.json()
        
        if resultado.get("status") == "success":
            file_id = resultado.get("file_id")
            return True, f"✅ ¡Archivo subido correctamente a Google Drive (ID: {file_id})!"
        else:
            return False, f"⚠️ Error en Google Script: {resultado.get('message')}"
            
    except Exception as e:
        return False, f"⚠️ Error de conexión con Google Apps Script: {str(e)}"
