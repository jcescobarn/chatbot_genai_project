from typing import List
from pathlib import Path

import fitz 
import docx
import os

def load_txt(file_path: Path) -> str:

    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def load_pdf(file_path: Path) -> str:

    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def load_docx(file_path: Path) -> str:

    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def load_file(file_path: str) -> str:
 
    ext = Path(file_path).suffix.lower()
    if ext == '.txt':
        return load_txt(file_path)
    elif ext == '.pdf':
        return load_pdf(file_path)
    elif ext == '.docx':
        return load_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")