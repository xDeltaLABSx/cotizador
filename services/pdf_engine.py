# services/pdf_engine.py
import io
import subprocess
import os
tempfile = __import__('tempfile')

def convertir_docx_a_pdf(docx_bytes):
    """
    Toma el archivo Word (.docx) perfectamente formateado con el membrete y 
    lo convierte a PDF manteniendo intactas las imágenes, márgenes y diseño.
    """
    # 1. Crear archivos temporales seguros en el servidor
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
        tmp_docx.write(docx_bytes)
        tmp_docx_path = tmp_docx.name
        
    tmp_pdf_path = tmp_docx_path.replace(".docx", ".pdf")
    
    try:
        # 2. Intentar conversión mediante LibreOffice (disponible en Linux/Streamlit Cloud)
        # Esto convierte el documento respetando 100% los gráficos, membretes y fuentes del Word base.
        proceso = subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(tmp_docx_path), tmp_docx_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30
        )
        
        if proceso.returncode == 0 and os.path.exists(tmp_pdf_path):
            with open(tmp_pdf_path, "rb") as f:
                pdf_bytes = f.read()
            return pdf_bytes
        else:
            raise Exception("No se pudo procesar la conversión gráfica mediante LibreOffice.")
            
    except Exception as e:
        # 3. Respaldo de emergencia por si el entorno limita herramientas de sistema
        # Devuelve un PDF informativo limpio para evitar que la app se detenga
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(190, 10, "DELTA LABS - Respaldo de PDF", 0, 1, "C")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(190, 6, f"\nEl documento Word (.docx) se generó con éxito.\nDetalle de conversión PDF en servidor: {str(e)}")
        return bytes(pdf.output())
        
    finally:
        # Limpieza de archivos temporales en el servidor
        if os.path.exists(tmp_docx_path):
            os.remove(tmp_docx_path)
        if os.path.exists(tmp_pdf_path):
            os.remove(tmp_pdf_path)
