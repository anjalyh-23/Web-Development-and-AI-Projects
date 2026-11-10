import os
from urllib.parse import urlparse
import requests
import streamlit as st
from google import genai
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Website Summarizer", page_icon="🌐")
st.title("🌐 Website Summarizer")
st.write("Enter a public website address to extract its content and generate a summary.")
key = os.getenv("GEMINI_API_KEY")
if not key:
    st.error("Add GEMINI_API_KEY to your .env file (see .env.example).")
    st.stop()
client = genai.Client(api_key=key)
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

def normalize(value):
    value = value.strip()
    if not value.startswith(("http://", "https://")):
        value = "https://" + value
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Enter a valid website URL.")
    return value

def read_site(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 StudentWebsiteSummarizer/1.0"}, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "svg"]):
        tag.decompose()
    title = soup.title.get_text(" ", strip=True) if soup.title else url
    text = " ".join(soup.get_text(" ", strip=True).split())
    return title, text[:18000]

url = st.text_input("Website name or URL", placeholder="abc.com")
if st.button("Summarize Website", type="primary"):
    if not url.strip():
        st.warning("Enter a website address.")
    else:
        try:
            target = normalize(url)
            with st.spinner("Fetching website content..."):
                title, content = read_site(target)
            if len(content) < 100:
                st.warning("Not enough readable text found. The site may require JavaScript or block automated access.")
            else:
                prompt = f"""Summarize this webpage for a student. Provide (1) a short overview, (2) main points as bullets, and (3) important services or concepts. Use only the supplied webpage text; do not guess.
Title: {title}
URL: {target}
Page text: {content}"""
                with st.spinner("Generating summary..."):
                    result = client.models.generate_content(model=MODEL, contents=prompt)
                st.subheader(title)
                st.caption(target)
                st.markdown(result.text)
                with st.expander("Show extracted page text"):
                    st.write(content)
        except requests.RequestException as error:
            st.error(f"Could not access website: {error}")
        except Exception as error:
            st.error(f"Could not summarize: {error}")
