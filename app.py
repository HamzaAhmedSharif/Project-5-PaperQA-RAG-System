import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import tempfile
import os
import time
import torch

from rag_utils import (
    extract_text_from_pdf,
    chunk_text,
    build_faiss_index,
    embed_query,
    load_embedding_model,
    process_pdf,
    search_index,
)

st.set_page_config(page_title="PaperQA", layout="wide")
st.title("📄 PaperQA - Simple RAG (No LangChain)")

RELEVANCE_THRESHOLD = 0.3


def _get_config_value(key, default):
    """Check Streamlit secrets first, then env var, then fall back to default."""
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.environ.get(key, default)


GENERATION_MODEL_NAME = _get_config_value("PAPERQA_GENERATION_MODEL", "google/flan-t5-small")
NUM_BEAMS = int(_get_config_value("PAPERQA_NUM_BEAMS", "1"))

# Lightweight config uses flan-t5-small with bfloat16 and low_cpu_mem_usage
IS_LIGHTWEIGHT = GENERATION_MODEL_NAME == "google/flan-t5-small"


@st.cache_resource
def load_models():
    # Embedding model: use bfloat16 for lightweight config only
    if IS_LIGHTWEIGHT:
        embed_model = load_embedding_model(
            model_kwargs={"torch_dtype": torch.bfloat16, "low_cpu_mem_usage": True}
        )
    else:
        embed_model = load_embedding_model()

    tokenizer = AutoTokenizer.from_pretrained(GENERATION_MODEL_NAME)
    if IS_LIGHTWEIGHT:
        model = AutoModelForSeq2SeqLM.from_pretrained(
            GENERATION_MODEL_NAME,
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
        )
    else:
        model = AutoModelForSeq2SeqLM.from_pretrained(GENERATION_MODEL_NAME)
    model.eval()
    return embed_model, tokenizer, model


for key, default in [("index", None), ("chunks", None), ("chunk_pages", None), ("filename", None)]:
    if key not in st.session_state:
        st.session_state[key] = default

embed_model, tokenizer, model = load_models()

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is None and st.session_state.filename is not None:
    st.session_state.index = None
    st.session_state.chunks = None
    st.session_state.chunk_pages = None
    st.session_state.filename = None

if st.session_state.index is not None:
    if st.button("🔄 Clear and reprocess current document"):
        st.session_state.index = None
        st.session_state.chunks = None
        st.session_state.chunk_pages = None
        st.session_state.filename = None
        st.rerun()

if uploaded_file:
    if st.session_state.index is None or st.session_state.filename != uploaded_file.name:
        start_time = time.time()
        with st.spinner("Reading PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            try:
                try:
                    chunks, chunk_pages, index, num_pages = process_pdf(tmp_path, embed_model)
                except ValueError as e:
                    st.error(str(e))
                    st.stop()

                st.session_state.index = index
                st.session_state.chunks = chunks
                st.session_state.chunk_pages = chunk_pages
                st.session_state.filename = uploaded_file.name

            finally:
                os.unlink(tmp_path)

        elapsed = time.time() - start_time
        st.success(f"✅ Processed {num_pages} pages into {len(chunks)} chunks in {elapsed:.1f}s.")

if st.session_state.index is not None:
    question = st.text_input("Ask a question about this paper:")
    if question:
        with st.spinner("Thinking..."):
            chunks = st.session_state.chunks
            chunk_pages = st.session_state.chunk_pages
            index = st.session_state.index

            k = min(3, len(chunks))
            q_emb = embed_query(embed_model, question)
            D, I = search_index(index, q_emb, k=k)

            best_score = float(D[0][0])
            if best_score < RELEVANCE_THRESHOLD:
                st.warning(
                    "I couldn't find content in this document relevant to that question. "
                    "Try rephrasing, or confirm it's actually covered in the PDF."
                )
            else:
                context = "\n".join(chunks[i] for i in I[0])
                prompt = f"Question: {question}\nContext: {context}\nAnswer:"

                inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
                outputs = model.generate(
                    **inputs,
                    max_length=200,
                    num_beams=NUM_BEAMS,
                    repetition_penalty=1.3,
                    no_repeat_ngram_size=3,
                    early_stopping=True,
                )
                answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

                st.write("**Answer:**", answer)

                st.write("---")
                st.write("**Sources used to generate this answer:**")
                for rank, idx in enumerate(I[0]):
                    snippet = chunks[idx][:250] + "..." if len(chunks[idx]) > 250 else chunks[idx]
                    st.write(f"**Source {rank + 1}** — page {chunk_pages[idx]} (similarity: {D[0][rank]:.3f}):")
                    st.write(f"> {snippet}")
                    st.write("")
else:
    st.info("Upload a PDF above to start asking questions.")