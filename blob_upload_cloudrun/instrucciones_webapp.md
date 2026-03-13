# Despliegue webapp Flask en Cloud Run

Webapp que permite subir ficheros .txt a GCS y descargar el resultado procesado por la Cloud Function.

---

## Prerequisitos

Buckets `miruta` y `miruta-output` creados y Cloud Function desplegada.

---

## Despliegue

Desde la carpeta `webapp`:

```
gcloud run deploy webapp-indexador --source=. --region=europe-west1 --platform=managed --allow-unauthenticated --port=8080
```

Con `--source=.` GCP construye la imagen automáticamente sin necesidad de Dockerfile. Al terminar devuelve la URL pública del servicio.

---

## Limpieza

```
gcloud run services delete webapp-indexador --region=europe-west1
```
