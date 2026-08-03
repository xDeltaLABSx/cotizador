# services/drive_engine.py
import os
import io
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

def obtener_servicio_drive():
    try:
        if "gcp_service_account" in st.secrets:
            secretos = dict(st.secrets["gcp_service_account"])
            
            # Unir las líneas de la llave privada de forma nativa si vienen en lista
            if "private_key_lines" in secretos:
                secretos["private_key"] = "\n".join(secretos["private_key_lines"])
                del secretos["private_key_lines"]
            elif "private_key" in secretos:
                secretos["private_key"] = str(secretos["private_key"]).strip().replace("\\n", "\n")

            creds = service_account.Credentials.from_service_account_info(
                secretos, 
                scopes=["https://www.googleapis.com/auth/drive"]
            )
            return build("drive", "v3", credentials=creds)
    except Exception as e:
        st.error(f"DETALLE TÉCNICO DE GOOGLE: {str(e)}")
    return None

def guardar_en_drive_y_excel(datos, doc_bytes, pdf_bytes, nombre_archivo, folder_id, sheet_id=None):
    try:
        drive_service = obtener_servicio_drive()
        if not drive_service:
            return False, "⚠️ No se pudo autenticar con Google Cloud. Revisa tus secretos."

        fh_docx = io.BytesIO(doc_bytes)
        media_docx = MediaIoBaseUpload(fh_docx, mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document", resumable=True)
        
        file_metadata = {
            'name': f"{nombre_archivo}.docx",
            'parents': [folder_id]
        }
        
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media_docx,
            fields='id'
        ).execute()

        return True, f"✅ ¡Archivo subido correctamente a Google Drive (ID: {file.get('id')})!"
        
    except Exception as e:
        return False, f"⚠️ Error de sincronización con Google: {str(e)}"
