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
            
            if "private_key" in secretos:
                pk = secretos["private_key"].strip()
                # Si la llave viene comprimida en una sola línea sin saltos reales, la reparamos por código
                if "----BEGIN PRIVATE KEY----" in pk and "\n" not in pk.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", ""):
                    # Limpiamos encabezados y pies para dejar solo el cuerpo base64
                    cuerpo = pk.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "").strip()
                    # Reconstruimos la llave con saltos de línea exactos cada 64 caracteres (estándar PEM)
                    lineas_cuerpo = [cuerpo[i:i+64] for i in range(0, len(cuerpo), 64)]
                    pk = "-----BEGIN PRIVATE KEY-----\n" + "\n".join(lineas_cuerpo) + "\n-----END PRIVATE KEY-----"
                
                secretos["private_key"] = pk

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
