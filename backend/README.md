# ChatPDF FAISS App (MVC)

Este projeto usa OpenAI + FAISS para responder perguntas com base em documentos PDF.

## Funcionalidades

- Upload de PDFs na pasta `documents/`
- Embeddings com OpenAI
- Indexação com FAISS
- API REST com FastAPI para integrar com front-end

## Como rodar

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
