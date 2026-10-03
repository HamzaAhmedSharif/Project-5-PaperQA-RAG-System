import re
import faiss
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer


BGE_QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF, returning list of (page_num, text) tuples."""
    reader = PdfReader(pdf_path)
    if reader.is_encrypted:
        raise ValueError("PDF is password-protected")
    pages_text = [(i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)]
    return pages_text


def chunk_text(pages_text, chunk_size=500, overlap_sentences=2):
    """
    Chunk text with sentence overlap, tracking page numbers.
    Returns (chunks, chunk_pages) where chunk_pages[i] is the page number of the first sentence in chunks[i].
    """
    sentence_page_pairs = []
    for page_num, text in pages_text:
        if not text.strip():
            continue
        for sent in re.split(r'(?<=[.!?])\s+', text):
            if sent.strip():
                sentence_page_pairs.append((page_num, sent))

    chunks, chunk_pages = [], []
    current = []
    current_len = 0
    for page_num, sent in sentence_page_pairs:
        current.append((page_num, sent))
        current_len += len(sent)
        if current_len >= chunk_size:
            chunks.append(" ".join(s for _, s in current))
            chunk_pages.append(current[0][0])
            current = current[-overlap_sentences:] if len(current) > overlap_sentences else current[:]
            current_len = sum(len(s) for _, s in current)
    if current:
        chunks.append(" ".join(s for _, s in current))
        chunk_pages.append(current[0][0])
    return chunks, chunk_pages


def build_faiss_index(chunks, embed_model):
    """Build FAISS IndexFlatIP index from text chunks using the given embedding model."""
    embeddings = embed_model.encode(chunks, normalize_embeddings=True).astype('float32')
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index, embeddings


def embed_query(embed_model, query):
    """Embed a query with BGE query instruction prefix and normalization."""
    instructed_query = BGE_QUERY_INSTRUCTION + query
    q_emb = embed_model.encode([instructed_query], normalize_embeddings=True).astype('float32')
    return q_emb


def search_index(index, query_embedding, k=3):
    """Search FAISS index, return (distances, indices)."""
    D, I = index.search(query_embedding, k=k)
    return D, I


def load_embedding_model(model_kwargs=None):
    """Load the BGE embedding model."""
    if model_kwargs is None:
        model_kwargs = {}
    return SentenceTransformer(EMBEDDING_MODEL_NAME, model_kwargs=model_kwargs)


def process_pdf(pdf_path, embed_model, chunk_size=500, overlap_sentences=2):
    """
    Full pipeline: extract -> chunk -> embed -> index.
    Returns (chunks, chunk_pages, index, num_pages).
    """
    pages_text = extract_text_from_pdf(pdf_path)
    full_text = " ".join(t for _, t in pages_text)
    if not full_text.strip():
        raise ValueError("No text could be extracted from PDF")
    chunks, chunk_pages = chunk_text(pages_text, chunk_size, overlap_sentences)
    index, _ = build_faiss_index(chunks, embed_model)
    return chunks, chunk_pages, index, len(pages_text)