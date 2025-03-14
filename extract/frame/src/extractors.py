# src/extractors.py
import re
import spacy

# Si deseas cargar un modelo spaCy en español:
# nlp = spacy.load("es_core_news_md")

def extract_metadata_from_law(text: str) -> dict:
    """
    Extrae metadatos de la ley (fecha, número, tipo, firmantes, etc.)
    usando expresiones regulares o spaCy.
    Retorna un diccionario con la info.
    """

    metadata = {}

    # --- EJEMPLO 1: Extraer número de Ley ---
    # Patrón posible: "LEY 1956" o "LEY No 1956"
    ley_match = re.search(r"(LEY\s+No?\s*(\d+))", text, re.IGNORECASE)
    if ley_match:
        metadata["numero_ley"] = ley_match.group(2)  # e.g. "1956"

    # --- EJEMPLO 2: Extraer fecha ---
    # Patrón: "4JUN2019" (aunque a veces puede tener espacios o formatos distintos)
    fecha_match = re.search(r"(\d{1,2}[A-Z]{3}\d{4})", text)
    if fecha_match:
        metadata["fecha"] = fecha_match.group(1)  # e.g. "4JUN2019"

    # --- EJEMPLO 3: Buscar firmantes ---
    # Podríamos usar un regex simplificado o spaCy para buscar nombres en mayúsculas.
    # Este es un ejemplo muy sencillo (no robusto).
    firmantes = re.findall(r"([A-ZÁÉÍÓÚÑ ]{5,})\n", text)
    # Filtra palabras sueltas y cosas raras:
    firmantes_limpios = []
    for f in firmantes:
        # Heurística: descartamos cadenas muy cortas
        if len(f.strip()) > 10:
            firmantes_limpios.append(f.strip())
    metadata["firmantes_detectados"] = firmantes_limpios

    # --- EJEMPLO 4: Tipo de acto (Ley o Acto Legislativo) ---
    # Asumiendo que si encuentra "LEY" en el texto, es un "ley"
    if "LEY" in text.upper():
        metadata["tipo_de_acto"] = "ley"
    else:
        metadata["tipo_de_acto"] = "acto_legislativo"

    # (Aquí podrías añadir más regex/spaCy para epígrafes, objeto, etc.)

    return metadata
