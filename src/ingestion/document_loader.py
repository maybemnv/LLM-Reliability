"""
Document Loader

This module provides functionality for loading documents from various sources.
Supports text files (.txt) and basic file discovery.

Future extensions can add PDF support via PyPDF2 or pdfplumber.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any
import os


@dataclass
class DocumentChunk:
    """
    Represents a chunk of text from a document.
    
    Attributes:
        content: The text content of the chunk.
        source: Path or identifier of the source document.
        metadata: Additional metadata about the chunk.
        chunk_index: Position of this chunk within the source document.
    """
    content: str
    source: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    chunk_index: int = 0
    
    def __post_init__(self):
        """Validate chunk data after initialization."""
        if not self.content:
            raise ValueError("Chunk content cannot be empty")
        if not self.source:
            raise ValueError("Chunk source cannot be empty")


def load_text_file(
    path: str,
    encoding: str = "utf-8"
) -> Optional[DocumentChunk]:
    """
    Load a single text file and return its content as a DocumentChunk.
    
    Args:
        path: Path to the text file.
        encoding: File encoding (default: utf-8).
        
    Returns:
        DocumentChunk containing the file content, or None if loading fails.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        
    Examples:
        >>> chunk = load_text_file("data/sample.txt")
        >>> print(chunk.content[:100])
    """
    file_path = Path(path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {path}")
    
    try:
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()
        
        if not content.strip():
            return None
        
        return DocumentChunk(
            content=content,
            source=str(file_path.absolute()),
            metadata={
                "filename": file_path.name,
                "extension": file_path.suffix,
                "size_bytes": file_path.stat().st_size
            },
            chunk_index=0
        )
    except UnicodeDecodeError:
        # Try alternative encoding
        try:
            with open(file_path, "r", encoding="latin-1") as f:
                content = f.read()
            
            if not content.strip():
                return None
            
            return DocumentChunk(
                content=content,
                source=str(file_path.absolute()),
                metadata={
                    "filename": file_path.name,
                    "extension": file_path.suffix,
                    "size_bytes": file_path.stat().st_size,
                    "encoding_fallback": "latin-1"
                },
                chunk_index=0
            )
        except Exception:
            return None
    except Exception:
        return None


def load_directory(
    path: str,
    extensions: Optional[List[str]] = None,
    recursive: bool = False
) -> List[DocumentChunk]:
    """
    Load all documents from a directory.
    
    Args:
        path: Path to the directory.
        extensions: List of file extensions to include (e.g., [".txt", ".md"]).
                   If None, defaults to [".txt"].
        recursive: Whether to search subdirectories.
        
    Returns:
        List of DocumentChunks from all loaded files.
        
    Examples:
        >>> chunks = load_directory("data/knowledge_base", extensions=[".txt"])
        >>> print(f"Loaded {len(chunks)} documents")
    """
    dir_path = Path(path)
    
    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")
    
    if not dir_path.is_dir():
        raise ValueError(f"Path is not a directory: {path}")
    
    if extensions is None:
        extensions = [".txt"]
    
    # Normalize extensions to lowercase with leading dot
    extensions = [
        ext if ext.startswith(".") else f".{ext}"
        for ext in extensions
    ]
    extensions = [ext.lower() for ext in extensions]
    
    documents: List[DocumentChunk] = []
    
    # Collect files
    if recursive:
        files = [
            f for f in dir_path.rglob("*")
            if f.is_file() and f.suffix.lower() in extensions
        ]
    else:
        files = [
            f for f in dir_path.iterdir()
            if f.is_file() and f.suffix.lower() in extensions
        ]
    
    # Sort for deterministic ordering
    files = sorted(files, key=lambda x: x.name)
    
    # Load each file
    for file_path in files:
        try:
            chunk = load_text_file(str(file_path))
            if chunk is not None:
                documents.append(chunk)
        except Exception:
            # Skip files that fail to load
            continue
    
    return documents


def get_file_stats(path: str) -> Dict[str, Any]:
    """
    Get statistics about files in a directory.
    
    Args:
        path: Path to the directory.
        
    Returns:
        Dictionary with file statistics.
    """
    dir_path = Path(path)
    
    if not dir_path.exists() or not dir_path.is_dir():
        return {"error": "Invalid directory path"}
    
    stats: Dict[str, Any] = {
        "total_files": 0,
        "total_size_bytes": 0,
        "extensions": {}
    }
    
    for file_path in dir_path.rglob("*"):
        if file_path.is_file():
            stats["total_files"] += 1
            stats["total_size_bytes"] += file_path.stat().st_size
            
            ext = file_path.suffix.lower()
            if ext not in stats["extensions"]:
                stats["extensions"][ext] = 0
            stats["extensions"][ext] += 1
    
    return stats
