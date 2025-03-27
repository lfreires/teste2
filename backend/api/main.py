from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from controller.chat_controller import ChatController

app = FastAPI()

# Libera o CORS para o front (Next.js em localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa a IA com todos os PDFs
controller = ChatController(pasta_documentos="documents/", pasta_data="data/faiss_metadata.pkl")

@app.get("/")
def root():
    return {"status": "ok", "mensagem": "API do Chat com PDF via FAISS"}

@app.post("/perguntar")
def perguntar(pergunta: str = Query(..., description="Pergunta feita pelo usuário")):
    resposta = controller.responder(pergunta)
    return {"pergunta": pergunta, "resposta": resposta}

"""
@app.post("/perguntar")
def perguntar(pergunta: str = Query(..., description="Pergunta feita pelo usuário")):
    return {"pergunta": pergunta, "resposta": f'A sua pergunta foi: {pergunta}'}
"""    