from flask import Flask, request, render_template, redirect, url_for, flash, Response
from google.cloud import storage
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'secret'

INPUT_BUCKET  = "miruta"
OUTPUT_BUCKET = "miruta-output"

client = storage.Client()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename.endswith('.txt'):
            flash("Por favor selecciona un archivo .txt válido.")
            return redirect(request.url)
        try:
            bucket = client.bucket(INPUT_BUCKET)
            blob   = bucket.blob(file.filename)
            blob.upload_from_file(file, content_type="text/plain")
            return redirect(url_for('resultado', filename=file.filename))
        except Exception as e:
            flash(f"Error al subir: {str(e)}")
            return redirect(request.url)

    return render_template('upload.html')


@app.route('/resultado/<filename>')
def resultado(filename):
    result_blob_name = filename.replace('.txt', '.txt_indexado.txt')
    result_blob      = client.bucket(OUTPUT_BUCKET).blob(result_blob_name)

    if not result_blob.exists():
        return render_template('resultado.html', listo=False)

    return render_template('resultado.html', listo=True, filename=result_blob_name)


@app.route('/descargar/<filename>')
def descargar(filename):
    blob    = client.bucket(OUTPUT_BUCKET).blob(filename)
    content = blob.download_as_text()
    return Response(
        content,
        mimetype="text/plain",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)