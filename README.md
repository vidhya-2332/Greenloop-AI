# GreenLoop AI — Local Waste-to-Value Assistant

GreenLoop AI is a Flask application for household waste guidance and community sustainability demonstrations. It validates uploaded image files, lets users select or receive a clearly labelled keyword suggestion for one of five waste streams, displays bilingual English and Tamil project guides, and records user-entered completed activities in SQLite.

It does **not** identify materials from image pixels, verify that an upcycling activity occurred, or calculate carbon savings.

## Objectives and users

- Help households, students, and workshop participants find practical reuse and disposal guidance.
- Present the same instructions in English and Tamil.
- Encourage safer reuse decisions and track user-entered completed projects.

## Features

- Image upload with extension, actual image format, integrity, 32 MB, and 60-megapixel checks; accepted photos are resized for analysis.
- Five material categories: Plastic Waste, Paper & Cardboard, Glass Bottles & Jars, Metal Cans & Tins, and Organic & Kitchen Waste.
- English and Tamil category descriptions and curated guides with materials, steps, safety notes, points, and disposal advice.
- Manual category choice always takes precedence. Description and filename keyword matches are explicitly identified as heuristics. Generic filenames remain unknown and prompt manual choice.
- Activity logging awards the selected curated project's points on completion; a recent identical submission is rejected. Dashboard figures come from stored records and recalculate after deletion.
- Responsive templates, image preview, Tamil/English guide switch, and activity dashboard.

## Architecture and workflow

1. `app.py` validates requests and uploaded files, then selects a category only from explicit user choice or transparent text keywords.
2. Pillow verifies image format and integrity and creates a resized preview. It does not inspect the contents to identify the material.
3. `waste_data.py` supplies category-specific bilingual guidance; the result page displays only the selected category's guides.
4. `database.py` stores completed activity records in SQLite and calculates dashboard counts, points, and milestones.
5. `templates/`, `static/css/`, and `static/js/` provide the interface.

The `/analyze` route first uses a local waste-trained MobileNetV2 ONNX model to suggest can/metal, glass, organic, paper, and plastic streams. It was trained on public waste image datasets, runs offline, and remains an educational suggestion rather than an authoritative sorting decision. Model card, preprocessing, limitations, and CC BY 4.0 attribution: [iAny waste model](https://huggingface.co/sengtha/iany-waste-v1). If these model files are missing, the app falls back to the legacy ImageNet model and then labelled keyword suggestions or manual selection. The model is most useful for a single, centered item in a clear, well-lit image; tiny, blank, or ambiguous images may remain unknown. The model files are in `models/waste_mobilenetv2.onnx` and `models/waste_mobilenetv2_labels.txt`.

## Categories and guide safety

All five category records are keyed by stable IDs (`plastic`, `paper`, `glass`, `metal`, `organic`). Category guides include bilingual materials and steps, difficulty, points, safety notes, and responsible-disposal advice. Persistence / decomposition values are estimates only; local conditions and item composition change them. Follow local municipal recycling rules. Do not reuse damaged glass or containers that held hazardous chemicals. Use caution around cut metal and sharp edges. Compost guidance excludes unsuitable items and should be followed with care.

## Requirements

- Python 3.11 or newer for local use (the current project environment is Python 3.14.3).
- Flask 3.1, Pillow 11 or 12, NumPy 2, and ONNX Runtime 1.x for local runtime. Gunicorn 23 is isolated in `requirements-production.txt` because it serves the Linux deployment, not the Windows development server.
- No paid API, model download, or external inference service is used by the application.

## Install and run on Windows

Open PowerShell in the project directory:

```powershell
cd D:\GreenLoop-AI
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
$env:GREENLOOP_SECRET_KEY = [guid]::NewGuid().ToString('N')
python app.py
```

If using the existing Python 3.14 environment, activate it with `venv\Scripts\Activate.ps1` and install `requirements.txt` there. The key command above sets a local per-shell secret; the app also generates an ephemeral random key if none is set. `.env.example` is a reference for configuring environment variables and is not loaded automatically. The app defaults to `http://127.0.0.1:5000`.

## Automated tests

Tests isolate both the database and uploads under temporary directories; running them does not reset or insert test rows into your real `data/greenloop.db`.

```powershell
.\.venv\Scripts\Activate.ps1
python -m unittest -v test_app.py
python -m py_compile app.py ai_classifier.py database.py waste_data.py test_app.py
```

## Data and security

- `GREENLOOP_DB_PATH` selects the SQLite file. Default: `data/greenloop.db`.
- `GREENLOOP_UPLOAD_FOLDER` selects image storage. Default: `static/uploads/` in the project (the deployed configuration uses a data volume).
- `GREENLOOP_SECRET_KEY` configures Flask sessions; never commit `.env` or a real secret. `.env.example` contains placeholders only; export variables in your shell or enter them in the hosting provider's environment settings.
- `GREENLOOP_HTTPS=1` enables secure session cookies when HTTPS terminates at the host.
- Set `GREENLOOP_PORT` to choose a local port other than 5000 when an older app instance is still running.
- Uploads are limited to PNG/JPEG/WEBP, 32 MB, and 60 megapixels. Accepted photos are resized to at most 1200 pixels per side for storage and analysis. Upload names are sanitized and randomized. Uploaded photos are served from the configured upload directory.
- Browser cross-site state-changing requests are rejected when marked cross-site or when their `Origin` does not match the host.
- Activity data is user-entered and not independently verified. The local database and uploaded photos may contain private data; keep them out of version control and restrict access to the deployed app accordingly.

## Production deployment: Render

The repository contains `render.yaml`, `.python-version`, `Procfile`, and `requirements-production.txt`. The Blueprint installs the production requirements and defines a Python web service using Gunicorn and a 1 GB persistent disk mounted at `/var/data`; SQLite and uploads are configured to live on that disk. A disk-backed Render service requires a paid service plan and is limited to one instance. Render's default filesystem is ephemeral, so without the configured disk changes can disappear on deploy/restart. See [Render Flask deployment](https://render.com/docs/deploy-flask), [Python versions](https://render.com/docs/python-version), and [persistent disk behavior](https://render.com/docs/disks).

To deploy, first publish the repository yourself, then create a Render Blueprint from it and review the plan/cost and disk settings before creating the service. `render.yaml` generates a secret key. Confirm the service's environment has `GREENLOOP_SECRET_KEY`, `GREENLOOP_DB_PATH=/var/data/greenloop.db`, `GREENLOOP_UPLOAD_FOLDER=/var/data/uploads`, and `GREENLOOP_HTTPS=1`. Do not use an ephemeral instance for persistent activity or upload data. No deployment has been performed or live-tested by this project preparation.

## Known limitations and future improvements

- The waste-specific MobileNet model predicts supported waste streams, but can still be wrong; manual confirmation remains recommended.
- The waste-specific model asset is licensed CC BY 4.0; retain the source and attribution when redistributing it. The legacy ImageNet model remains as an optional fallback.
- The app is a single-user demonstration without accounts or access control. Public deployments should be restricted or extended with authentication, privacy controls, and a production database before collecting sensitive records.
- Category advice and persistence estimates are general educational guidance; verify local recycling rules and review DIY instructions for the actual item.

