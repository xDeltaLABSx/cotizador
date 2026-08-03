# services/drive_engine.py
import os
import io
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

def obtener_servicio_drive():
    try:
        if "project_id" in st.secrets and "private_key" in st.secrets:
            # Armamos el diccionario de credenciales de forma plana y segura
            secretos = {
                "type": "service_account",
                "project_id": st.secrets["project_id"],
                "private_key_id": st.secrets.get("private_key_id", "3125ad883efba098b2131112153b3fddd311df47"),
                "private_key": str(st.secrets["private_key"]).replace("\\n", "\n"),
                "client_email": st.secrets["client_email"],
                "client_id": "114549220877666542984",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bot-delta%40delta-labs-auth.iam.gserviceaccount.com",
                "universe_domain": "googleapis.com"
            }

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
