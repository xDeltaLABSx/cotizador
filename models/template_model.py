# models/template_model.py
import json
import os

SEED_PATH = os.path.join("data", "catalogo_seed.json")
CUSTOM_PATH = os.path.join("data", "catalogo_custom.json")

def _cargar_json(ruta):
    if not os.path.exists(ruta):
        return None
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def _guardar_json(ruta, datos):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def obtener_catalogo_completo():
    """
    Combina las plantillas base del sistema con las nuevas que hayas creado tú.
    """
    base = _cargar_json(SEED_PATH) or {"servicios": [], "exclusiones_default": [], "entregables_default": []}
    custom = _cargar_json(CUSTOM_PATH) or {"servicios": []}
    
    # Combinamos la lista de servicios (primero los base, luego tus personalizaciones)
    servicios_totales = base.get("servicios", []) + custom.get("servicios", [])
    
    return {
        "servicios": servicios_totales,
        "exclusiones": base.get("exclusiones_default", []),
        "entregables": base.get("entregables_default", [])
    }

def obtener_servicio_por_id(servicio_id):
    """
    Busca un servicio específico para rellenar los cuadros de texto en la app.
    """
    catalogo = obtener_catalogo_completo()
    for s in catalogo["servicios"]:
        if s["id"] == servicio_id:
            return s
    return None

def guardar_nueva_plantilla(nombre, objetivo, metodologia, equipo, unidad, precio_base):
    """
    Permite guardar un texto modificado como una NUEVA plantilla permanente en tu catálogo.
    """
    custom = _cargar_json(CUSTOM_PATH) or {"servicios": []}
    
    # Generamos un identificador único basado en el nombre
    nuevo_id = "custom_" + nombre.lower().replace(" ", "_").replace(".", "")[:20]
    
    nueva_plantilla = {
        "id": nuevo_id,
        "nombre": f"⭐ {nombre}",
        "objetivo": objetivo,
        "metodologia": metodologia,
        "equipo": equipo,
        "unidad_default": unidad,
        "precio_unitario_default": float(precio_base)
    }
    
    # Si ya existe una con ese ID, la actualizamos; si no, la agregamos
    servicios_existentes = [s for s in custom["servicios"] if s["id"] != nuevo_id]
    servicios_existentes.append(nueva_plantilla)
    custom["servicios"] = servicios_existentes
    
    _guardar_json(CUSTOM_PATH, custom)
    return nuevo_id
