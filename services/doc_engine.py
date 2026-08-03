# services/doc_engine.py
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import io
import os
from config.settings import COMPANY_INFO, COLORS, obtener_fecha_formal

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Tipografía ejecutiva corporativa
FONT_NAME = "Segoe UI"
BODY_SIZE_PT = 10.0
TITLE_SIZE_PT = 11.5

def _hex_a_rgb(hex_str):
    return RGBColor(int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))

def _set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def _evitar_salto_fila(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def _aplicar_estilo_parrafo(p, size_pt=BODY_SIZE_PT, bold=False, color_hex=COLORS["TEXT_HEX"], keep_next=False, keep_together=True, space_after=4):
    p.paragraph_format.keep_with_next = keep_next
    p.paragraph_format.keep_together = keep_together
    p.paragraph_format.space_after = Pt(space_after)
    for run in p.runs:
        run.font.name = FONT_NAME
        run.font.size = Pt(size_pt)
        run.font.bold = bold
        run.font.color.rgb = _hex_a_rgb(color_hex)

def generar_cotizacion_docx(datos):
    """
    Genera el documento Word (.docx) replicando la estructura limpia, jerarquía y espaciados
    del formato manual de alta ingeniería.
    """
    ruta_plantilla = os.path.join(BASE_DIR, "assets", "plantilla_base.docx")
    
    if os.path.exists(ruta_plantilla):
        doc = docx.Document(ruta_plantilla)
        for p in list(doc.paragraphs):
            p._element.getparent().remove(p._element)
        for t in list(doc.tables):
            t._element.getparent().remove(t._element)
    else:
        doc = docx.Document()

    # Metadatos de Windows
    doc.core_properties.author = datos.get("autor_meta", "DELTA")
    doc.core_properties.title = datos.get("titulo_meta", "")
    doc.core_properties.keywords = datos.get("etiquetas_meta", "")

    # --- 1. FECHA FORMAL (Con espacio de respiración bajo el membrete gráfico) ---
    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_before = Pt(32)
    p_date.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fecha_texto = obtener_fecha_formal(datos.get("ciudad"), datos.get("fecha_dt"))
    p_date.add_run(f"Fecha: {fecha_texto}")
    _aplicar_estilo_parrafo(p_date, bold=True, space_after=12)
    
    # --- 2. BLOQUE DE DATOS DEL PROYECTO (Estilo Manual Izquierdo) ---
    p_client = doc.add_paragraph()
    p_client.paragraph_format.space_after = Pt(14)
    p_client.add_run(f"Atención a: {datos.get('cliente_atencion', 'Fernando')}\n")
    p_client.add_run(f"Proyecto: {datos.get('nombre_proyecto', 'Autopista Tijuana - Rosarito 2000')}\n")
    p_client.add_run(f"Ubicación: {datos.get('ciudad', 'Tijuana, Baja California')}\n")
    p_client.add_run(f"Servicio: {datos.get('objetivo', 'Trazo, Nivelación y Replanteo Topográfico')}")
    _aplicar_estilo_parrafo(p_client, bold=False, color_hex=COLORS["TEXT_HEX"], keep_next=True)
    
    # --- 3. SECCIÓN 1: ALCANCE TÉCNICO ---
    h1 = doc.add_heading(level=2)
    h1.add_run("1. Alcance Técnico del Proyecto")
    _aplicar_estilo_parrafo(h1, size_pt=TITLE_SIZE_PT, bold=True, color_hex=COLORS["PRIMARY_HEX"], keep_next=True, space_after=6)
    
    p_obj = doc.add_paragraph(datos.get("metodologia", "El servicio comprende los trabajos de campo y gabinete necesarios para la ubicación geométrica y altimétrica."))
    _aplicar_estilo_parrafo(p_obj, space_after=8)
    
    # Entregables / Subpuntos estructurados como en tu formato manual
    entregables_lista = datos.get("entregables", [])
    for idx, item in enumerate(entregables_lista):
        p_ent = doc.add_paragraph(f"• {item}")
        p_ent.paragraph_format.left_indent = Inches(0.2)
        _aplicar_estilo_parrafo(p_ent, space_after=3)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # --- 4. SECCIÓN 2: PROPUESTA ECONÓMICA (Igual a tu tabla manual) ---
    h2 = doc.add_heading(level=2)
    h2.add_run("2. Propuesta Económica")
    _aplicar_estilo_parrafo(h2, size_pt=TITLE_SIZE_PT, bold=True, color_hex=COLORS["PRIMARY_HEX"], keep_next=True, space_after=6)
    
    conceptos = datos.get("conceptos_economicos", [])
    num_filas = len(conceptos) + 2
    tabla = doc.add_table(rows=num_filas, cols=5)
    tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers = ["Concepto", "Personal y Equipamiento", "Duración", "Costo (MXN)", "Total (MXN)"]
    for i, title in enumerate(headers):
        celda = tabla.rows[0].cells[i]
        celda.text = title
        _set_cell_background(celda, COLORS["PRIMARY_HEX"])
        p = celda.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _aplicar_estilo_parrafo(p, size_pt=9.0, bold=True, color_hex="FFFFFF")
    
    _evitar_salto_fila(tabla.rows[0])
        
    total_mxn = 0.0
    for idx, cons in enumerate(conceptos):
        monto = float(cons.get("monto", 0.0))
        total_mxn += monto
        row_cells = tabla.rows[idx + 1].cells
        row_cells[0].text = cons.get("desc", "Servicio Topográfico")
        row_cells[1].text = "Brigada RTK / Estación"
        row_cells[2].text = "1 Semana"
        row_cells[3].text = f"$ {monto:,.2f}"
        row_cells[4].text = f"$ {monto:,.2f}"
        
        for c_idx in [1, 2, 3, 4]:
            row_cells[c_idx].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        if idx % 2 == 1:
            for col_c in row_cells:
                _set_cell_background(col_c, COLORS["ZEBRA_HEX"])
        _evitar_salto_fila(tabla.rows[idx + 1])
                
    # Fila de Total
    celda_tot_lbl = tabla.rows[-1].cells[3]
    celda_tot_lbl.text = "TOTAL:"
    celda_tot_lbl.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _aplicar_estilo_parrafo(celda_tot_lbl.paragraphs[0], size_pt=9.5, bold=True, color_hex=COLORS["PRIMARY_HEX"])
    
    celda_tot_val = tabla.rows[-1].cells[4]
    celda_tot_val.text = f"$ {total_mxn:,.2f}"
    celda_tot_val.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _aplicar_estilo_parrafo(celda_tot_val.paragraphs[0], size_pt=9.5, bold=True, color_hex=COLORS["PRIMARY_HEX"])
    _evitar_salto_fila(tabla.rows[-1])
    
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    
    # --- 5. SECCIÓN 3: CONDICIONES Y EXCLUSIONES ---
    h3 = doc.add_heading(level=2)
    h3.add_run("3. Condiciones de Ejecución y Forma de Pago")
    _aplicar_estilo_parrafo(h3, size_pt=TITLE_SIZE_PT, bold=True, color_hex=COLORS["PRIMARY_HEX"], keep_next=True, space_after=6)
    
    p_cl = doc.add_paragraph(datos.get("clausulas", (
        "• Vigencia de la cotización: 15 días hábiles.\n"
        "• Forma de pago: 50% de anticipo para movilización de brigada y 50% contra entrega de resultados.\n"
        "• Los precios no incluyen I.V.A."
    )))
    _aplicar_estilo_parrafo(p_cl, space_after=12)
    
    # --- 6. FIRMA ---
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.keep_together = True
    p_sign.add_run("Atentamente,\n\n\n")
    run_name = p_sign.add_run(f"{COMPANY_INFO['LEGAL_REP']}\n")
    run_name.bold = True
    run_name.font.color.rgb = _hex_a_rgb(COLORS["PRIMARY_HEX"])
    run_role = p_sign.add_run(f"{COMPANY_INFO['ROLE']}\n{COMPANY_INFO['NAME']}")
    run_role.font.size = Pt(9.0)
    _aplicar_estilo_parrafo(p_sign)
    
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()
