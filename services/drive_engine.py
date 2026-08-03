# services/drive_engine.py
import os
import io
import re
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

def sanitizar_llave_pem(pk_raw: str) -> str:
    """ Sanea y reconstruye una llave privada PEM garantizando formato OpenSSL / RFC 7468 estricto. """
    if not pk_raw:
        return ""
    
    # 1. Limpiar retornos de carro de Windows y saltos escapados
    texto = str(pk_raw).replace("\r", "").replace("\\n", "\n")
    
    # 2. Filtrar encabezados, pies y líneas vacías para aislar el cuerpo Base64
    lineas = texto.split("\n")
    lineas_cuerpo = [l.strip() for l in lineas if l.strip() and not l.strip().startswith("-----")]
    cuerpo_b64 = "".join(lineas_cuerpo)
    
    # 3. Eliminar cualquier carácter que no sea Base64 válido
    cuerpo_b64 = re.sub(r'[^A-Za-z0-9+/=]', '', cuerpo_b64)
    
    # 4. Corregir y ajustar el padding de Base64 (múltiplo de 4)
    mod = len(cuerpo_b64) % 4
    if mod != 0:
        cuerpo_b64 += "=" * (4 - mod)
        
    # 5. Dividir el cuerpo en bloques exactos de 64 caracteres (estándar PEM/OpenSSL)
    bloques_64 = [cuerpo_b64[i:i+64] for i in range(0, len(cuerpo_b64), 64)]
    
    # 6. Reconstruir la estructura PEM limpia
    pem_final = "-----BEGIN PRIVATE KEY-----\n" + "\n".join(bloques_64) + "\n-----END PRIVATE KEY-----\n"
    return pem_final

def obtener_servicio_drive():
    try:
        if "gcp_service_account" in st.secrets:
            secretos = dict(st.secrets["gcp_service_account"])
            
            # Sanitización de la llave privada
            if "private_key" in secretos:
                secretos["private_key"] = sanitizar_llave_pem(secretos["private_key"])

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
