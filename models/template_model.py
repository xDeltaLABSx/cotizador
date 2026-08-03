# models/template_model.py
import json
import os
from services.plantillas import cargar_plantillas_iniciales

RUTA_CATALOGO = os.path.join("data", "catalogo_seed.json")

def obtener_catalogo_completo():
    """Lee el catálogo desde JSON. Si le faltan las 21 plantillas oficiales de DELTA LABS, las sincroniza."""
    catalogo = {"servicios": [], "entregables": [], "exclusiones": []}
    
    if os.path.exists(RUTA_CATALOGO):
        try:
            with open(RUTA_CATALOGO, "r", encoding="utf-8") as f:
                catalogo = json.load(f)
        except Exception:
            pass

    if "servicios" not in catalogo:
        catalogo["servicios"] = []

    # Sincronizar las 21 plantillas de DELTA LABS si no están registradas
    plantillas_base = cargar_plantillas_iniciales()
    nombres_existentes = {s["nombre"] for s in catalogo["servicios"]}
    hubo_cambios = False

    for nombre, info in plantillas_base.items():
        if nombre not in nombres_existentes:
            s_id = nombre.lower().replace(" - ", "_").replace(" ", "_").replace("(", "").replace(")", "").replace("&", "y")
            catalogo["servicios"].append({
                "id": s_id,
                "nombre": nombre,
                "objetivo": info.get("objetivo", ""),
                "metodologia": info.get("metodología", info.get("metodologia", "")),
                "equipo": info.get("equipo", ""),
                "unidad_default": info.get("unidad", "m2"),
                "precio_unitario_default": info.get("precio_base", 10.0)
            })
            hubo_cambios = True

    if hubo_cambios:
        guardar_catalogo(catalogo)

    return catalogo

def guardar_catalogo(catalogo):
    """Guarda el catálogo en disco e invalida cachés si es necesario."""
    os.makedirs(os.path.dirname(RUTA_CATALOGO), exist_ok=True)
    try:
        with open(RUTA_CATALOGO, "w", encoding="utf-8") as f:
            json.dump(catalogo, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def obtener_servicio_por_id(servicio_id):
    """Obtiene la ficha técnica de un servicio en particular."""
    catalogo = obtener_catalogo_completo()
    for s in catalogo.get("servicios", []):
        if s["id"] == servicio_id:
            return s
    return None

def guardar_nueva_plantilla(nombre, objetivo, metodologia, equipo, unidad, precio_base):
    """Crea un nuevo servicio en el catálogo."""
    catalogo = obtener_catalogo_completo()
    s_id = nombre.lower().replace(" - ", "_").replace(" ", "_").replace("(", "").replace(")", "").replace("&", "y")
    
    nuevo = {
        "id": s_id,
        "nombre": nombre,
        "objetivo": objetivo,
        "metodologia": metodologia,
        "equipo": equipo,
        "unidad_default": unidad,
        "precio_unitario_default": float(precio_base)
    }
    
    catalogo["servicios"].append(nuevo)
    return guardar_catalogo(catalogo)

def actualizar_plantilla_por_id(s_id, nombre, objetivo, metodologia, equipo, unidad, precio_base):
    """Actualiza una plantilla existente."""
    catalogo = obtener_catalogo_completo()
    for s in catalogo.get("servicios", []):
        if s["id"] == s_id:
            s["nombre"] = nombre
            s["objetivo"] = objetivo
            s["metodologia"] = metodologia
            s["equipo"] = equipo
            s["unidad_default"] = unidad
            s["precio_unitario_default"] = float(precio_base)
            break
    return guardar_catalogo(catalogo)

def eliminar_plantilla_por_id(s_id):
    """Elimina una plantilla del catálogo permanentemente."""
    catalogo = obtener_catalogo_completo()
    catalogo["servicios"] = [s for s in catalogo.get("servicios", []) if s["id"] != s_id]
    return guardar_catalogo(catalogo)
