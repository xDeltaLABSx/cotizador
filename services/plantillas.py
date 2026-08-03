# services/plantillas.py
import streamlit as st

PLANTILLAS_BASE = {
    "Topo - Planimetría (Libre)": {
        "unidad": "m2", "area_min": 2500.0, "precio_min": 4500.0, "precio_extra": 2.0,
        "objetivo": "Ejecutar el levantamiento planimétrico de detalle en terrenos de configuración libre o abierta para la delimitación perimetral y ubicación de elementos aparentes.",
        "metodología": "• Reconocimiento de linderos principales. • Estacionamiento y radiación con Estación Total de alta precisión o GNSS en modo RTK. • Procesamiento de libretas electrónicas y dibujo asistido en CAD.",
        "equipo": "• Estación Total de alta precisión • Bastones y prismas • Software CAD",
        "entregables": (
            "Archivos CAD (DWG / DXF) con planimetría, retícula UTM y cuadro de construcción.\n"
            "Archivo de Coordenadas (CSV compatible con Trimble Coordinate Manager y Excel).\n"
            "Memoria Técnica Descriptiva y Reporte Fotográfico del predio."
        ),
        "exclusiones": (
            "No incluye brechas, tala, roza ni desmonte de vegetación para apertura de líneas de vista.\n"
            "No incluye pago de permisos, derechos de paso ni gestiones municipales para accesos a predios privados.\n"
            "El cliente garantizará el libre acceso y condiciones de seguridad para la brigada técnica en la zona de trabajo."
        )
    },
    "Topo - Planimetria (Medio)": {
        "unidad": "m2", "area_min": 2500.0, "precio_min": 6000.0, "precio_extra": 4.0,
        "objetivo": "Realizar el levantamiento planimétrico en superficies con densidad media de vegetación u obstáculos urbanos para la correcta vinculación geométrica.",
        "metodología": "• Establecimiento de estaciones de enlace auxiliar. • Toma de puntos de control planimétrico intermedio. • Compensación de poligonales y dibujo vectorial.",
        "equipo": "• Estación Total • Sistema GNSS RTK • Software de procesamiento espacial",
        "entregables": (
            "Archivos CAD (DWG / DXF) con planimetría compensada, retícula UTM y cuadro de construcción.\n"
            "Archivo de Coordenadas de los vértices (CSV compatible con Trimble Coordinate Manager y Excel).\n"
            "Memoria Técnica Descriptiva y Reporte Fotográfico de los puntos de control."
        ),
        "exclusiones": (
            "No incluye brechas, tala, roza ni desmonte de vegetación para apertura de líneas de vista.\n"
            "No incluye pago de permisos, derechos de paso ni gestiones municipales para accesos a predios privados.\n"
            "El cliente garantizará el libre acceso y condiciones de seguridad para la brigada técnica en la zona de trabajo."
        )
    },
    "Topo - Planimetria (Alto)": {
        "unidad": "m2", "area_min": 2500.0, "precio_min": 7500.0, "precio_extra": 5.0,
        "objetivo": "Levantamiento planimétrico de alta complejidad en zonas con alta densidad de construcciones, desniveles o restrictions visuales severas.",
        "metodología": "• Densificación de red de apoyo local. • Levantamiento intensivo de esquinas, bardas y ejes constructivos. • Validación topológica estricta en gabinete.",
        "equipo": "• Estación Total motorizada • Sistema GNSS de doble frecuencia • Software CAD avanzado",
        "entregables": (
            "Archivos CAD (DWG / DXF) a detalle con planimetría, retícula UTM y cuadro de construcción.\n"
            "Archivo de Coordenadas de detalle y poligonales (CSV compatible con Trimble Coordinate Manager y Excel).\n"
            "Memoria Técnica de compensación geométrica y Reporte Fotográfico."
        ),
        "exclusiones": (
            "No incluye brechas, tala, roza ni desmonte de vegetación para apertura de líneas de vista.\n"
            "No incluye pago de permisos, derechos de paso ni gestiones municipales para accesos a predios privados.\n"
            "El cliente garantizará el libre acceso y condiciones de seguridad para la brigada técnica en la zona de trabajo."
        )
    },
    "Topo - P&A": {
        "unidad": "m2", "area_min": 2500.0, "precio_min": 6000.0, "precio_extra": 2.5,
        "objetivo": "Obtener la representación tridimensional detallada (planimetría y altimetría) del terreno mediante la generación de curvas de nivel y retícula de coordenadas.",
        "metodología": "• Enlace a bancos de nivel temporales o geodésicos. • Radiación mixta planialtimétrica de detalles del terreno y obras civiles. • Generación de modelo digital de elevación (MDE) y curvas de nivel.",
        "equipo": "• Sistema GNSS RTK • Estación Total de alta precisión • Software CAD y de modelado tridimensional",
        "entregables": (
            "Archivos CAD (DWG / DXF) con planimetría, altimetría, retícula UTM y curvas de nivel a equidistancia convenida.\n"
            "Archivo de Coordenadas planialtimétricas (CSV compatible con Trimble Coordinate Manager y Excel).\n"
            "Modelo Digital de Elevación (MDE) en formato CAD/Ráster y Memoria Descriptiva."
        ),
        "exclusiones": (
            "No incluye brechas, tala, roza ni desmonte de vegetación para apertura de líneas de vista.\n"
            "No incluye pago de permisos, derechos de paso ni gestiones municipales para accesos a predios privados.\n"
            "El cliente garantizará el libre acceso y condiciones de seguridad para la brigada técnica en la zona de trabajo."
        )
    },
    "Topo - P&A&G": {
        "unidad": "m2", "area_min": 2500.0, "precio_min": 8000.0, "precio_extra": 2.5,
        "objetivo": "Ejecutar un levantamiento planialtimétrico integral rigurosamente georeferenciado al marco de referencia oficial (INEGI / ITRF) para proyectos de ingeniería ejecutiva.",
        "metodología": "• Ocupación estática GNSS para ligue a red geodésica nacional oficial. • Control de vértices monumentados en sitio. • Levantamiento intensivo P&A y ajuste por mínimos cuadrados.",
        "equipo": "• Receptores GNSS Geodésicos de Doble Frecuencia • Estación Total • Software Leica Infinity / Trimble / QGIS",
        "entregables": (
            "Plano Ejecutivo CAD (DWG / DXF) georeferenciado con planimetría, altimetría y curvas de nivel.\n"
            "Archivo de Coordenadas ITRF/UTM (CSV compatible con Trimble Coordinate Manager y Excel).\n"
            "Memoria Geodésica de post-proceso con ligue al marco de referencia oficial (INEGI/ITRF) y monografías de vértices."
        ),
        "exclusiones": (
            "No incluye brechas, tala, roza ni desmonte de vegetación para apertura de líneas de vista.\n"
            "No incluye pago de permisos, derechos de paso ni gestiones municipales para accesos a predios privados.\n"
            "El cliente garantizará el libre acceso y condiciones de seguridad para la brigada técnica en la zona de trabajo."
        )
    },
    "Topo - P&A (ha)": {
        "unidad": "ha", "area_min": 1.0, "precio_min": 7000.0, "precio_extra": 2500.0,
        "objetivo": "Levantamiento topográfico planialtimétrico extensivo por hectárea para grandes extensiones territoriales, predios rústicos o corredores.",
        "metodología": "• Diseño de red de triangulación y bases de apoyo satelital. • Barrido topográfico con brigadas terrestres de apoyo y/o fotogrametría complementaria. • Procesamiento masivo de datos altimétricos.",
        "equipo": "• Receptores GNSS RTK Base/Rover • Estación Total • Software de diseño y cálculo de volúmenes",
        "entregables": (
            "Archivos CAD (DWG / DXF) general y por cuadro con curvas de nivel y detalles topográficos.\n"
            "Archivo de Coordenadas masivo (CSV compatible con Trimble Coordinate Manager y Excel).\n"
            "Memoria Técnica Descriptiva del predio general y Reporte Fotográfico."
        ),
        "exclusiones": (
            "No incluye brechas, tala, roza ni desmonte de vegetación para apertura de líneas de vista.\n"
            "No incluye pago de permisos, derechos de paso ni gestiones municipales para accesos a predios privados.\n"
            "El cliente garantizará el libre acceso y condiciones de seguridad para la brigada técnica en la zona de trabajo."
        )
    },
    "Topo - P&A&G (ha)": {
        "unidad": "ha", "area_min": 1.0, "precio_min": 10000.0, "precio_extra": 2500.0,
        "objetivo": "Levantamiento planialtimétrico georeferenciado por hectárea en predios de gran extensión con exigencia de certificación legal y técnica.",
        "metodología": "• Enlace geodésico primario de alta precisión. • Levantamiento sistemático por bloques y control de calidad por redundancia geométrica. • Generación de entregables oficiales georeferenciados.",
        "equipo": "• GNSS Geodésicos de Doble Frecuencia • Estación Total • Software de compensación espacial",
        "entregables": (
            "Planos CAD (DWG / DXF) georeferenciados con modelo altimétrico e información catastral del polígono.\n"
            "Archivo de Coordenadas de linderos y superficie (CSV compatible con Trimble Coordinate Manager y Excel).\n"
            "Memoria Geodésica oficial con certificación de enlace al marco ITRF/INEGI y monografías de control."
        ),
        "exclusiones": (
            "No incluye brechas, tala, roza ni desmonte de vegetación para apertura de líneas de vista.\n"
            "No incluye pago de permisos, derechos de paso ni gestiones municipales para accesos a predios privados.\n"
            "El cliente garantizará el libre acceso y condiciones de seguridad para la brigada técnica en la zona de trabajo."
        )
    },
    "Arq - Estructural": {
        "unidad": "m2", "area_min": 500.0, "precio_min": 7000.0, "precio_extra": 15.0,
        "objetivo": "Levantamiento dimensional de precisión enfocado en elementos estructurales (columnas, trabes, losas, muros de carga y desplomes) para proyectos arquitectónicos o de rehabilitación.",
        "metodología": "• Verificación de ejes estructurales principales. • Medición milimétrica de secciones de elementos y alturas libres. • Detección de desplomes y deflexiones.",
        "equipo": "• Distanciómetro láser de alta precisión • Estación Total • Software CAD",
        "entregables": (
            "Planos Estructurales de estado actual en formato CAD (DWG / DXF) con ejes, columnas, muros y trabes.\n"
            "Cortes arquitectónicos y estructurales indicando niveles libres y alturas.\n"
            "Memoria Técnica dimensional indicando desplomes observados y Reporte Fotográfico."
        ),
        "exclusiones": (
            "No incluye calas, peritajes de resistencia de concreto ni estudios de mecánica de suelos.\n"
            "No incluye desmontaje de plafones, acabados o paneles para descubrir estructuras ocultas.\n"
            "El cliente garantizará iluminación suficiente y acceso libre a los elementos estructurales a medir."
        )
    },
    "Arq - E&Instalaciones": {
        "unidad": "m2", "area_min": 500.0, "precio_min": 6500.0, "precio_extra": 18.0,
        "objetivo": "Levantamiento arquitectónico integral que incluye la structure física y el mapeo de instalaciones especiales (hidráulicas, sanitarias, eléctricas, HVAC y contra incendio).",
        "metodología": "• Catastro de ductos, tableros, registros y salidas de instalaciones. • Vinculación espacial con el levantamiento estructural base. • Representación esquemática en planos especializados por ingenierías.",
        "equipo": "• Escáner láser portátil / Distanciómetros • Estación Total • Software BIM / CAD",
        "entregables": (
            "Planos Arquitectónicos y de Instalaciones en CAD (DWG / DXF) diferenciados por ingenierías.\n"
            "Mapeo de registros, tableros, bajadas pluviales/sanitarias y trayectorias de HVAC visibles.\n"
            "Reporte Fotográfico y Memoria Descriptiva del estado aparente de las instalaciones."
        ),
        "exclusiones": (
            "No incluye rastreo de tuberías ocultas sin registro visible ni pruebas de presión/estanqueidad.\n"
            "No incluye desmontaje de acabados ni intervención de equipos electromecánicos energizados.\n"
            "El cliente facilitará el acceso a cuartos de máquinas, azoteas y ductos principales."
        )
    },
    "Arq - Nave Industrial": {
        "unidad": "m2", "area_min": 500.0, "precio_min": 8000.0, "precio_extra": 12.0,
        "objetivo": "Levantamiento arquitectónico y dimensional de naves industriales, nudos de armaduras, nivelación de pisos industriales y crujías.",
        "metodología": "• Trazo de ejes longitudinales y transversales de la nave. • Verificación altimétrica de pisos de concreto y gálibos libres en cubierta. • Mapeo de columnas y bases de anclaje.",
        "equipo": "• Estación Total de alta precisión • Niveles ópticos/digitales de precisión • Software CAD",
        "entregables": (
            "Planos Arquitectónicos y de distribución estructural de la nave industrial en CAD (DWG / DXF).\n"
            "Planta altimétrica con nivelación milimétrica de firme de concreto y perfiles longitudinales/transversales.\n"
            "Reporte Técnico de gálibos libres y estado dimensional de crujías."
        ),
        "exclusiones": (
            "No incluye interrupción de operaciones de la línea de producción (se trabajará bajo coordinación).\n"
            "No incluye inspección de soldaduras ni ensayos no destructivos en estructura metálica.\n"
            "El cliente proporcionará permisos de acceso y el equipo de protección personal específico si el sitio lo requiere."
        )
    },
    "Arq - Local Comercial": {
        "unidad": "m2", "area_min": 500.0, "precio_min": 7000.0, "precio_extra": 10.0,
        "objetivo": "Levantamiento detallado de locales comerciales (interiores y fachadas) para adecuaciones de diseño interior, plazas comerciales o entrega de locales.",
        "metodología": "• Medición milimétrica de perímetros comerciales, vitrinas y alturas de marquesinas. • Ubicación de acometidas de servicios (agua, luz, drenaje). • Generación de planos arquitectónicos de estado actual.",
        "equipo": "• Medidores láser de corto alcance • Estación Total compacta • Software CAD",
        "entregables": (
            "Planos Arquitectónicos de estado actual (Planta de conjunto, fachadas y cortes) en CAD (DWG / DXF).\n"
            "Detalle de acometidas de servicios públicos/plazas (agua, luz, drenaje, voz y datos).\n"
            "Memoria de superficies útiles y comerciales con Reporte Fotográfico."
        ),
        "exclusiones": (
            "No incluye gestiones ni pagos administrativos ante la gerencia de plazas comerciales para ingreso de equipo.\n"
            "No abarca el desmontaje de mobiliario comercial, estanterías o muros falsos de exhibición.\n"
            "El cliente coordinará los horarios de ingreso para no afectar la operación del centro comercial."
        )
    },
    "GNSS - Linea Base LOCAL": {
        "unidad": "lote", "area_min": 1.0, "precio_min": 3500.0, "precio_extra": 1000.0,
        "objetivo": "Medición y cálculo de líneas base geodésicas locales para el establecimiento de puntos de control primarios con enlace a la red municipal o estatal.",
        "metodología": "• Estacionamiento forzado en vértices extremos. • Observación estática simultánea con dos o más receptores GNSS. • Procesamiento vectorial y análisis de errores de cierre.",
        "equipo": "• Receptores GNSS Geodésicos de Doble Frecuencia • Trípodes y Tribrachs de alta precisión",
        "entregables": (
            "Archivo de Coordenadas geodésicas y proyectadas de las líneas base (CSV compatible con Trimble Coordinate Manager y Excel).\n"
            "Memoria Geodésica de cálculo vectorial, análisis de vectores y reporte de cierre de red.\n"
            "Monografías descriptivas oficiales de cada vértice con ubicación, croquis y fotografías."
        ),
        "exclusiones": (
            "No incluye la construcción civil de mojoneras profundas de concreto (se cotiza de forma adicional por unidad).\n"
            "No abarca trabajos de levantamiento topográfico de detalle (únicamente establecimiento de la red de control).\n"
            "El cliente garantizará permisos de acceso y resguardo de la instrumentación durante las observaciones satelitales."
        )
    },
    "GNSS - Linea Base Foraneo": {
        "unidad": "lote", "area_min": 1.0, "precio_min": 4000.0, "precio_extra": 1500.0,
        "objetivo": "Establecimiento y cálculo de líneas base geodésicas de largo alcance en zonas foráneas para proyectos de infraestructura regional o de gran envergadura.",
        "metodología": "• Planeación de sesiones de observación prolongadas. • Descarga y post-proceso de efemérides precisas en gabinete. • Ajuste de red por mínimos cuadrados.",
        "equipo": "• Par de Receptores GNSS Geodésicos avanzados • Software de post-proceso geodésico",
        "entregables": (
            "Archivo de Coordenadas de alta precisión ITRF/UTM (CSV compatible con Trimble Coordinate Manager y Excel).\n"
            "Memoria de Post-proceso Geodésico con efemérides precisas y ligue a estaciones CORS/RGNA del INEGI.\n"
            "Monografías técnicas georeferenciadas de los vértices geodésicos establecidos."
        ),
        "exclusiones": (
            "No incluye la construcción civil de mojoneras geodésicas monumentadas de concreto (salvo acuerdo contractual previo).\n"
            "No abarca permisos especiales de tránsito por terrenos comunitarios, ejidales o zonas de acceso restringido.\n"
            "El cliente garantizará condiciones operativas de seguridad para la brigada técnica en el territorio foráneo."
        )
    },
    "Visita - Local": {
        "unidad": "jornada", "area_min": 1.0, "precio_min": 4500.0, "precio_extra": 4500.0,
        "objetivo": "Visita técnica de reconocimiento, inspección ocular o peritaje preliminar en zona local para evaluación de condiciones del terreno.",
        "metodología": "• Recorrido físico por el predio. • Toma de fotografías georeferenciadas y levantamiento de puntos de control rápido con GPS de mano. • Elaboración de reporte técnico preliminar.",
        "equipo": "• Dispositivos móviles de captura • GPS navegador • Equipamiento básico de protección",
        "entregables": (
            "Reporte Técnico de Reconocimiento y Evaluación del sitio en formato PDF.\n"
            "Archivo de Coordenadas expeditas de linderos o puntos de interés (CSV compatible con Trimble Coordinate Manager y Excel).\n"
            "Memoria Fotográfica georeferenciada de campo."
        ),
        "exclusiones": (
            "No incluye la emisión de planos topográficos de detalle con valor ejecutivo o legal.\n"
            "No abarca trazos, nivelaciones ni replanteos en obra durante el periodo de inspección.\n"
            "El cliente proveerá el acceso libre y acompañamiento en sitio si el predio requiere autorización."
        )
    },
    "Visita - Foranea": {
        "unidad": "jornada", "area_min": 1.0, "precio_min": 6000.0, "precio_extra": 6000.0,
        "objetivo": "Visita de inspección, logística o evaluación técnica en zonas foráneas para validación operativa de proyectos.",
        "metodología": "• Desplazamiento a sitio de proyecto. • Inspección de accesos, puntos de control existentes y condiciones de seguridad operativa. • Emisión de bitácora de campo.",
        "equipo": "• Vehículo de campo • Equipamiento de captura digital y navegación",
        "entregables": (
            "Reporte Ejecutivo de Visita e Inspección Técnica Foránea con factibilidad operativa y logística.\n"
            "Archivo de Coordenadas preliminares de campo (CSV compatible con Trimble Coordinate Manager y Excel).\n"
            "Anexo fotográfico georeferenciado y bitácora de reconocimiento de rutas de acceso."
        ),
        "exclusiones": (
            "No incluye trabajos ejecutivos de topografía de detalle ni trazos constructivos en sitio.\n"
            "No incluye gestiones ante autoridades municipales o ejidales para el ingreso a la propiedad.\n"
            "El cliente facilitará los permisos de acceso y el enlace de contacto en el sitio del proyecto."
        )
    },
    "Cuadrilla - Local": {
        "unidad": "semana", "area_min": 1.0, "precio_min": 15000.0, "precio_extra": 0.0,
        "objetivo": "Asignación semanal de brigada topográfica completa (Topógrafo operador y ayudantes) para ejecución continua de obra civil en zona local.",
        "metodología": "• Ejecución de trazos, niveles, desplantes y referencias diarias solicitadas por la superintendencia de obra. • Registro en libretas de campo y control de tolerancias constructivas.",
        "equipo": "• Estación Total • Niveles • Jalones, prismas y herramienta menor de campo",
        "entregables": (
            "Bitácora diaria de campo con registro de trazos, nivelaciones, desniveles y referencias ejecutadas.\n"
            "Archivo de Coordenadas de replanteo y control diario (CSV compatible con Trimble Coordinate Manager y Excel).\n"
            "Reporte semanal de avance técnico firmado por la residencia o superintendencia del cliente."
        ),
        "exclusiones": (
            "No incluye firma como Director Responsable de Obra (DRO) ni corresponsabilidad estructural técnica.\n"
            "No incluye suministro de monumentos definitivos de concreto, mojoneras ni varillas (únicamente estacas de trazo y madera).\n"
            "El cliente será responsable de proporcionar condiciones de seguridad laboral e industrial en su frente de obra."
        )
    },
    "Cuadrilla - Foranea": {
        "unidad": "semana", "area_min": 1.0, "precio_min": 19000.0, "precio_extra": 0.0,
        "objetivo": "Despliegue semanal de brigada topográfica especializada en zona foránea para soporte integral en proyectos carreteros, industriales o urbanización.",
        "metodología": "• Ejecución ininterrumpida de actividades de campo (trazo, control de terracerías, estructuras). • Reportes diarios de avance y supervisión técnica directa.",
        "equipo": "• Sistema GNSS RTK • Estación Total • Vehículo utilitario y equipo completo de medición",
        "entregables": (
            "Bitácora de campo diaria con registro y esquemas de trazos, secciones y niveles ejecutados en obra.\n"
            "Archivo de Coordenadas de replanteo y control geodésico (CSV compatible con Trimble Coordinate Manager y Excel).\n"
            "Reporte semanal de avance y productividad de brigada firmado por el residente del proyecto."
        ),
        "exclusiones": (
            "No incluye gastos excepcionales de casetas de cuota o peajes en rutas extraordinarias (fuera del trayecto base acordado).\n"
            "No incluye el suministro de mojoneras geodésicas ni concreto estructural para monumentación fija.\n"
            "El cliente garantizará la seguridad física y de tránsito para el personal de DELTA LABS en la zona de trabajo."
        )
    },
    "Fotogrametria - Jornada": {
        "unidad": "jornada", "area_min": 1.0, "precio_min": 9000.0, "precio_extra": 9000.0,
        "objetivo": "Ejecución de vuelos fotogramétricos con vehículos aéreos no tripulados (UAV) por jornada operativa para captura masiva de imágenes aéreas.",
        "metodología": "• Diseño y programación de planes de vuelo automatizados. • Colocación y medición de puntos de apoyo en tierra (GCP). • Ejecución de vuelos bajo normatividad aeronáutica.",
        "equipo": "• Dron profesional con cámara métrica • Receptores GNSS para GCPs • Estación de control de tierra",
        "entregables": (
            "Paquete de imágenes aéreas originales en alta resolución libres de distorsión óptica.\n"
            "Archivo de Coordenadas de los Puntos de Control Terrestre - GCPs (CSV compatible con Trimble Coordinate Manager y Excel).\n"
            "Reporte técnico de vuelo fotogramétrico indicando parámetros aerotransportados y cobertura operativa."
        ),
        "exclusiones": (
            "No incluye procesamiento especializado en gabinete para ortomosaicos o modelos 3D (se cotiza por hectárea por separado).\n"
            "No abarca tramitología de permisos excepcionales de vuelo ante AFAC/SENEAM en zonas restringidas aéreas.\n"
            "El cliente es responsable de garantizar el acceso físico a los predios para la colocación de los objetivos o lonas de apoyo (GCP)."
        )
    },
    "Fotogrametria - (ha)": {
        "unidad": "ha", "area_min": 3.0, "precio_min": 6000.0, "precio_extra": 750.0,
        "objetivo": "Procesamiento y generación de productos fotogramétricos (ortomosaicos de alta resolución, nubes de puntos densas y modelos digitales de elevación) por hectárea.",
        "metodología": "• Aerotriangulación y alineación fotogramétrica de imágenes. • Generación de malla poligonal y nube de puntos clasificada. • Exportación de ortomosaico georeferenciado en formato ráster y CAD.",
        "equipo": "• Software de procesamiento fotogramétrico (DJI Terra / Agisoft Metashape) • Estación de trabajo de alto rendimiento",
        "entregables": (
            "Ortomosaico georeferenciado de alta resolución espacial en formato ráster (GeoTIFF / ECW).\n"
            "Modelo Digital de Elevación (MDE) y Curvas de Nivel generadas en formato CAD (DWG / DXF).\n"
            "Nube de Puntos Fotogramétrica densa en formato estándar (.LAS / .LAZ) y Reporte Técnico de Calidad."
        ),
        "exclusiones": (
            "No abarca el levantamiento topográfico tradicional bajo vegetación extremadamente densa (para penetración de follaje se requiere tecnología LiDAR).\n"
            "No incluye trámites gubernamentales o aeronáuticos en caso de restricción del espacio aéreo local.\n"
            "El cliente garantizará las condiciones climáticas operativas y el libre acceso al predio de estudio."
        )
    },
    "Vuelo Lidar - Jornada": {
        "unidad": "jornada", "area_min": 1.0, "precio_min": 18000.0, "precio_extra": 18000.0,
        "objetivo": "Captura de datos geoespaciales mediante tecnología LiDAR aerotransportada por jornada para penetración de vegetación y modelado de alta densidad.",
        "metodología": "• Calibración del sistema LiDAR inercial y GPS en tierra. • Vuelo automatizado a baja altura sobre el corredor o poligonal de estudio. • Descarga y sincronización de nubes de puntos crudas.",
        "equipo": "• Sistema LiDAR aerotransportado montado en UAV • Base GNSS de referencia",
        "entregables": (
            "Archivo original de nube de puntos LiDAR aerotransportada (.LAS / .LAZ) con sincronización inercial (IMU/GNSS).\n"
            "Archivo de Coordenadas de la estación base geodésica de referencia (CSV compatible con Trimble Coordinate Manager y Excel).\n"
            "Reporte Técnico Operativo de jornada de captura LiDAR indicando densidad media por m2."
        ),
        "exclusiones": (
            "No incluye la clasificación de terreno ni depuración en gabinete de la nube de puntos (se cotiza por hectárea como servicio de procesamiento).\n"
            "No abarca vuelos en condiciones meteorológicas adversas que pongan en peligro la aeronavegabilidad del equipo.\n"
            "El cliente proporcionará los permisos de despegue y resguardo dentro de su predio o frente de obra."
        )
    },
    "Vuelo Lidar - Ha": {
        "unidad": "ha", "area_min": 50.0, "precio_min": 20000.0, "precio_extra": 600.0,
        "objetivo": "Procesamiento, filtrado y clasificación de nubes de puntos LiDAR por hectárea para extracción de terreno desnudo (Bare Earth) y perfiles longitudinales.",
        "metodología": "• Filtrado de ruido atmosférico y vegetación alta/baja. • Clasificación automatizada y manual de puntos (suelo, vegetación, estructuras). • Generación de curvas de nivel de alta precisión.",
        "equipo": "• Estaciones de trabajo especializadas • Software de procesamiento LiDAR",
        "entregables": (
            "Nube de Puntos LiDAR clasificada (.LAS / .LAZ) con extracción técnica de terreno desnudo (Bare Earth).\n"
            "Modelo Digital de Terreno (MDT) de alta precisión y Curvas de Nivel en formato vectorial CAD (DWG / DXF).\n"
            "Archivo de Coordenadas de control terrestre altimétrico (CSV compatible con Trimble Coordinate Manager y Excel).\n"
            "Memoria Técnica de calibración de sistema y precisión en Z (altimetría)."
        ),
        "exclusiones": (
            "No incluye tala, poda ni remoción física de vegetación en campo (la penetración y filtrado se realiza digitalmente).\n"
            "No abarca la batimetría ni levantamiento subacuático en ríos, presas o cuerpos de agua profundos.\n"
            "El cliente garantizará el acceso a los puntos terrestres para las comprobaciones de control geodésico."
        )
    }
}

def cargar_plantillas_iniciales():
    """Devuelve las plantillas base y las inicializa en sesión si no existen."""
    if "plantillas_dinamicas" not in st.session_state:
        st.session_state["plantillas_dinamicas"] = PLANTILLAS_BASE
    return PLANTILLAS_BASE
