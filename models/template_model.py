# models/template_model.py
import json
import os

RUTA_CATALOGO = os.path.join("data", "catalogo_seed.json")

def obtener_catalogo_completo():
    """Lee el catálogo de servicios desde el archivo JSON de manera nativa."""
    catalogo = {"servicios": [], "entregables": [], "exclusiones": []}
    if os.path.exists(RUTA_CATALOGO):
        try:
            with open(RUTA_CATALOGO, "r", encoding="utf-8") as f:
                catalogo = json.load(f)
        except Exception:
            pass
    return catalogo

def guardar_catalogo(catalogo):
    """Guarda el catálogo actualizado en disco."""
    os.makedirs(os.path.dirname(RUTA_CATALOGO), exist_ok=True)
    try:
        with open(RUTA_CATALOGO, "w", encoding="utf-8") as f:
            json.dump(catalogo, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def obtener_servicio_por_id(servicio_id):
    catalogo = obtener_catalogo_completo()
    for s in catalogo.get("servicios", []):
        if s["id"] == servicio_id:
            return s
    return None

def guardar_nueva_plantilla(nombre, objetivo, metodologia, equipo, unidad, precio_base, entregables="", exclusiones=""):
    catalogo = obtener_catalogo_completo()
    s_id = nombre.lower().replace(" - ", "_").replace(" ", "_").replace("(", "").replace(")", "").replace("&", "y")
    
    nuevo = {
        "id": s_id,
        "nombre": nombre,
        "objetivo": objetivo,
        "metodologia": metodologia,
        "equipo": equipo,
        "unidad_default": unidad,
        "precio_unitario_default": float(precio_base),
        "area_min": 1.0,
        "precio_min": float(precio_base),
        "precio_extra": 0.0,
        "entregables": entregables,
        "exclusiones": exclusiones
    }
    catalogo["servicios"].append(nuevo)
    return guardar_catalogo(catalogo)

def actualizar_plantilla_por_id(s_id, nombre, objetivo, metodologia, equipo, unidad, precio_base, entregables="", exclusiones=""):
    catalogo = obtener_catalogo_completo()
    for s in catalogo.get("servicios", []):
        if s["id"] == s_id:
            s["nombre"] = nombre
            s["objetivo"] = objetivo
            s["metodologia"] = metodologia
            s["equipo"] = equipo
            s["unidad_default"] = unidad
            s["precio_unitario_default"] = float(precio_base)
            s["precio_min"] = float(precio_base)
            s["entregables"] = entregables
            s["exclusiones"] = exclusiones
            break
    return guardar_catalogo(catalogo)

def eliminar_plantilla_por_id(s_id):
    """Elimina permanentemente un servicio del catálogo."""
    catalogo = obtener_catalogo_completo()
    catalogo["servicios"] = [s for s in catalogo.get("servicios", []) if s["id"] != s_id]
    return guardar_catalogo(catalogo)
