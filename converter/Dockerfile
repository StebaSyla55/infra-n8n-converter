FROM debian:12-slim
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /data/shared

# ─── 1) Systèmes + LaTeX complet pour pandoc ───────────────────────────────
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
    libreoffice-core \
    libreoffice-writer \
    default-jre-headless \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# ─── 2) CLI JavaScript & Python-Docx-Template ───────────────────────────────
RUN npm install -g docxtemplater-cli@latest \
 && pip3 install --no-cache-dir --break-system-packages docxtpl \
 && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["tail","-f","/dev/null"]
