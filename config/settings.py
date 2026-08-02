# config/settings.py
from datetime import datetime

# --- 1. IDENTIDAD INSTITUCIONAL ---
COMPANY_INFO = {
    "NAME": "DELTA Land Aerial Building Surveyors LABS",
    "SUBTITLE": "Servicios Profesionales de Topografía, Geodesia y Fotogrametría",
    "LEGAL_REP": "Ing. Fernando Cristofer Cárdenas Martínez",
    "ROLE": "Representante Legal y Director Técnico",
    "BANK_NAME": "Tu Banco Oficial",
    "CLABE_ENDING": "XXXXXXXXXXXXXX43",  # Configurado con tus parámetros oficiales
    "DEFAULT_CITY": "Ciudad de México"
}

# --- 2. PALETA DE COLORES EDITORIALES (PARA WORD Y PDF) ---
COLORS = {
    "PRIMARY_HEX": "1A5276",     # Azul marino corporativo (Títulos y membrete)
    "SECONDARY_HEX": "5D6D7E",   # Gris pizarra (Subtítulos y notas)
    "ZEBRA_HEX": "F2F4F4",       # Gris perla (Filas alternas de tablas económicas)
    "TEXT_HEX": "333333"         # Gris carbón (Texto general, más legible que el negro puro)
}

# --- 3. REGLAS DE DOCUMENTO ---
DOC_CONFIG = {
    "FONT_NAME": "Arial",
    "BODY_SIZE_PT": 10.5,
    "HEADER_SIZE_PT": 12.0,
    "TITLE_SIZE_PT": 11.0,
    "QUOTE_VALIDITY_DAYS": 15
}

# --- 4. FORMATEADOR FORMAL DE FECHAS ---
def obtener_fecha_formal(ciudad=None, fecha_dt=None):
    """
    Genera la fecha en formato: 'Ciudad de México a DD de MM del YYYY'
    """
    if ciudad is None:
        ciudad = COMPANY_INFO["DEFAULT_CITY"]
    if fecha_dt is None:
        fecha_dt = datetime.now()
        
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    
    dia = fecha_dt.strftime("%d")
    mes_nombre = meses[fecha_dt.month - 1]
    anio = fecha_dt.strftime("%Y")
    
    return f"{ciudad} a {dia} de {mes_nombre} del {anio}"
