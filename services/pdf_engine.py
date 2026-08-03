# services/pdf_engine.py
import io
import os
import tempfile
import subprocess
import docx
from fpdf import FPDF
from config.settings import COMPANY_INFO

def convertir_docx_a_pdf(docx_bytes=None, datos=None):
    """
    Convierte el archivo Word (.docx) real a PDF utilizando LibreOffice en segundo plano
    para garantizar que el diseño, los logotipos y las tablas salgan idénticos.
    Si el entorno no soporta el motor de sistema, utiliza un espejo estructurado limpio.
    """
    if not docx_bytes:
        from services.doc_engine import generar_cotizacion_docx
        if datos:
            docx_bytes = generar_cotizacion_docx(datos)
        else:
            return b""

    # 1. Crear archivo temporal para el Word
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
        tmp_docx.write(docx_bytes)
        tmp_docx_path = tmp_docx.name

    tmp_pdf_path = tmp_docx_path.replace(".docx", ".pdf")

    try:
        # 2. Intentar conversión de alta fidelidad con LibreOffice del servidor
        proceso = subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(tmp_docx_path), tmp_docx_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=25
        )
        
        if proceso.returncode == 0 and os.path.exists(tmp_pdf_path):
            with open(tmp_pdf_path, "rb") as f:
                pdf_bytes = f.read()
            return pdf_bytes
        else:
            raise Exception("Motor gráfico no disponible.")

    except Exception:
        # 3. CONVERSOR ESPEJO DE RESPALDO (Lee el docx recién creado párrafo por párrafo)
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Leer el contenido exacto del docx generado
        doc_leido = docx.Document(io.BytesIO(docx_bytes))
        
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(40, 40, 40)
        
        for p in doc_leido.paragraphs:
            if p.text.strip():
                texto_limpio = p.text.encode("latin-1", "replace").decode("latin-1")
                is_title = p.text.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "At'n", "Ref:", "Fecha:"))
                
                if is_title:
                    pdf.set_font("Helvetica", "B", 10.5)
                    pdf.set_text_color(24, 76, 120)
                else:
                    pdf.set_font("Helvetica", "", 10)
                    pdf.set_text_color(40, 40, 40)
                    
                pdf.multi_cell(180, 5, texto_limpio)
                pdf.ln(1)
                
        return bytes(pdf.output())

    finally:
        if os.path.exists(tmp_docx_path):
            os.remove(tmp_docx_path)
        if os.path.exists(tmp_pdf_path):
            os.remove(tmp_pdf_path)
