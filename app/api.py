# app/api.py  ──  50 lignes, rien de sorcier
from fastapi import FastAPI, UploadFile, File, Header, HTTPException
import subprocess, os, uuid, shutil

SHARED = "/data/shared"                # déjà monté dans le conteneur
SCRIPT = f"{SHARED}/render_template.py"
API_KEY = os.getenv("API_KEY")         # même clé dans n8n
DOCX   = "bon_de_commande.docx"
PDF    = "bon_de_commande.pdf"

app = FastAPI()

def run(cmd: list[str], timeout=120):
    cp = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if cp.returncode:
        raise RuntimeError(cp.stderr or "error")
    return cp.stdout

@app.post("/convert")
async def convert(
        file: UploadFile = File(...),
        x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(401, "Bad API key")

    tmp = f"{SHARED}/bdc_{uuid.uuid4().hex}.json"
    with open(tmp, "wb") as f:
        shutil.copyfileobj(file.file, f)

    run(["python3", "-u", SCRIPT], timeout=60)
    run(["libreoffice", "--headless", "--convert-to", "pdf",
         f"{SHARED}/{DOCX}", "--outdir", SHARED], timeout=60)

    return {"docx": f"{SHARED}/{DOCX}", "pdf": f"{SHARED}/{PDF}"}
