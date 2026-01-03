"""
Vector Store Tests
"""

import pytest
import tempfile
from pathlib import Path

from retrieval.store import FAISSVectorStore
from retrieval.service import retrieve_documents
from ingestion.models import DocumentChunk
from embeddings.bge_embedder import BGEEmbedder


@pytest.fixture(scope="module")
def embedder():
    return BGEEmbedder()


@pytest.fixture
def sample_chunks():
    return [
        DocumentChunk(
            content="Air pollution causes respiratory diseases.",
            source="health_doc.txt",
            chunk_index=0,
            token_count=10
        ),
        DocumentChunk(
            content="Climate change leads to rising sea levels.",
            source="climate_doc.txt",
            chunk_index=0,
            token_count=12
        ),
        DocumentChunk(
            content="Renewable energy includes solar and wind power.",
            source="energy_doc.txt",
            chunk_index=0,
            token_count=11
        ),
    ]


class TestFAISSVectorStoreInit:
    def test_init_default_embedder(self):
        store = FAISSVectorStore()
        assert store.embedder is not None
        assert store.dimension > 0
    
    def test_empty_by_default(self, embedder):
        store = FAISSVectorStore(embedder=embedder)
        assert store.is_empty
        assert store.size == 0


class TestAddChunks:
    def test_add_chunks(self, embedder, sample_chunks):
        store = FAISSVectorStore(embedder=embedder)
        store.add_chunks(sample_chunks)
        assert store.size == len(sample_chunks)
    
    def test_add_empty_list(self, embedder):
        store = FAISSVectorStore(embedder=embedder)
        store.add_chunks([])
        assert store.is_empty


class TestSearch:
    def test_search_returns_list(self, embedder, sample_chunks):
        store = FAISSVectorStore(embedder=embedder)
        store.build_index(sample_chunks)
        results = store.search("air pollution health")
        assert isinstance(results, list)
    
    def test_search_result_structure(self, embedder, sample_chunks):
        store = FAISSVectorStore(embedder=embedder)
        store.build_index(sample_chunks)
        results = store.search("health effects")
        
        for r in results:
            assert "content" in r
            assert "source" in r
            assert "relevance_score" in r
    
    def test_search_relevance_range(self, embedder, sample_chunks):
        store = FAISSVectorStore(embedder=embedder)
        store.build_index(sample_chunks)
        results = store.search("climate change")
        
        for r in results:
            assert 0 <= r["relevance_score"] <= 1
    
    def test_search_empty_query(self, embedder, sample_chunks):
        store = FAISSVectorStore(embedder=embedder)
        store.build_index(sample_chunks)
        assert store.search("") == []
    
    def test_search_empty_store(self, embedder):
        store = FAISSVectorStore(embedder=embedder)
        assert store.search("any query") == []


class TestPersistence:
    def test_save_and_load(self, embedder, sample_chunks):
        with tempfile.TemporaryDirectory() as temp_dir:
            store1 = FAISSVectorStore(embedder=embedder)
            store1.build_index(sample_chunks)
            store1.save_index(temp_dir)
            
            store2 = FAISSVectorStore(embedder=embedder, index_path=temp_dir)
            assert store2.size == store1.size
    
    def test_save_creates_files(self, embedder, sample_chunks):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FAISSVectorStore(embedder=embedder)
            store.build_index(sample_chunks)
            store.save_index(temp_dir)
            
            assert (Path(temp_dir) / "faiss_index.bin").exists()
            assert (Path(temp_dir) / "chunks_metadata.json").exists()


class TestRetrieveDocuments:
    def test_retrieve_returns_list(self):
        results = retrieve_documents("test query")
        assert isinstance(results, list)
    
    def test_retrieve_empty_query(self):
        assert retrieve_documents("") == []
