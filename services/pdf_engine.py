# services/pdf_engine.py
from fpdf import FPDF
import io
from config.settings import COMPANY_INFO, COLORS, obtener_fecha_formal

class CotizacionPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(24, 76, 120)  # Azul Institucional
        self.cell(0, 8, COMPANY_INFO["NAME"], 0, 1, "R")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(100, 110, 120)
        self.cell(0, 5, COMPANY_INFO["SUBTITLE"], 0, 1, "R")
        self.ln(12)  # Espacio de respiración bajo el encabezado

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"{COMPANY_INFO['NAME']} - Página {self.page_no()}/{{nb}}", 0, 0, "C")

def generar_cotizacion_pdf(datos):
    """Genera un archivo PDF limpio y ejecutivo en bytes puros."""
    pdf = CotizacionPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # Fecha formal
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 6, obtener_fecha_formal(datos.get("ciudad"), datos.get("fecha_dt")), 0, 1, "R")
    pdf.ln(4)
    
    # Bloque de cliente
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(24, 76, 120)
    pdf.multi_cell(0, 5, f"At'n: {datos.get('cliente_atencion', '')}\n{datos.get('cliente_cargo', '')}\n{datos.get('cliente_empresa', '')}\nPresente.\n\nRef: {datos.get('nombre_proyecto', '')}")
    pdf.ln(4)
    
    # Secciones técnicas
    def add_section(titulo, texto):
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(24, 76, 120)
        pdf.cell(0, 7, titulo, 0, 1, "L")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(0, 5, texto)
        pdf.ln(3)

    add_section("1. Objetivo del Proyecto", datos.get("objetivo", ""))
    add_section("2. Metodología y Procedimiento Técnico", datos.get("metodologia", ""))
    add_section("3. Instrumentación y Equipo Desplegado", datos.get("equipo", ""))
    
    # Entregables
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(24, 76, 120)
    pdf.cell(0, 7, "4. Entregables del Proyecto", 0, 1, "L")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 40, 40)
    for ent in datos.get("entregables", []):
        pdf.cell(5, 5, "-", 0, 0)
        pdf.multi_cell(0, 5, ent)
    pdf.ln(3)
    
    # Propuesta Económica
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(24, 76, 120)
    pdf.cell(0, 7, "5. Propuesta Económica", 0, 1, "L")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(24, 76, 120)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(110, 7, "Descripción del Servicio", 1, 0, "C", fill=True)
    pdf.cell(30, 7, "Cant.", 1, 0, "C", fill=True)
    pdf.cell(45, 7, "Importe (MXN)", 1, 1, "C", fill=True)
    
    total_mxn = 0.0
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(40, 40, 40)
    for idx, cons in enumerate(datos.get("conceptos_economicos", [])):
        monto = float(cons.get("monto", 0.0))
        total_mxn += monto
        pdf.cell(110, 6, str(cons.get("desc", ""))[:55], 1, 0, "L")
        pdf.cell(30, 6, str(cons.get("cant", "")), 1, 0, "C")
        pdf.cell(45, 6, f"$ {monto:,.2f}", 1, 1, "R")
        
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(24, 76, 120)
    pdf.cell(140, 7, "TOTAL (Sin I.V.A.):", 1, 0, "R")
    pdf.cell(45, 7, f"$ {total_mxn:,.2f}", 1, 1, "R")
    pdf.ln(5)
    
    # Firma y Cuenta bancaria
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(0, 5, f"Atentamente,\n\n\n{COMPANY_INFO['LEGAL_REP']}\n{COMPANY_INFO['ROLE']}\n{COMPANY_INFO['NAME']}\n\nCLABE para Anticipos: {COMPANY_INFO['CLABE_ENDING']} ({COMPANY_INFO['BANK_NAME']})")
    
    return bytes(pdf.output())
