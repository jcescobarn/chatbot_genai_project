from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import tempfile

from models.rag_engine import rag_engine  

router = APIRouter()

@router.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    valid_exts = (".pdf", ".docx", ".txt")
    if not file.filename.lower().endswith(valid_exts):
        raise HTTPException(status_code=400, detail="Tipo de archivo no soportado.")

    try:
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        chunks_stored = rag_engine.ingest_document(tmp_path, source_name=file.filename)

        return {"message": f"{file.filename} ingresado exitosamente con {chunks_stored} chunks."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar archivo: {str(e)}")

    finally:
        if Path(tmp_path).exists():
            Path(tmp_path).unlink()
