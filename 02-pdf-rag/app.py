import os
import streamlit as st
from google import genai
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="PDF RAG Assistant", page_icon="📚")
st.title("📚 Ask Your PDF")
st.write("Upload a PDF and ask questions. This demo retrieves relevant text chunks before generating an answer.")
key = os.getenv("GEMINI_API_KEY")
if not key:
    st.error("Add GEMINI_API_KEY to your .env file (see .env.example).")
    st.stop()
client = genai.Client(api_key=key)
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

def chunks_from(text, size=850, overlap=120):
    words = text.split()
    step = size - overlap
    return [" ".join(words[i:i + size]) for i in range(0, len(words), step)]

def retrieve(question, chunks, k=4):
    terms = {w.lower().strip(".,!?;:()") for w in question.split() if len(w) > 2}
    ranked = []
    for chunk in chunks:
        words = {w.lower().strip(".,!?;:()") for w in chunk.split()}
        score = len(terms & words)
        if score:
            ranked.append((score, chunk))
    ranked.sort(reverse=True, key=lambda item: item[0])
    return [chunk for _, chunk in ranked[:k]] or chunks[:k]

pdf = st.file_uploader("Choose a PDF", type="pdf")
if pdf and st.button("Process PDF"):
    reader = PdfReader(pdf)
    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    if not extracted.strip():
        st.error("No selectable text found. Scanned PDFs need OCR first.")
    else:
        st.session_state.chunks = chunks_from(extracted)
        st.session_state.docname = pdf.name
        st.success(f"Processed {len(reader.pages)} pages into {len(st.session_state.chunks)} chunks.")

if "chunks" in st.session_state:
    st.caption("Document: " + st.session_state.docname)
    question = st.text_input("Ask a question about your PDF")
    if st.button("Generate answer") and question.strip():
        passages = retrieve(question, st.session_state.chunks)
        context = "\n\n---\n\n".join(passages)
        prompt = f"Answer using only this context. If the answer is absent, say so. Do not invent facts.\n\nCONTEXT:\n{context}\n\nQUESTION: {question}"
        with st.spinner("Retrieving passages and generating answer..."):
            try:
                answer = client.models.generate_content(model=MODEL, contents=prompt)
                st.subheader("Answer")
                st.write(answer.text)
                with st.expander("View retrieved passages"):
                    for index, passage in enumerate(passages, 1):
                        st.markdown(f"**Passage {index}**\n\n{passage}")
            except Exception as error:
                st.error(str(error))
