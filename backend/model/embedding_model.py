import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
client = OpenAI()
openai_api_key = os.getenv("OPENAI_API_KEY")

def gerar_embeddings_com_metadados(chunks, origem_pdf, hash_pdf):
    embeddings = []
    metadados = []


    for i, chunk in enumerate(chunks):
        print(f"🔹 Gerando embedding do chunk {i+1}/{len(chunks)}")
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )
        embedding = response.data[0].embedding
        embeddings.append(embedding)
        metadados.append({
            "origem": origem_pdf,
            "id_documento": hash_pdf,
            "texto": chunk,
            "index_chunk": i
        })

    return embeddings, metadados


def gerar_embedding_pergunta(pergunta):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=pergunta
    )
    return response.data[0].embedding

def top_n_similares(pergunta, embeddings_chunks, chunks_texto, top_n=3):
    emb_pergunta = np.array(gerar_embedding_pergunta(pergunta)).reshape(1, -1)
    emb_chunks = np.array(embeddings_chunks)

    similaridades = cosine_similarity(emb_pergunta, emb_chunks)[0]
    indices_top = np.argsort(similaridades)[::-1][:top_n]

    resultados = []
    for idx in indices_top:
        resultados.append({
            "similaridade": similaridades[idx],
            "texto": chunks_texto[idx]
        })
    return resultados

def responder_com_chatgpt(pergunta, trechos, historico=[]):
    from pprint import pprint  # opcional: só pra debug
    contexto = "\n\n".join([f"- {t['texto']}" for t in trechos])

    system_msg = {
        "role": "system",
        "content": (
            "Você é um assistente virtual simpático chamado Sinap 😊.\n\n"
            "Responda de forma clara, acolhedora e útil, como se estivesse conversando com uma pessoa de verdade.\n"
            "Você tem acesso ao histórico da conversa nesta sessão, e pode usá-lo para responder perguntas como 'o que você disse antes?'.\n"
            "Se a pergunta estiver fora de contexto ou não for clara, oriente o usuário com gentileza.\n"
            "Nunca mencione que você é um modelo de linguagem, nem fale que está usando contexto fornecido.\n"
            "Se o usuário parecer satisfeito (ex: 'legal', 'boa', 'valeu'), apenas agradeça de forma simpática, sem insistir em continuar a conversa.\n"
        )
    }

    mensagens = [system_msg]

    # Adiciona o histórico (intercalando user/assistant)
    for msg in historico:
        mensagens.append({"role": "user", "content": msg["pergunta"]})
        mensagens.append({"role": "assistant", "content": msg["resposta"]})

    # Adiciona o contexto como uma system message separada (pra não bagunçar o histórico)
    if contexto.strip():
        mensagens.append({
            "role": "system",
            "content": f"📚 Contexto de apoio:\n{contexto}"
        })

    # Pergunta atual
    mensagens.append({"role": "user", "content": pergunta})

    # 🔍 Debug opcional (ver se o chat está montando corretamente)
    # from pprint import pprint
    # pprint(mensagens)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=mensagens,
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

