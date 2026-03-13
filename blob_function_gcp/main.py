from collections import Counter
from google.cloud import storage
import functions_framework
import logging

INPUT_BUCKET  = "miruta"
OUTPUT_BUCKET = "miruta-output"

@functions_framework.cloud_event
def blob_trigger(cloud_event):
    """
    Se activa automáticamente cuando llega un fichero al bucket INPUT_BUCKET.
    Equivalente al blob_trigger de Azure Functions.
    """
    data      = cloud_event.data
    blob_name = data["name"]

    logging.info(f"Fichero recibido: {blob_name} ({data.get('size', '?')} bytes)")

    # Procesar solo archivos .txt
    if not blob_name.lower().endswith(".txt"):
        logging.info(f"Ignorando archivo no .txt: {blob_name}")
        return

    try:
        client = storage.Client()

        # Leer contenido del fichero de entrada
        input_bucket = client.bucket(INPUT_BUCKET)
        blob         = input_bucket.blob(blob_name)
        text         = blob.download_as_text(encoding="utf-8")

        # Crear índice de palabras (mismo procesamiento que en Azure)
        words        = text.lower().split()
        counts       = Counter(words)
        output_lines = [f"{word}: {count}" for word, count in sorted(counts.items())]
        index_text   = "\n".join(output_lines)

        # Nombre del fichero de salida
        output_name = f"{blob_name}_indexado.txt"

        # Escribir en el bucket de salida
        output_bucket = client.bucket(OUTPUT_BUCKET)

        # Crear bucket si no existe
        if not output_bucket.exists():
            client.create_bucket(OUTPUT_BUCKET)
            logging.info(f"Bucket '{OUTPUT_BUCKET}' creado.")

        output_blob = output_bucket.blob(output_name)
        output_blob.upload_from_string(index_text, content_type="text/plain")

        logging.info(f"Índice guardado en: {OUTPUT_BUCKET}/{output_name}")

    except Exception as e:
        logging.error(f"Error procesando {blob_name}: {e}")
        raise
