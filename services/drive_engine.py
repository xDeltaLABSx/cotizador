# services/drive_engine.py
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
from datetime import datetime

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]

def conectar_google():
    """Conecta de forma segura usando st.secrets en Streamlit Cloud."""
    if "gcp_service_account" not in st.secrets:
        return None, None
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=SCOPES
    )
    return gspread.authorize(creds), build('drive', 'v3', credentials=creds)

def guardar_en_drive_y_excel(datos, word_bytes, pdf_bytes, nombre_base, drive_folder_id, sheet_id):
    """
    Subirá el .docx y .pdf a tu carpeta de Google Drive y añadirá un renglón a tu Excel/Google Sheet.
    """
    try:
        gclient, drive_service = conectar_google()
        if not gclient:
            return False, "⚠️ Falta configurar st.secrets['gcp_service_account'] en Streamlit Cloud."
            
        # 1. Subir Word (.docx) a la carpeta de Google Drive
        meta_docx = {'name': f"{nombre_base}.docx", 'parents': [drive_folder_id]}
        media_docx = MediaIoBaseUpload(io.BytesIO(word_bytes), mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        drive_service.files().create(body=meta_docx, media_body=media_docx).execute()
        
        # 2. Subir PDF (.pdf) a la carpeta de Google Drive
        meta_pdf = {'name': f"{nombre_base}.pdf", 'parents': [drive_folder_id]}
        media_pdf = MediaIoBaseUpload(io.BytesIO(pdf_bytes), mimetype='application/pdf')
        drive_service.files().create(body=meta_pdf, media_body=media_pdf).execute()
        
        # 3. Registrar fila en el Excel (Google Sheet)
        hoja = gclient.open_by_key(sheet_id).sheet1
        fila = [
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            datos.get("cliente_empresa", ""),
            datos.get("cliente_atencion", ""),
            datos.get("nombre_proyecto", ""),
            datos.get("titulo_meta", ""),
            f"$ {sum(float(c['monto']) for c in datos.get('conceptos_economicos', [])):,.2f}"
        ]
        hoja.append_row(fila)
        return True, "✅ ¡Word y PDF guardados en Drive, y Excel actualizado con éxito!"
        
    except Exception as e:
        return False, f"⚠️ Error de sincronización con Google: {str(e)}"
