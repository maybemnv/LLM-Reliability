"""
Semantic Chunker Tests
"""

import pytest

from ingestion.models import Document, DocumentChunk
from ingestion.chunker import SemanticChunker


class TestDocumentChunk:
    def test_valid_chunk(self):
        chunk = DocumentChunk(
            content="Chunk content",
            source="/path/to/file.txt",
            chunk_index=0,
            token_count=10
        )
        assert chunk.content == "Chunk content"
        assert chunk.chunk_index == 0
    
    def test_chunk_with_metadata(self):
        chunk = DocumentChunk(
            content="Content",
            source="source",
            chunk_index=0,
            token_count=5,
            metadata={"key": "value"}
        )
        assert chunk.metadata["key"] == "value"


class TestSemanticChunkerInit:
    def test_default_parameters(self):
        chunker = SemanticChunker()
        assert chunker.min_chunk_tokens == 500
        assert chunker.max_chunk_tokens == 700
        assert chunker.overlap_ratio == 0.12
    
    def test_custom_parameters(self):
        chunker = SemanticChunker(min_chunk_tokens=400, max_chunk_tokens=600)
        assert chunker.min_chunk_tokens == 400
    
    def test_invalid_min_tokens(self):
        with pytest.raises(ValueError, match="must be positive"):
            SemanticChunker(min_chunk_tokens=-1)
    
    def test_min_exceeds_max(self):
        with pytest.raises(ValueError, match="cannot exceed"):
            SemanticChunker(min_chunk_tokens=800, max_chunk_tokens=500)


class TestTokenCounting:
    def test_count_tokens_empty(self):
        chunker = SemanticChunker()
        assert chunker.count_tokens("") == 0
    
    def test_count_tokens_simple(self):
        chunker = SemanticChunker()
        assert chunker.count_tokens("Hello world") > 0


class TestChunking:
    def test_chunk_empty_text(self):
        chunker = SemanticChunker()
        assert chunker.chunk_text("") == []
    
    def test_chunk_includes_source(self):
        chunker = SemanticChunker(min_chunk_tokens=1, max_chunk_tokens=1000)
        chunks = chunker.chunk_text("Content here.", source="/test/file.txt")
        assert len(chunks) > 0
        assert chunks[0].source == "/test/file.txt"
    
    def test_chunk_indexes_sequential(self):
        text = "\n\n".join([f"Paragraph {i}. " * 50 for i in range(5)])
        chunker = SemanticChunker(min_chunk_tokens=50, max_chunk_tokens=100)
        chunks = chunker.chunk_text(text)
        
        for i, chunk in enumerate(chunks):
            assert chunk.chunk_index == i


class TestChunkDocument:
    def test_chunk_document(self):
        doc = Document(
            content="This is document content. " * 100,
            source="/path/to/doc.txt",
            metadata={"file_type": ".txt"}
        )
        
        chunker = SemanticChunker(min_chunk_tokens=50, max_chunk_tokens=150)
        chunks = chunker.chunk_document(doc)
        
        assert len(chunks) > 0
        assert chunks[0].source == doc.source
