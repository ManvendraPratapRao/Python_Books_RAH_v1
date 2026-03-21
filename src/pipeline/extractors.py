import os
import fitz  # PyMuPDF
import ebooklib
from ebooklib import epub
import mobi
from bs4 import BeautifulSoup

def extract_pdf(file_path: str) -> str:
    """Extracts text from a PDF file."""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def extract_epub(file_path: str) -> str:
    """Extracts text from an EPUB file."""
    book = epub.read_epub(file_path)
    text = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            item_text = soup.get_text(separator="\n", strip=True)
            if item_text:
                text.append(item_text)
    return "\n".join(text)

def extract_mobi(file_path: str) -> str:
    """Extracts text from a MOBI file."""
    tempdir, filepath = mobi.extract(file_path)
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text(separator="\n", strip=True)
        # Preliminary cleaning: remove excessive newlines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return "\n".join(lines)
    finally:
        # Cleanup can be added here if needed, mobi extraction usually creates temp files
        pass

def get_extractor_for_file(filename: str):
    """Returns the appropriate extractor function based on file extension."""
    ext = os.path.splitext(filename)[1].lower()
    if ext == '.pdf':
        return extract_pdf
    elif ext == '.epub':
        return extract_epub
    elif ext == '.mobi':
        return extract_mobi
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
