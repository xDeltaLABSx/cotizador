# services/doc_engine.py
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import io
from config.settings import COMPANY_INFO, COLORS, DOC_CONFIG, obtener_fecha_formal

def _hex_a_rgb(hex_str):
    """Convierte color hexadecimal en objeto RGBColor para python-docx."""
    return RGBColor(int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))

def _set_cell_background(cell, fill_hex):
    """Aplica color de fondo hexadecimal a una celda de tabla."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def _aplicar_estilo_parrafo(p, size_pt=DOC_CONFIG["BODY_SIZE_PT"], bold=False, color_hex=COLORS["TEXT_HEX"], keep_next=False):
    """Aplica formato tipográfico coherente y protección contra saltos de hoja."""
    p.paragraph_format.keep_with_next = keep_next
    for run in p.runs:
        run.font.name = DOC_CONFIG["FONT_NAME"]
        run.font.size = Pt(size_pt)
        run.font.bold = bold
        run.font.color.rgb = _hex_a_rgb(color_hex)

def generar_cotizacion_docx(datos):
    """
    Genera el documento oficial en Word (.docx) aplicando las reglas editoriales institucionales.
    """
    doc = docx.Document()
    
    # --- MÁRGENES PROFESIONALES ---
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Pie de página institucional
        footer = section.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_ft = p_ft.add_run(f"{COMPANY_INFO['NAME']} — {COMPANY_INFO['SUBTITLE']}")
        run_ft.font.name = DOC_CONFIG["FONT_NAME"]
        run_ft.font.size = Pt(8.5)
        run_ft.font.color.rgb = _hex_a_rgb(COLORS["SECONDARY_HEX"])

    # --- 1. ENCABEZADO Y MEMBRETE ---
    p_hdr = doc.add_paragraph()
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run_comp = p_hdr.add_run(f"{COMPANY_INFO['NAME']}\n")
    run_comp.font.name = DOC_CONFIG["FONT_NAME"]
    run_comp.font.size = Pt(DOC_CONFIG["HEADER_SIZE_PT"])
    run_comp.font.bold = True
    run_comp.font.color.rgb = _hex_a_rgb(COLORS["PRIMARY_HEX"])
    
    run_sub = p_hdr.add_run(f"{COMPANY_INFO['SUBTITLE']}\nCotización Técnica y Comercial")
    run_sub.font.name = DOC_CONFIG["FONT_NAME"]
    run_sub.font.size = Pt(9.0)
    run_sub.font.color.rgb = _hex_a_rgb(COLORS["SECONDARY_HEX"])
    
    # --- 2. FECHA FORMAL MEXICANA ---
    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fecha_texto = obtener_fecha_formal(datos.get("ciudad"), datos.get("fecha_dt"))
    p_date.add_run(fecha_texto)
    _aplicar_estilo_parrafo(p_date, bold=True)
    
    # --- 3. BLOQUE DE DESTINATARIO ---
    p_client = doc.add_paragraph()
    p_client.paragraph_format.space_after = Pt(12)
    p_client.add_run(f"At'n: {datos.get('cliente_atencion', 'Ingeniero Responsable')}\n")
    if datos.get("cliente_cargo"):
        p_client.add_run(f"{datos.get('cliente_cargo')}\n")
    p_client.add_run(f"{datos.get('cliente_empresa', 'Empresa / Constructora')}\n")
    p_client.add_run("Presente.\n")
    p_client.add_run(f"\nRef: Propuesta de Servicios — {datos.get('nombre_proyecto', 'Levantamiento Topográfico')}")
    _aplicar_estilo_parrafo(p_client, bold=True, color_hex=COLORS["PRIMARY_HEX"])
    
    # --- 4. SECCIÓN 1: OBJETIVO DEL PROYECTO ---
    h1 = doc.add_heading(level=2)
    h1.add_run("1. Objetivo del Proyecto")
    _aplicar_estilo_parrafo(h1, size_pt=DOC_CONFIG["TITLE_SIZE_PT"], bold=True, color_hex=COLORS["PRIMARY_HEX"], keep_next=True)
    
    p_obj = doc.add_paragraph(datos.get("objetivo", ""))
    _aplicar_estilo_parrafo(p_obj)
    
    # --- 5. SECCIÓN 2: METODOLOGÍA DE TRABAJO ---
    h2 = doc.add_heading(level=2)
    h2.add_run("2. Metodología y Procedimiento Técnico")
    _aplicar_estilo_parrafo(h2, size_pt=DOC_CONFIG["TITLE_SIZE_PT"], bold=True, color_hex=COLORS["PRIMARY_HEX"], keep_next=True)
    
    p_met = doc.add_paragraph(datos.get("metodologia", ""))
    _aplicar_estilo_parrafo(p_met)
    
    # --- 6. SECCIÓN 3: EQUIPAMIENTO ESPECIALIZADO ---
    h3 = doc.add_heading(level=2)
    h3.add_run("3. Instrumentación y Equipo Desplegado")
    _aplicar_estilo_parrafo(h3, size_pt=DOC_CONFIG["TITLE_SIZE_PT"], bold=True, color_hex=COLORS["PRIMARY_HEX"], keep_next=True)
    
    p_eq = doc.add_paragraph(datos.get("equipo", ""))
    _aplicar_estilo_parrafo(p_eq)
    
    # --- 7. SECCIÓN 4: ENTREGABLES Y ARCHIVOS TÉCNICOS ---
    h4 = doc.add_heading(level=2)
    h4.add_run("4. Entregables del Proyecto")
    _aplicar_estilo_parrafo(h4, size_pt=DOC_CONFIG["TITLE_SIZE_PT"], bold=True, color_hex=COLORS["PRIMARY_HEX"], keep_next=True)
    
    for item in datos.get("entregables", []):
        p_ent = doc.add_paragraph(f"• {item}")
        p_ent.paragraph_format.left_indent = Inches(0.25)
        _aplicar_estilo_parrafo(p_ent)

    # --- 8. SECCIÓN 5: PROPUESTA ECONÓMICA ---
    h5 = doc.add_heading(level=2)
    h5.add_run("5. Propuesta Económica")
    _aplicar_estilo_parrafo(h5, size_pt=DOC_CONFIG["TITLE_SIZE_PT"], bold=True, color_hex=COLORS["PRIMARY_HEX"], keep_next=True)
    
    conceptos = datos.get("conceptos_economicos", [])
    num_filas = len(conceptos) + 2  # Encabezado + Conceptos + Fila Total
    tabla = doc.add_table(rows=num_filas, cols=3)
    tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers = ["Descripción del Servicio / Concepto", "Cant. / Unidad", "Importe (MXN)"]
    for i, title in enumerate(headers):
        celda = tabla.rows[0].cells[i]
        celda.text = title
        _set_cell_background(celda, COLORS["PRIMARY_HEX"])
        p = celda.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _aplicar_estilo_parrafo(p, bold=True, color_hex="FFFFFF")
        
    total_mxn = 0.0
    for idx, cons in enumerate(conceptos):
        monto = float(cons.get("monto", 0.0))
        total_mxn += monto
        row_cells = tabla.rows[idx + 1].cells
        row_cells[0].text = cons.get("desc", "Servicio topográfico")
        row_cells[1].text = cons.get("cant", "1 Lote")
        row_cells[2].text = f"$ {monto:,.2f}"
        
        row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if idx % 2 == 1:
            for col_c in row_cells:
                _set_cell_background(col_c, COLORS["ZEBRA_HEX"])
                
    # Fila de Total
    celda_tot_lbl = tabla.rows[-1].cells[1]
    celda_tot_lbl.text = "TOTAL (Sin I.V.A.):"
    celda_tot_lbl.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _aplicar_estilo_parrafo(celda_tot_lbl.paragraphs[0], bold=True, color_hex=COLORS["PRIMARY_HEX"])
    
    celda_tot_val = tabla.rows[-1].cells[2]
    celda_tot_val.text = f"$ {total_mxn:,.2f}"
    celda_tot_val.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _aplicar_estilo_parrafo(celda_tot_val.paragraphs[0], bold=True, color_hex=COLORS["PRIMARY_HEX"])
    
    doc.add_paragraph()
    
    # --- 9. SECCIÓN 6: EXCLUSIONES Y PREMISAS TÉCNICAS ---
    h6 = doc.add_heading(level=2)
    h6.add_run("6. Premisas Técnicas y Exclusiones")
    _aplicar_estilo_parrafo(h6, size_pt=DOC_CONFIG["TITLE_SIZE_PT"], bold=True, color_hex=COLORS["PRIMARY_HEX"], keep_next=True)
    
    for excl in datos.get("exclusiones", []):
        p_ex = doc.add_paragraph(f"• {excl}")
        p_ex.paragraph_format.left_indent = Inches(0.25)
        _aplicar_estilo_parrafo(p_ex, color_hex=COLORS["SECONDARY_HEX"])
        
    # --- 10. CLÁUSULAS Y SALUDO FINAL ---
    h7 = doc.add_heading(level=2)
    h7.add_run("7. Condiciones de Trabajo y Forma de Pago")
    _aplicar_estilo_parrafo(h7, size_pt=DOC_CONFIG["TITLE_SIZE_PT"], bold=True, color_hex=COLORS["PRIMARY_HEX"], keep_next=True)
    
    p_cl = doc.add_paragraph(datos.get("clausulas", (
        "• Vigencia de cotización: 15 días hábiles a partir de su emisión.\n"
        "• Condiciones de pago: 50% de anticipo para movilización de brigada en campo y 50% contra entrega de informe técnico y archivos finales.\n"
        "• Los precios enunciados están en Moneda Nacional (MXN) y no incluyen I.V.A."
    )))
    _aplicar_estilo_parrafo(p_cl)
    
    p_sal = doc.add_paragraph(datos.get("saludo_final", "Agradeciendo de antemano su confianza, quedamos a su entera disposición para cualquier aclaración técnica o modificación que requiera el proyecto."))
    _aplicar_estilo_parrafo(p_sal, keep_next=True)
    
    # --- 11. BLOQUE DE FIRMA Y DATOS BANCARIOS ---
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.keep_with_next = True
    p_sign.paragraph_format.space_before = Pt(24)
    
    run_att = p_sign.add_run("Atentamente,\n\n\n\n")
    run_att.font.name = DOC_CONFIG["FONT_NAME"]
    
    run_name = p_sign.add_run(f"{COMPANY_INFO['LEGAL_REP']}\n")
    run_name.bold = True
    run_name.font.color.rgb = _hex_a_rgb(COLORS["PRIMARY_HEX"])
    
    run_role = p_sign.add_run(f"{COMPANY_INFO['ROLE']}\n{COMPANY_INFO['NAME']}\n\n")
    run_role.font.size = Pt(9.5)
    
    run_bank = p_sign.add_run(f"Datos Bancarios para Anticipo: CLABE {COMPANY_INFO['CLABE_ENDING']} ({COMPANY_INFO['BANK_NAME']})")
    run_bank.font.size = Pt(8.5)
    run_bank.font.color.rgb = _hex_a_rgb(COLORS["SECONDARY_HEX"])
    
    # Salida en bytes puros para evitar bloqueos en Streamlit Cloud
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()
