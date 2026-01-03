"""
Document Loader Tests
"""

import pytest
import tempfile
from pathlib import Path

from ingestion.models import Document
from ingestion.loaders import (
    load_txt,
    load_document,
    load_documents_from_directory
)


class TestDocument:
    def test_valid_document(self):
        doc = Document(content="Test content", source="/path/to/file.txt")
        assert doc.content == "Test content"
        assert doc.source == "/path/to/file.txt"
    
    def test_document_with_metadata(self):
        doc = Document(
            content="Test content",
            source="/path/to/file.txt",
            metadata={"file_type": ".txt", "size": 100}
        )
        assert doc.metadata["file_type"] == ".txt"
    
    def test_empty_content_raises(self):
        with pytest.raises(ValueError, match="content cannot be empty"):
            Document(content="", source="/path/to/file.txt")
    
    def test_empty_source_raises(self):
        with pytest.raises(ValueError, match="source cannot be empty"):
            Document(content="Some content", source="")


class TestLoadTxt:
    def test_load_valid_txt_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Hello, World!")
            temp_path = f.name
        
        try:
            content = load_txt(temp_path)
            assert content == "Hello, World!"
        finally:
            Path(temp_path).unlink()
    
    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            load_txt("/nonexistent/path/file.txt")


class TestLoadDocument:
    def test_load_txt_document(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Document content")
            temp_path = f.name
        
        try:
            doc = load_document(temp_path)
            assert doc.content == "Document content"
            assert doc.metadata["file_type"] == ".txt"
        finally:
            Path(temp_path).unlink()
    
    def test_unsupported_format(self):
        with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as f:
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError, match="Unsupported"):
                load_document(temp_path)
        finally:
            Path(temp_path).unlink()


class TestLoadDocumentsFromDirectory:
    def test_load_multiple_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            for i in range(3):
                (Path(temp_dir) / f"doc{i}.txt").write_text(f"Content {i}")
            
            docs = load_documents_from_directory(temp_dir)
            assert len(docs) == 3
    
    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            docs = load_documents_from_directory(temp_dir)
            assert docs == []
