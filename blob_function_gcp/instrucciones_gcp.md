# Despliegue en GCP — Blob trigger

Cloud Function gen2 con trigger de GCS: se activa al subir un fichero a un bucket, lo procesa y guarda el resultado en otro bucket.

---

## Paso 1 — Habilitar APIs

```
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable eventarc.googleapis.com
gcloud services enable pubsub.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

---

## Paso 2 — Crear los buckets

```
gsutil mb -l europe-west1 gs://miruta
gsutil mb -l europe-west1 gs://miruta-output
```

Los nombres de bucket son globales en GCP. Si `miruta` ya existe en otro proyecto fallará, usa un nombre más específico.

---

## Paso 3 — Permisos para el trigger de GCS

El trigger funciona a través de Eventarc, que usa Pub/Sub internamente para recibir notificaciones de GCS. La cuenta de servicio de GCS necesita el rol `pubsub.publisher` o el despliegue falla.

Obtén el project number:

```
gcloud projects describe YOUR_PROJECT_ID --format="value(projectNumber)"
```

Asigna el permiso sustituyendo `NUMERO_PROYECTO`:

```
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID --member="serviceAccount:service-NUMERO_PROYECTO@gs-project-accounts.iam.gserviceaccount.com" --role="roles/pubsub.publisher"
```

---

## Paso 4 — Desplegar la Cloud Function

Desde la carpeta `function`:

```
gcloud functions deploy blob_trigger --gen2 --region=europe-west1 --runtime=python311 --entry-point=blob_trigger --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" --trigger-event-filters="bucket=miruta" --source=. --memory=256MB
```

`finalized` activa la función cuando el fichero se ha subido completamente, no durante la subida.

---

## Paso 5 — Probar

```
gcloud storage cp prueba.txt gs://miruta/prueba.txt
```

Comprobar que aparece el resultado:

```
gcloud storage ls gs://miruta-output/
```

Ver logs:

```
gcloud functions logs read blob_trigger --region=europe-west1 --gen2
```

---

## Limpieza

```
gcloud functions delete blob_trigger --region=europe-west1 --gen2
gsutil rm -r gs://miruta
gsutil rm -r gs://miruta-output
```
