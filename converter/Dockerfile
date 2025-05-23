##############################################################################
# Image  : converter (DOCX templating  +  PDF LibreOffice)                   #
# Usage  : appelé en interne par n8n via POST http://converter:8000/convert  #
##############################################################################

FROM debian:12-slim
ENV DEBIAN_FRONTEND=noninteractive

# ─── 1) Dépendances système ────────────────────────────────────────────────
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        mupdf-tools \
        pandoc \
        ghostscript \
        curl \
        ca-certificates \
        nodejs npm \
        python3-pip python3-bs4 python3-lxml \
        libxml2 libxslt1.1 \
        libreoffice-core libreoffice-writer \
        default-jre-headless \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# ─── 2) Outils CLI & bibliothèques Python ──────────────────────────────────
RUN npm install -g docxtemplater-cli@latest \
 && pip3 install --no-cache-dir --break-system-packages \
        docxtpl \
        fastapi \
        "uvicorn[standard]" \
        python-multipart \
 && rm -rf /var/lib/apt/lists/*

# ─── 3) Code API FastAPI ───────────────────────────────────────────────────
# Le dossier "app" contient app/api.py (l’endpoint /convert)
COPY app /app

# ─── 4) Volume partagé avec n8n ────────────────────────────────────────────
#   - /data/shared contient : render_template.py, templates DOCX,
#     JSON généré par n8n, fichiers de sortie DOCX/PDF
VOLUME ["/data/shared"]

# ─── 5) Lancement du service ───────────────────────────────────────────────
WORKDIR /app
EXPOSE 8000
CMD CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

