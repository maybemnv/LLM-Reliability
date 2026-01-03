"""
Document Loaders

Functions for loading documents from various file formats.
Single responsibility: file I/O operations only.
"""

from pathlib import Path
from typing import List, Optional

from ingestion.models import Document

try:
    from PyPDF2 import PdfReader
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


def load_txt(file_path: str, encoding: str = "utf-8") -> str:
    """
    Load content from a plain text file.
    
    Args:
        file_path: Path to the text file.
        encoding: Text encoding (default: utf-8).
        
    Returns:
        The text content of the file.
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    with open(path, "r", encoding=encoding) as f:
        return f.read()


def load_pdf(file_path: str) -> str:
    """
    Load and extract text content from a PDF file.
    
    Args:
        file_path: Path to the PDF file.
        
    Returns:
        The extracted text content from all pages.
    """
    if not PDF_AVAILABLE:
        raise ImportError(
            "PyPDF2 is required for PDF loading. "
            "Install with: pip install PyPDF2"
        )
    
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    try:
        reader = PdfReader(file_path)
        pages_text: List[str] = []
        
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                pages_text.append(page_text)
        
        return "\n\n".join(pages_text)
    
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {file_path}. Error: {e}")


def load_document(file_path: str) -> Document:
    """
    Load a document from file, automatically detecting format.
    
    Args:
        file_path: Path to the document file.
        
    Returns:
        Document object with content and metadata.
    """
    path = Path(file_path)
    extension = path.suffix.lower()
    
    if extension == ".txt":
        content = load_txt(file_path)
    elif extension == ".pdf":
        content = load_pdf(file_path)
    else:
        raise ValueError(
            f"Unsupported file format: {extension}. "
            "Supported formats: .txt, .pdf"
        )
    
    metadata = {
        "file_type": extension,
        "file_name": path.name,
        "file_size_bytes": path.stat().st_size
    }
    
    return Document(
        content=content,
        source=str(path.absolute()),
        metadata=metadata
    )


def load_documents_from_directory(
    directory_path: str,
    extensions: Optional[List[str]] = None,
    recursive: bool = False
) -> List[Document]:
    """
    Load all documents from a directory.
    
    Args:
        directory_path: Path to the directory containing documents.
        extensions: File extensions to include (default: [".txt", ".pdf"]).
        recursive: If True, search subdirectories recursively.
        
    Returns:
        List of Document objects for all valid files found.
    """
    if extensions is None:
        extensions = [".txt", ".pdf"]
    
    extensions = [
        ext if ext.startswith(".") else f".{ext}"
        for ext in extensions
    ]
    extensions = [ext.lower() for ext in extensions]
    
    directory = Path(directory_path)
    
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory_path}")
    
    if not directory.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {directory_path}")
    
    documents: List[Document] = []
    
    if recursive:
        file_iterator = directory.rglob("*")
    else:
        file_iterator = directory.glob("*")
    
    for file_path in file_iterator:
        if file_path.is_file() and file_path.suffix.lower() in extensions:
            try:
                doc = load_document(str(file_path))
                documents.append(doc)
            except (ValueError, IOError) as e:
                print(f"Warning: Skipping {file_path}: {e}")
    
    return documents
