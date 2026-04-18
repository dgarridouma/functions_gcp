# Deployment on GCP — Blob trigger

Gen2 Cloud Function with a GCS trigger: it activates when a file is uploaded to a bucket, processes it, and saves the result to another bucket.

---

## Step 1 — Enable APIs

```
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable eventarc.googleapis.com
gcloud services enable pubsub.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

---

## Step 2 — Create the buckets

```
gsutil mb -l europe-west1 gs://mipath
gsutil mb -l europe-west1 gs://mipath-output
```

Bucket names are global in GCP. If `mipath` already exists in another project it will fail — use a more specific name.

---

## Step 3 — Permissions for the GCS trigger

The trigger works through Eventarc, which uses Pub/Sub internally to receive GCS notifications. The GCS service account needs the `pubsub.publisher` role or the deployment will fail.

Get the project number:

```
gcloud projects describe YOUR_PROJECT_ID --format="value(projectNumber)"
```

Assign the permission replacing `PROJECT_NUMBER`:

```
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID --member="serviceAccount:service-PROJECT_NUMBER@gs-project-accounts.iam.gserviceaccount.com" --role="roles/pubsub.publisher"
```

---

## Step 4 — Deploy the Cloud Function

From the `function` folder:

```
gcloud functions deploy blob_trigger --gen2 --region=europe-west1 --runtime=python311 --entry-point=blob_trigger --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" --trigger-event-filters="bucket=mypath" --source=. --memory=256MB
```

`finalized` triggers the function when the file has been fully uploaded, not during the upload.

---

## Step 5 — Test

```
gcloud storage cp test.txt gs://miruta/test.txt
```

Check that the result appears:

```
gcloud storage ls gs://miruta-output/
```

View logs:

```
gcloud functions logs read blob_trigger --region=europe-west1 --gen2
```

---

## Cleanup

```
gcloud functions delete blob_trigger --region=europe-west1 --gen2
gsutil rm -r gs://miruta
gsutil rm -r gs://miruta-output
```
