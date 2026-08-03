# services/plantillas.py
import streamlit as st

PLANTILLAS_BASE = {
    "Topo - Planimetría (Libre)": {
        "unidad": "m2", "area_min": 2500.0, "precio_min": 4500.0, "precio_extra": 2.0,
        "objetivo": "Ejecutar el levantamiento planimétrico de detalle en terrenos de configuración libre o abierta para la delimitación perimetral y ubicación de elementos aparentes.",
        "metodología": "• Reconocimiento de linderos principales. • Estacionamiento y radiación con Estación Total de alta precisión o GNSS en modo RTK. • Procesamiento de libretas electrónicas y dibujo asistido en CAD.",
        "equipo": "• Estación Total de alta precisión • Bastones y prismas • Software CAD"
    },
    "Topo - Planimetria (Medio)": {
        "unidad": "m2", "area_min": 2500.0, "precio_min": 6000.0, "precio_extra": 4.0,
        "objetivo": "Realizar el levantamiento planimétrico en superficies con densidad media de vegetación u obstáculos urbanos para la correcta vinculación geométrica.",
        "metodología": "• Establecimiento de estaciones de enlace auxiliar. • Toma de puntos de control planimétrico intermedio. • Compensación de poligonales y dibujo vectorial.",
        "equipo": "• Estación Total • Sistema GNSS RTK • Software de procesamiento espacial"
    },
    "Topo - Planimetria (Alto)": {
        "unidad": "m2", "area_min": 2500.0, "precio_min": 7500.0, "precio_extra": 5.0,
        "objetivo": "Levantamiento planimétrico de alta complejidad en zonas con alta densidad de construcciones, desniveles o restricciones visuales severas.",
        "metodología": "• Densificación de red de apoyo local. • Levantamiento intensivo de esquinas, bardas y ejes constructivos. • Validación topológica estricta en gabinete.",
        "equipo": "• Estación Total motorizada • Sistema GNSS de doble frecuencia • Software CAD avanzado"
    },
    "Topo - P&A": {
        "unidad": "m2", "area_min": 2500.0, "precio_min": 6000.0, "precio_extra": 2.5,
        "objetivo": "Obtener la representación tridimensional detallada (planimetría y altimetría) del terreno mediante la generación de curvas de nivel y retícula de coordenadas.",
        "metodología": "• Enlace a bancos de nivel temporales o geodésicos. • Radiación mixta planialtimétrica de detalles del terreno y obras civiles. • Generación de modelo digital de elevación (MDE) y curvas de nivel.",
        "equipo": "• Sistema GNSS RTK • Estación Total de alta precisión • Software CAD y de modelado tridimensional"
    },
    "Topo - P&A&G": {
        "unidad": "m2", "area_min": 2500.0, "precio_min": 8000.0, "precio_extra": 2.5,
        "objetivo": "Ejecutar un levantamiento planialtimétrico integral rigurosamente georeferenciado al marco de referencia oficial (INEGI / ITRF) para proyectos de ingeniería ejecutiva.",
        "metodología": "• Ocupación estática GNSS para ligue a red geodésica nacional oficial. • Control de vértices monumentados en sitio. • Levantamiento intensivo P&A y ajuste por mínimos cuadrados.",
        "equipo": "• Receptores GNSS Geodésicos de Doble Frecuencia • Estación Total • Software Leica Infinity / Trimble / QGIS"
    },
    "Topo - P&A (ha)": {
        "unidad": "ha", "area_min": 1.0, "precio_min": 7000.0, "precio_extra": 2500.0,
        "objetivo": "Levantamiento topográfico planialtimétrico extensivo por hectárea para grandes extensiones territoriales, predios rústicos o corredores.",
        "metodología": "• Diseño de red de triangulación y bases de apoyo satelital. • Barrido topográfico con brigadas terrestres de apoyo y/o fotogrametría complementaria. • Procesamiento masivo de datos altimétricos.",
        "equipo": "• Receptores GNSS RTK Base/Rover • Estación Total • Software de diseño y cálculo de volúmenes"
    },
    "Topo - P&A&G (ha)": {
        "unidad": "ha", "area_min": 1.0, "precio_min": 10000.0, "precio_extra": 2500.0,
        "objetivo": "Levantamiento planialtimétrico georeferenciado por hectárea en predios de gran extensión con exigencia de certificación legal y técnica.",
        "metodología": "• Enlace geodésico primario de alta precisión. • Levantamiento sistemático por bloques y control de calidad por redundancia geométrica. • Generación de entregables oficiales georeferenciados.",
        "equipo": "• GNSS Geodésicos de Doble Frecuencia • Estación Total • Software de compensación espacial"
    },
    "Arq - Estructural": {
        "unidad": "m2", "area_min": 500.0, "precio_min": 7000.0, "precio_extra": 15.0,
        "objetivo": "Levantamiento dimensional de precisión enfocado en elementos estructurales (columnas, trabes, losas, muros de carga y desplomes) para proyectos arquitectónicos o de rehabilitación.",
        "metodología": "• Verificación de ejes estructurales principales. • Medición milimétrica de secciones de elementos y alturas libres. • Detección de desplomes y deflexiones.",
        "equipo": "• Distanciómetro láser de alta precisión • Estación Total • Software CAD"
    },
    "Arq - E&Instalaciones": {
        "unidad": "m2", "area_min": 500.0, "precio_min": 6500.0, "precio_extra": 18.0,
        "objetivo": "Levantamiento arquitectónico integral que incluye la estructura física y el mapeo de instalaciones especiales (hidráulicas, sanitarias, eléctricas, HVAC y contra incendio).",
        "metodología": "• Catastro de ductos, tableros, registros y salidas de instalaciones. • Vinculación espacial con el levantamiento estructural base. • Representación esquemática en planos especializados por ingenierías.",
        "equipo": "• Escáner láser portátil / Distanciómetros • Estación Total • Software BIM / CAD"
    },
    "Arq - Nave Industrial": {
        "unidad": "m2", "area_min": 500.0, "precio_min": 8000.0, "precio_extra": 12.0,
        "objetivo": "Levantamiento arquitectónico y dimensional de naves industriales, nudos de armaduras, nivelación de pisos industriales y crujías.",
        "metodología": "• Trazo de ejes longitudinales y transversales de la nave. • Verificación altimétrica de pisos de concreto y gálibos libres en cubierta. • Mapeo de columnas y bases de anclaje.",
        "equipo": "• Estación Total de alta precisión • Niveles ópticos/digitales de precisión • Software CAD"
    },
    "Arq - Local Comercial": {
        "unidad": "m2", "area_min": 500.0, "precio_min": 7000.0, "precio_extra": 10.0,
        "objetivo": "Levantamiento detallado de locales comerciales (interiores y fachadas) para adecuaciones de diseño interior, plazas comerciales o entrega de locales.",
        "metodología": "• Medición milimétrica de perímetros comerciales, vitrinas y alturas de marquesinas. • Ubicación de acometidas de servicios (agua, luz, drenaje). • Generación de planos arquitectónicos de estado actual.",
        "equipo": "• Medidores láser de corto alcance • Estación Total compacta • Software CAD"
    },
    "GNSS - Linea Base LOCAL": {
        "unidad": "lote", "area_min": 1.0, "precio_min": 3500.0, "precio_extra": 1000.0,
        "objetivo": "Medición y cálculo de líneas base geodésicas locales para el establecimiento de puntos de control primarios con enlace a la red municipal o estatal.",
        "metodología": "• Estacionamiento forzado en vértices extremos. • Observación estática simultánea con dos o más receptores GNSS. • Procesamiento vectorial y análisis de errores de cierre.",
        "equipo": "• Receptores GNSS Geodésicos de Doble Frecuencia • Trípodes y Tribrachs de alta precisión"
    },
    "GNSS - Linea Base Foraneo": {
        "unidad": "lote", "area_min": 1.0, "precio_min": 4000.0, "precio_extra": 1500.0,
        "objetivo": "Establecimiento y cálculo de líneas base geodésicas de largo alcance en zonas foráneas para proyectos de infraestructura regional o de gran envergadura.",
        "metodología": "• Planeación de sesiones de observación prolongadas. • Descarga y post-proceso de efemérides precisas en gabinete. • Ajuste de red por mínimos cuadrados.",
        "equipo": "• Par de Receptores GNSS Geodésicos avanzados • Software de post-proceso geodésico"
    },
    "Visita - Local": {
        "unidad": "jornada", "area_min": 1.0, "precio_min": 4500.0, "precio_extra": 4500.0,
        "objetivo": "Visita técnica de reconocimiento, inspección ocular o peritaje preliminar en zona local para evaluación de condiciones del terreno.",
        "metodología": "• Recorrido físico por el predio. • Toma de fotografías georeferenciadas y levantamiento de puntos de control rápido con GPS de mano. • Elaboración de reporte técnico preliminar.",
        "equipo": "• Dispositivos móviles de captura • GPS navegador • Equipamiento básico de protección"
    },
    "Visita - Foranea": {
        "unidad": "jornada", "area_min": 1.0, "precio_min": 6000.0, "precio_extra": 6000.0,
        "objetivo": "Visita de inspección, logística o evaluación técnica en zonas foráneas para validación operativa de proyectos.",
        "metodología": "• Desplazamiento a sitio de proyecto. • Inspección de accesos, puntos de control existentes y condiciones de seguridad operativa. • Emisión de bitácora de campo.",
        "equipo": "• Vehículo de campo • Equipamiento de captura digital y navegación"
    },
    "Cuadrilla - Local": {
        "unidad": "semana", "area_min": 1.0, "precio_min": 15000.0, "precio_extra": 0.0,
        "objetivo": "Asignación semanal de brigada topográfica completa (Topógrafo operador y ayudantes) para ejecución continua de obra civil en zona local.",
        "metodología": "• Ejecución de trazos, niveles, desplantes y referencias diarias solicitadas por la superintendencia de obra. • Registro en libretas de campo y control de tolerancias constructivas.",
        "equipo": "• Estación Total • Niveles • Jalones, prismas y herramienta menor de campo"
    },
    "Cuadrilla - Foranea": {
        "unidad": "semana", "area_min": 1.0, "precio_min": 19000.0, "precio_extra": 0.0,
        "objetivo": "Despliegue semanal de brigada topográfica especializada en zona foránea para soporte integral en proyectos carreteros, industriales o urbanización.",
        "metodología": "• Ejecución ininterrumpida de actividades de campo (trazo, control de terracerías, estructuras). • Reportes diarios de avance y supervisión técnica directa.",
        "equipo": "• Sistema GNSS RTK • Estación Total • Vehículo utilitario y equipo completo de medición"
    },
    "Fotogrametria - Jornada": {
        "unidad": "jornada", "area_min": 1.0, "precio_min": 9000.0, "precio_extra": 9000.0,
        "objetivo": "Ejecución de vuelos fotogramétricos con vehículos aéreos no tripulados (UAV) por jornada operativa para captura masiva de imágenes aéreas.",
        "metodología": "• Diseño y programación de planes de vuelo automatizados. • Colocación y medición de puntos de apoyo en tierra (GCP). • Ejecución de vuelos bajo normatividad aeronáutica.",
        "equipo": "• Dron profesional con cámara métrica • Receptores GNSS para GCPs • Estación de control de tierra"
    },
    "Fotogrametria - (ha)": {
        "unidad": "ha", "area_min": 3.0, "precio_min": 6000.0, "precio_extra": 750.0,
        "objetivo": "Procesamiento y generación de productos fotogramétricos (ortomosaicos de alta resolución, nubes de puntos densas y modelos digitales de elevación) por hectárea.",
        "metodología": "• Aerotriangulación y alineación fotogramétrica de imágenes. • Generación de malla poligonal y nube de puntos clasificada. • Exportación de ortomosaico georeferenciado en formato ráster y CAD.",
        "equipo": "• Software de procesamiento fotogramétrico (DJI Terra / Agisoft Metashape) • Estación de trabajo de alto rendimiento"
    },
    "Vuelo Lidar - Jornada": {
        "unidad": "jornada", "area_min": 1.0, "precio_min": 18000.0, "precio_extra": 18000.0,
        "objetivo": "Captura de datos geoespaciales mediante tecnología LiDAR aerotransportada por jornada para penetración de vegetación y modelado de alta densidad.",
        "metodología": "• Calibración del sistema LiDAR inercial y GPS en tierra. • Vuelo automatizado a baja altura sobre el corredor o poligonal de estudio. • Descarga y sincronización de nubes de puntos crudas.",
        "equipo": "• Sistema LiDAR aerotransportado montado en UAV • Base GNSS de referencia"
    },
    "Vuelo Lidar - Ha": {
        "unidad": "ha", "area_min": 50.0, "precio_min": 20000.0, "precio_extra": 600.0,
        "objetivo": "Procesamiento, filtrado y clasificación de nubes de puntos LiDAR por hectárea para extracción de terreno desnudo (Bare Earth) y perfiles longitudinales.",
        "metodología": "• Filtrado de ruido atmosférico y vegetación alta/baja. • Clasificación automatizada y manual de puntos (suelo, vegetación, estructuras). • Generación de curvas de nivel de alta precisión.",
        "equipo": "• Estaciones de trabajo especializadas • Software de procesamiento LiDAR"
    }
}

def cargar_plantillas_iniciales():
    if "plantillas_dinamicas" not in st.session_state:
        st.session_state["plantillas_dinamicas"] = PLANTILLAS_BASE
    return PLANTILLAS_BASE
