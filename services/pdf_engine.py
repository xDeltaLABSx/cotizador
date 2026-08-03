# services/pdf_engine.py
from fpdf import FPDF
import io
import os
from config.settings import COMPANY_INFO, obtener_fecha_formal

def _limpiar_texto(texto):
    """Sanitiza caracteres Unicode para la fuente Helvetica."""
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

class CotizacionNativaPDF(FPDF):
    def header(self):
        # Incrusta tu imagen gráfica de membrete directamente en el PDF (Ancho seguro de 190 mm)
        ruta_img = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "encabezado.png")
        if os.path.exists(ruta_img):
            try:
                # Dibuja la imagen corporativa respetando el margen izquierdo (10mm)
                self.image(ruta_img, x=10, y=8, w=190)
            except Exception:
                pass
        # Espacio de respiración obligatorio debajo del gráfico para que no se encime con la fecha
        self.ln(30)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(190, 8, _limpiar_texto(f"{COMPANY_INFO['NAME']} — Página {self.page_no()}/{{nb}}"), 0, 0, "C")

def convertir_docx_a_pdf(docx_bytes=None, datos=None):
    """Genera el PDF nativo con la imagen de membrete y ancho exacto de 180 mm contra desbordes."""
    if not datos:
        datos = {
            "ciudad": COMPANY_INFO["DEFAULT_CITY"],
            "fecha_dt": None,
            "cliente_atencion": "Ingeniero Responsable",
            "cliente_empresa": "Constructora",
            "nombre_proyecto": "Levantamiento Topográfico",
            "objetivo": "", "metodologia": "", "equipo": "",
            "conceptos_economicos": [], "entregables": [], "exclusiones": [],
            "clausulas": "", "saludo_final": ""
        }

    pdf = CotizacionNativaPDF(orientation='P', unit='mm', format='A4')
    pdf.alias_nb_pages()
    pdf.add_page()
    # Margen izquierdo y derecho de 15 mm para garantizar que ningún texto toque el borde
    pdf.set_margins(left=15, top=15, right=15)
    pdf.set_auto_page_break(auto=True, margin=18)
    
    # Ancho útil exacto de la hoja con márgenes de 15mm = 180 mm
    ANCHO_UTIL = 180 
    
    # 1. Fecha formal alineada a la derecha
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 30, 30)
    fecha_limpia = _limpiar_texto(obtener_fecha_formal(datos.get("ciudad"), datos.get("fecha_dt")))
    pdf.cell(ANCHO_UTIL, 6, fecha_limpia, 0, 1, "R")
    pdf.ln(2)
    
    # 2. Bloque de destinatario
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(24, 76, 120)
    bloque_cliente = (
        f"At'n: {datos.get('cliente_atencion', '')}\n"
        f"{datos.get('cliente_cargo', '')}\n"
        f"{datos.get('cliente_empresa', '')}\n"
        "Presente.\n\n"
        f"Ref: {datos.get('nombre_proyecto', '')}"
    )
    pdf.multi_cell(ANCHO_UTIL, 5, _limpiar_texto(bloque_cliente))
    pdf.ln(3)
    
    # Función auxiliar estricta a 180 mm
    def add_section(titulo, texto):
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(24, 76, 120)
        pdf.cell(ANCHO_UTIL, 7, _limpiar_texto(titulo), 0, 1, "L")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(ANCHO_UTIL, 5, _limpiar_texto(texto))
        pdf.ln(2)

    # 3. Secciones principales
    add_section("1. Objetivo del Proyecto", datos.get("objetivo", ""))
    add_section("2. Metodología y Procedimiento Técnico", datos.get("metodologia", ""))
    add_section("3. Instrumentación y Equipo Desplegado", datos.get("equipo", ""))
    
    # 4. Entregables
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(24, 76, 120)
    pdf.cell(ANCHO_UTIL, 7, "4. Entregables del Proyecto", 0, 1, "L")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 40, 40)
    for ent in datos.get("entregables", []):
        pdf.multi_cell(ANCHO_UTIL, 5, f"   - {_limpiar_texto(ent)}")
    pdf.ln(2)
    
    # 5. Propuesta Económica (Tabla exacta distribuida en 180 mm: 105 + 30 + 45)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(24, 76, 120)
    pdf.cell(ANCHO_UTIL, 7, "5. Propuesta Económica", 0, 1, "L")
    
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(24, 76, 120)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(105, 7, _limpiar_texto("Descripción del Servicio / Concepto"), 1, 0, "C", fill=True)
    pdf.cell(30, 7, "Cant.", 1, 0, "C", fill=True)
    pdf.cell(45, 7, "Importe (MXN)", 1, 1, "C", fill=True)
    
    total_mxn = 0.0
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(40, 40, 40)
    for cons in datos.get("conceptos_economicos", []):
        monto = float(cons.get("monto", 0.0))
        total_mxn += monto
        pdf.cell(105, 6, _limpiar_texto(cons.get("desc", ""))[:55], 1, 0, "L")
        pdf.cell(30, 6, _limpiar_texto(cons.get("cant", "")), 1, 0, "C")
        pdf.cell(45, 6, f"$ {monto:,.2f}", 1, 1, "R")
        
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(24, 76, 120)
    pdf.cell(135, 7, "TOTAL (Sin I.V.A.):", 1, 0, "R")
    pdf.cell(45, 7, f"$ {total_mxn:,.2f}", 1, 1, "R")
    pdf.ln(3)
    
    # 6. Premisas y Exclusiones
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(24, 76, 120)
    pdf.cell(ANCHO_UTIL, 7, "6. Premisas Técnicas y Exclusiones", 0, 1, "L")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    for excl in datos.get("exclusiones", []):
        pdf.multi_cell(ANCHO_UTIL, 5, f"   - {_limpiar_texto(excl)}")
    pdf.ln(2)
    
    # 7. Condiciones y Saludo
    add_section("7. Condiciones de Trabajo y Forma de Pago", datos.get("clausulas", ""))
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(ANCHO_UTIL, 5, _limpiar_texto(datos.get("saludo_final", "")))
    pdf.ln(4)
    
    # 8. Firma y Datos Bancarios
    pdf.multi_cell(ANCHO_UTIL, 5, "Atentamente,\n\n")
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(24, 76, 120)
    pdf.cell(ANCHO_UTIL, 5, _limpiar_texto(COMPANY_INFO["LEGAL_REP"]), 0, 1, "L")
    
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(ANCHO_UTIL, 4, _limpiar_texto(COMPANY_INFO["ROLE"]), 0, 1, "L")
    pdf.cell(ANCHO_UTIL, 4, _limpiar_texto(COMPANY_INFO["NAME"]), 0, 1, "L")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(100, 110, 120)
    cuenta_txt = f"Datos Bancarios para Anticipo: CLABE {COMPANY_INFO['CLABE_ENDING']} ({COMPANY_INFO['BANK_NAME']})"
    pdf.cell(ANCHO_UTIL, 4, _limpiar_texto(cuenta_txt), 0, 1, "L")
    
    return bytes(pdf.output())
