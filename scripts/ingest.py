"""
Document Ingestion Script

CLI tool for processing documents into the FAISS vector store.

Usage:
    python scripts/ingest.py
    python scripts/ingest.py --input Data/knowledge_base --output Data/vector_store
"""

import argparse
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ingestion import load_documents_from_directory, SemanticChunker
from embeddings import BGEEmbedder
from retrieval.store import FAISSVectorStore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest documents into vector store")
    parser.add_argument("--input", "-i", default="Data/knowledge_base", help="Input directory")
    parser.add_argument("--output", "-o", default="Data/vector_store", help="Output directory")
    parser.add_argument("--recursive", "-r", action="store_true", help="Search recursively")
    parser.add_argument("--min-tokens", type=int, default=500, help="Min tokens per chunk")
    parser.add_argument("--max-tokens", type=int, default=700, help="Max tokens per chunk")
    parser.add_argument("--overlap", type=float, default=0.12, help="Overlap ratio")
    parser.add_argument("--batch-size", type=int, default=32, help="Embedding batch size")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    return parser.parse_args()


def main():
    args = parse_args()
    
    print("=" * 60)
    print("Document Ingestion Pipeline")
    print("=" * 60)
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"Error: Input directory not found: {input_path}")
        sys.exit(1)
    
    # Load documents
    print(f"\n[1/4] Loading documents from: {input_path}")
    start = time.time()
    documents = load_documents_from_directory(str(input_path), recursive=args.recursive)
    
    if not documents:
        print("Error: No documents found")
        sys.exit(1)
    
    print(f"    Loaded {len(documents)} document(s) in {time.time()-start:.2f}s")
    
    # Chunk documents
    print(f"\n[2/4] Chunking documents...")
    start = time.time()
    chunker = SemanticChunker(
        min_chunk_tokens=args.min_tokens,
        max_chunk_tokens=args.max_tokens,
        overlap_ratio=args.overlap
    )
    
    all_chunks = []
    for doc in documents:
        chunks = chunker.chunk_document(doc)
        all_chunks.extend(chunks)
        if args.verbose:
            print(f"    {Path(doc.source).name}: {len(chunks)} chunks")
    
    print(f"    Created {len(all_chunks)} chunk(s) in {time.time()-start:.2f}s")
    
    # Generate embeddings
    print(f"\n[3/4] Generating embeddings...")
    start = time.time()
    embedder = BGEEmbedder()
    print(f"    Model: {embedder.model_name}")
    
    vector_store = FAISSVectorStore(embedder=embedder)
    vector_store.build_index(all_chunks, batch_size=args.batch_size, show_progress=args.verbose)
    
    print(f"    Generated {vector_store.size} embeddings in {time.time()-start:.2f}s")
    
    # Save index
    print(f"\n[4/4] Saving index to: {output_path}")
    start = time.time()
    vector_store.save_index(str(output_path))
    print(f"    Index saved in {time.time()-start:.2f}s")
    
    print("\n" + "=" * 60)
    print("Ingestion Complete!")
    print(f"    Documents: {len(documents)} | Chunks: {len(all_chunks)} | Vectors: {vector_store.size}")
    print("=" * 60)


if __name__ == "__main__":
    main()
