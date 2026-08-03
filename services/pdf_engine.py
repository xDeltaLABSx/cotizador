# services/pdf_engine.py
from fpdf import FPDF
import io
from config.settings import COMPANY_INFO, obtener_fecha_formal

def _limpiar_texto(texto):
    """Sanitiza caracteres Unicode para evitar conflictos con la fuente Helvetica."""
    if not texto:
        return ""
    reemplazos = {
        "•": "-", "\u2022": "-", "–": "-", "—": "-", 
        "“": '"', "”": '"', "‘": "'", "’": "'", "…": "..."
    }
    texto_str = str(texto)
    for orig, dest in reemplazos.items():
        texto_str = texto_str.replace(orig, dest)
    return texto_str.encode("latin-1", "replace").decode("latin-1")

class CotizacionPDF(FPDF):
    def header(self):
        # Ancho fijo de 190 mm (A4 de 210 menos 10mm de cada margen)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(24, 76, 120)  # Azul Institucional
        self.cell(190, 7, _limpiar_texto(COMPANY_INFO["NAME"]), 0, 1, "R")
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(100, 110, 120)
        self.cell(190, 5, _limpiar_texto(COMPANY_INFO["SUBTITLE"]), 0, 1, "R")
        self.ln(8)  # Espacio de respiración bajo el encabezado

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(190, 10, f"DELTA LABS - Página {self.page_no()}/{{nb}}", 0, 0, "C")

def generar_cotizacion_pdf(datos):
    """Genera el archivo PDF ejecutivo con anchos fijos para evitar errores de espacio horizontal."""
    pdf = CotizacionPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=18)
    
    # 1. FECHA FORMAL (Ancho fijo de 190 mm)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 30, 30)
    fecha_limpia = _limpiar_texto(obtener_fecha_formal(datos.get("ciudad"), datos.get("fecha_dt")))
    pdf.cell(190, 6, fecha_limpia, 0, 1, "R")
    pdf.ln(3)
    
    # 2. DESTINATARIO
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(24, 76, 120)
    bloque_cliente = (
        f"At'n: {datos.get('cliente_atencion', '')}\n"
        f"{datos.get('cliente_cargo', '')}\n"
        f"{datos.get('cliente_empresa', '')}\n"
        "Presente.\n\n"
        f"Ref: {datos.get('nombre_proyecto', '')}"
    )
    pdf.multi_cell(190, 5, _limpiar_texto(bloque_cliente))
    pdf.ln(4)
    
    # FUNCIÓN INTERNA PARA SECCIONES CON ANCHO FIJO DE 190 mm
    def add_section(titulo, texto):
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(24, 76, 120)
        pdf.cell(190, 7, _limpiar_texto(titulo), 0, 1, "L")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(190, 5, _limpiar_texto(texto))
        pdf.ln(3)

    # 3. OBJETIVO, METODOLOGÍA Y EQUIPO
    add_section("1. Objetivo del Proyecto", datos.get("objetivo", ""))
    add_section("2. Metodología y Procedimiento Técnico", datos.get("metodologia", ""))
    add_section("3. Instrumentación y Equipo Desplegado", datos.get("equipo", ""))
    
    # 4. ENTREGABLES
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(24, 76, 120)
    pdf.cell(190, 7, "4. Entregables del Proyecto", 0, 1, "L")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 40, 40)
    for ent in datos.get("entregables", []):
        texto_entregable = f"   - {_limpiar_texto(ent)}"
        pdf.multi_cell(190, 5, texto_entregable)
    pdf.ln(3)
    
    # 5. PROPUESTA ECONÓMICA (TABLA EXACTA DE 190 mm: 110 + 35 + 45)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(24, 76, 120)
    pdf.cell(190, 7, "5. Propuesta Económica", 0, 1, "L")
    
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(24, 76, 120)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(110, 7, _limpiar_texto("Descripción del Servicio / Concepto"), 1, 0, "C", fill=True)
    pdf.cell(35, 7, "Cant.", 1, 0, "C", fill=True)
    pdf.cell(45, 7, "Importe (MXN)", 1, 1, "C", fill=True)
    
    total_mxn = 0.0
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(40, 40, 40)
    for cons in datos.get("conceptos_economicos", []):
        monto = float(cons.get("monto", 0.0))
        total_mxn += monto
        pdf.cell(110, 6, _limpiar_texto(cons.get("desc", ""))[:58], 1, 0, "L")
        pdf.cell(35, 6, _limpiar_texto(cons.get("cant", "")), 1, 0, "C")
        pdf.cell(45, 6, f"$ {monto:,.2f}", 1, 1, "R")
        
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(24, 76, 120)
    pdf.cell(145, 7, "TOTAL (Sin I.V.A.):", 1, 0, "R")
    pdf.cell(45, 7, f"$ {total_mxn:,.2f}", 1, 1, "R")
    pdf.ln(4)
    
    # 6. PREMISAS Y EXCLUSIONES
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(24, 76, 120)
    pdf.cell(190, 7, "6. Premisas Técnicas y Exclusiones", 0, 1, "L")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    for excl in datos.get("exclusiones", []):
        texto_exclusion = f"   - {_limpiar_texto(excl)}"
        pdf.multi_cell(190, 5, texto_exclusion)
    pdf.ln(3)
    
    # 7. CONDICIONES DE TRABAJO Y SALUDO FINAL
    add_section("7. Condiciones de Trabajo y Forma de Pago", datos.get("clausulas", ""))
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(190, 5, _limpiar_texto(datos.get("saludo_final", "")))
    pdf.ln(5)
    
    # 8. FIRMA Y DATOS BANCARIOS (Celdas aseguradas a 190 mm)
    pdf.multi_cell(190, 5, "Atentamente,\n\n")
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(24, 76, 120)
    pdf.cell(190, 5, _limpiar_texto(COMPANY_INFO["LEGAL_REP"]), 0, 1, "L")
    
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(190, 4, _limpiar_texto(COMPANY_INFO["ROLE"]), 0, 1, "L")
    pdf.cell(190, 4, _limpiar_texto(COMPANY_INFO["NAME"]), 0, 1, "L")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(100, 110, 120)
    cuenta_txt = f"Datos Bancarios para Anticipo: CLABE {COMPANY_INFO['CLABE_ENDING']} ({COMPANY_INFO['BANK_NAME']})"
    pdf.cell(190, 4, _limpiar_texto(cuenta_txt), 0, 1, "L")
    
    return bytes(pdf.output())
