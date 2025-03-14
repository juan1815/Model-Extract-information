# src/pipeline.py
import logging
import os
import re
import json

from deepdoctection.dataflow.serialize import DataFromFiles
from deepdoctection.dataflow.map import MapData
from deepdoctection.dataflow.base import CacheData
from deepdoctection.dataflow.transform import FlattenPages
from deepdoctection.mapper import mapper_fn
from deepdoctection import Document

# Importa tu OCR backend preferido. Aquí usaremos Tesseract como ejemplo:
from deepdoctection.extern.ocr import TesseractOcrEngine

# Si deseas usar spaCy para refinar la extracción:
import spacy

# Importamos funciones auxiliares de extracción
from src.extractors import extract_metadata_from_law

def build_pipeline(pdf_path: str):
    """
    Construye un DataFlow de DeepDoctection para:
    1. Leer PDFs de una carpeta o archivo específico.
    2. Convertirlos a imágenes de página.
    3. Ejecutar OCR.
    4. Extraer metadatos.
    """
    # 1. Crear DataFlow que lea PDFs
    df = DataFromFiles(pdf_path)

    # 2. Convertir PDFs en páginas de imagen
    #    DeepDoctection lo hace internamente usando un 'convert_to_image' (Ghostscript o similar).
    #    Por defecto, DataFromFiles + FlattenPages ya crea objetos Document con páginas individuales.
    df = df.apply(FlattenPages())

    # 3. Configurar el OCR con Tesseract
    ocr_engine = TesseractOcrEngine()

    @mapper_fn
    def run_ocr(doc: Document) -> Document:
        # doc.viz() -> imagen PIL de la página
        # Ejecutamos OCR en la imagen
        ocr_result = ocr_engine.run(doc.viz_as_pil)
        # Guardamos el texto en doc.text
        doc.text = ocr_result.text
        return doc

    df = df.map(run_ocr)

    # 4. Extraer metadatos (fecha, número de ley, firmantes, etc.) con una función auxiliar
    @mapper_fn
    def extract_metadata(doc: Document) -> Document:
        # doc.text ahora contiene el texto OCR de la página
        # Llamamos a nuestra función que hace la magia de regex, spaCy, etc.
        metadata = extract_metadata_from_law(doc.text)
        # Guardamos la metadata en doc.user_data para uso posterior
        doc.user_data["metadata"] = metadata
        return doc

    df = df.map(extract_metadata)

    # 5. (Opcional) Cachear resultados para no repetir OCR en cada corrida
    df = CacheData(df, cache_size=1)

    return df

def main():
    logging.basicConfig(level=logging.INFO)
    # Ruta del PDF a procesar
    pdf_path = "data/pdf/20190604 LEY 1956.pdf"
    
    # Construimos el pipeline
    df = build_pipeline(pdf_path)

    # Iteramos sobre cada página procesada
    # y recopilamos la metadata de cada una
    all_metadata = []
    for doc in df:
        # Extraemos la metadata que guardamos en doc.user_data["metadata"]
        meta = doc.user_data.get("metadata", {})
        # Agregamos info adicional si queremos, p. ej. número de página
        page_info = {
            "file_name": doc.file_name,
            "page_index": doc.page_idx,
            "metadata": meta
        }
        all_metadata.append(page_info)

    # Al final, podríamos guardar todo en un JSON
    with open("resultado_ley1956.json", "w", encoding="utf-8") as f:
        json.dump(all_metadata, f, ensure_ascii=False, indent=4)

    logging.info("Procesamiento finalizado. Revisa 'resultado_ley1956.json' para ver la salida.")

if __name__ == "__main__":
    main()
