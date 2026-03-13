# GCP Cloud Functions Examples

A collection of practical Python examples for learning how to develop serverless functions on Google Cloud Platform. Each folder is an independent project that can be deployed and run on its own.

---

## Repository Structure

```
functions_gcp/
├── hello_function_gcp/         # Basic HTTP function: hello world
├── blob_function_gcp/          # Function triggered by Cloud Storage events
├── blob_upload_cloudrun/       # File upload to Cloud Storage via a web interface (Cloud Run)
└── parkings_function_gcp/      # HTTP function that queries parking data
```

---

## Prerequisites

- [Python 3.9+](https://www.python.org/)
- [Google Cloud SDK (gcloud CLI)](https://cloud.google.com/sdk/docs/install)
- A [Google Cloud account](https://cloud.google.com/free) with a project created
- Billing enabled on your GCP project (required to deploy functions)

---

## Examples

### `hello_function_gcp`

A basic HTTP-triggered Cloud Function that returns a greeting on GET or POST requests. A good starting point to verify that the local environment and GCP project are set up correctly.

**Trigger:** HTTP

**Deploy:**
```bash
cd hello_function_gcp
gcloud functions deploy hello_function_gcp \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated
```

---

### `blob_function_gcp`

A function that is automatically triggered when a file is uploaded to a **Google Cloud Storage** bucket. Processes the object data received in the event.

**Trigger:** Cloud Storage

See the deployment instructions inside the `blob_function_gcp/` folder.

---

### `blob_upload_cloudrun`

A small web application (HTML + Python) deployed on **Cloud Run** that allows uploading files to a Cloud Storage bucket through a browser interface.

**Runtime:** Cloud Run  
**Key concepts:** file upload, Cloud Storage integration, CORS, containerized deployment

See the deployment instructions inside the `blob_upload_cloudrun/` folder.

---

### `parkings_function_gcp`

An HTTP-triggered Cloud Function that queries and returns real-time parking data from an open data API. A practical example of consuming an external API from a Cloud Function.

**Trigger:** HTTP

**Deploy:**
```bash
cd parkings_function_gcp
gcloud functions deploy parkings_function_gcp \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated
```

---

## Running an Example Locally

Cloud Functions can be tested locally using the [Functions Framework for Python](https://github.com/GoogleCloudPlatform/functions-framework-python):

1. Navigate to the example folder:
   ```bash
   cd <example_folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install functions-framework
   ```

3. Start the local server:
   ```bash
   functions-framework --target <FUNCTION_NAME>
   ```

4. Send a test request:
   ```bash
   curl http://localhost:8080
   ```

> For Cloud Storage-triggered functions, use the `--signature-type event` flag when starting the framework locally.

---

## Managing Credentials

Never hardcode credentials in your source code. The recommended approaches for each environment are:

- **Local development:** use [Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials) by running `gcloud auth application-default login`
- **Cloud Functions / Cloud Run:** assign the appropriate IAM roles to the service account used by the function
- **Environment variables:** set sensitive values (bucket names, project IDs) via the `--set-env-vars` flag on deployment or through the GCP Console

---

## Resources

- [Cloud Functions documentation](https://cloud.google.com/functions/docs)
- [Cloud Functions Python runtime](https://cloud.google.com/functions/docs/concepts/python-runtime)
- [Cloud Run documentation](https://cloud.google.com/run/docs)
- [Cloud Storage triggers](https://cloud.google.com/functions/docs/calling/cloud-storage)
- [Functions Framework for Python](https://github.com/GoogleCloudPlatform/functions-framework-python)
- [GCP IAM and credentials](https://cloud.google.com/iam/docs)

---

## Author

**dgarridouma** · [GitHub](https://github.com/dgarridouma)
