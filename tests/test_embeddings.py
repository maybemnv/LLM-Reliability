"""
BGE Embedder Tests
"""

import pytest
import numpy as np

from embeddings.bge_embedder import BGEEmbedder


@pytest.fixture(scope="module")
def embedder():
    return BGEEmbedder()


class TestBGEEmbedderInit:
    def test_default_model(self, embedder):
        assert "bge" in embedder.model_name.lower()
    
    def test_dimension(self, embedder):
        assert embedder.dimension == 768


class TestSingleEmbedding:
    def test_embed_returns_array(self, embedder):
        result = embedder.embed("Test text")
        assert isinstance(result, np.ndarray)
    
    def test_embed_correct_dimension(self, embedder):
        result = embedder.embed("Test text")
        assert result.shape == (embedder.dimension,)
    
    def test_embed_normalized(self, embedder):
        result = embedder.embed("Test text", normalize=True)
        assert abs(np.linalg.norm(result) - 1.0) < 0.01
    
    def test_embed_empty_raises(self, embedder):
        with pytest.raises(ValueError, match="empty"):
            embedder.embed("")
    
    def test_embed_deterministic(self, embedder):
        text = "Consistent text"
        r1 = embedder.embed(text)
        r2 = embedder.embed(text)
        np.testing.assert_array_almost_equal(r1, r2)


class TestBatchEmbedding:
    def test_batch_returns_2d_array(self, embedder):
        texts = ["Text one", "Text two", "Text three"]
        result = embedder.embed_batch(texts)
        assert result.ndim == 2
    
    def test_batch_correct_shape(self, embedder):
        texts = ["Text one", "Text two"]
        result = embedder.embed_batch(texts)
        assert result.shape == (2, embedder.dimension)
    
    def test_batch_empty_list(self, embedder):
        result = embedder.embed_batch([])
        assert result.shape == (0, embedder.dimension)


class TestQueryEmbedding:
    def test_query_returns_array(self, embedder):
        result = embedder.embed_query("Search query")
        assert isinstance(result, np.ndarray)
    
    def test_query_differs_from_document(self, embedder):
        text = "Same text content"
        query_emb = embedder.embed_query(text)
        doc_emb = embedder.embed(text)
        assert not np.allclose(query_emb, doc_emb)
    
    def test_query_empty_raises(self, embedder):
        with pytest.raises(ValueError, match="empty"):
            embedder.embed_query("")


class TestSimilarity:
    def test_similarity_identical(self, embedder):
        emb = embedder.embed("Test text", normalize=True)
        sim = embedder.similarity(emb, emb)
        assert abs(sim - 1.0) < 0.01
    
    def test_similar_texts_high_score(self, embedder):
        e1 = embedder.embed("Air pollution health effects", normalize=True)
        e2 = embedder.embed("Health impacts of air pollution", normalize=True)
        assert embedder.similarity(e1, e2) > 0.8
