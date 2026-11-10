# Web Development and AI Projects

Three assignment-ready applications:

1. React + Express + MongoDB registration/login.
2. PDF RAG chatbot using Python, Streamlit and Google Gemini.
3. Website summarizer using Python, Streamlit, BeautifulSoup and Google Gemini.

## Requirements
- Node.js 18+
- Python 3.10+
- MongoDB Atlas or local MongoDB
- Gemini API key: https://aistudio.google.com/app/apikey

## 1. Login and Registration
Backend:
```bash
cd 01-authentication/backend
npm install
```
Copy `.env.example` to `.env`, set `MONGO_URI` and a long random `JWT_SECRET`, then run `npm run dev`.

In another terminal:
```bash
cd 01-authentication/frontend
npm install
npm run dev
```
Open the Vite URL. Register first, then log in with the same credentials.

## 2. PDF RAG Chatbot
```bash
cd 02-pdf-rag
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```
Copy `.env.example` to `.env`, add `GEMINI_API_KEY`, then run `streamlit run app.py`. Upload a text-based PDF, process it, and ask questions. Relevant text chunks are retrieved before Gemini generates an answer.

## 3. Website Summarizer
```bash
cd 03-website-summarizer
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```
Copy `.env.example` to `.env`, add `GEMINI_API_KEY`, then run `streamlit run app.py`. Enter a public URL such as `https://example.com`.

## Security
Never commit `.env` files, API keys, database passwords, or JWT secrets. `.env.example` files contain placeholders. Passwords are hashed with bcrypt. Website pages that require JavaScript or block automated requests may not be extractable.
