**Deployment**

This backend is a small Flask app that writes contact submissions to a Google Sheet.

Quick start (local):

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Place your `credentials.json` (Google service account) in the project root.

3. Run locally:

```bash
export DEBUG=1
export PORT=5000
python app.py
```

Docker (build & run):

```bash
docker build -t dongle-backend .
docker run -p 5000:5000 -v $(pwd)/credentials.json:/app/credentials.json:ro -e PORT=5000 dongle-backend
```

Heroku deploy (example):

```bash
heroku create
git push heroku main
heroku config:set DEBUG=0
```

Notes:
- The application expects `credentials.json` to exist at runtime. Do not commit it to source control.
- The WSGI entrypoint is the `app` object in `app.py` (usable by gunicorn).