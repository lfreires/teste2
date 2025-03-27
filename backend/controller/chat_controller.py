from model.mp3_transformer import extract_audio_from_video
from controller.utils import buscar_pdfs_em_diretorio, save_transcription_to_txt, buscar_not_pdfs_em_diretorio, buscar_videos_em_diretorio, gerar_hash, carregar_txt, carregar_docx, carregar_doc
from services.s3_services import sincronizar_bidirecional_s3, sincronizar_pasta_com_s3
from model.pdf_model import extrair_texto_pdf, dividir_em_chunks
from model.doc_model import extrair_texto
from model.embedding_model import (
    gerar_embeddings_com_metadados,
    gerar_embedding_pergunta,
    responder_com_chatgpt
)
from model.faiss_index import FaissIndex
from model.conversation_memory import ConversadorTemporario
from model.audio_transcriber import transcribe_audio
import os

class ChatController:
    def __init__(self, pasta_documentos="documents/", pasta_data="data/faiss_metadata.pkl"):
        self.pasta_documentos = pasta_documentos
        self.pasta_data = pasta_data

        self.conversador = ConversadorTemporario(limite=5)
        
        # Sincroniza com o S3
        self._sincronizar()
        # Inicializa o índice FAISS
        self.faiss_index = FaissIndex()
        # Indexa PDFs
        self._indexar_pdfs()
        # Indexa arquivos não-PDF
        self._indexar_outros_documentos()

        self._indexar_arquivos_video()

    def _sincronizar(self):
        sincronizar_bidirecional_s3(self.pasta_data, self.pasta_data)
        sincronizar_pasta_com_s3(self.pasta_documentos, self.pasta_documentos)

    def _indexar_pdfs(self):
        caminhos = buscar_pdfs_em_diretorio(self.pasta_documentos)

        for caminho in caminhos:
            hash_doc = gerar_hash(caminho)

            if self.faiss_index.documento_ja_indexado(hash_doc):
                print(f"⚠️ Documento já indexado: {caminho}")
                continue

            print(f"📄 Indexando novo PDF: {caminho}")
            texto = extrair_texto_pdf(caminho)
            self._processar_documento(texto, caminho, hash_doc)

    def _indexar_arquivos_video(self):
        caminhos = buscar_videos_em_diretorio(self.pasta_documentos)

        for caminho in caminhos:
            hash_doc = gerar_hash(caminho)

            if self.faiss_index.documento_ja_indexado(hash_doc):
                print(f"⚠️ Documento já indexado: {caminho}")
                continue

            print(f"📄 Indexando novo documento: {caminho}")

            audio_video = extract_audio_from_video(caminho, self.pasta_documentos)
            transcricao = transcribe_audio(audio_video)

            arquivo_texto_path = os.path.splitext(audio_video)[0] + ".txt"
            arquivo_texto = save_transcription_to_txt(transcricao, arquivo_texto_path)

            texto = self._extrair_texto_generico(arquivo_texto_path)
            self._processar_documento(texto, caminho, hash_doc)

    def _indexar_outros_documentos(self):
        caminhos = buscar_not_pdfs_em_diretorio(self.pasta_documentos)

        for caminho in caminhos:
            hash_doc = gerar_hash(caminho)

            if self.faiss_index.documento_ja_indexado(hash_doc):
                print(f"⚠️ Documento já indexado: {caminho}")
                continue

            print(f"📄 Indexando novo documento: {caminho}")
            texto = self._extrair_texto_generico(caminho)
            self._processar_documento(texto, caminho, hash_doc)

    def _extrair_texto_generico(self, caminho):
        if caminho.endswith(".txt"):
            return carregar_txt(caminho)
        elif caminho.endswith(".docx"):
            return carregar_docx(caminho)
        elif caminho.endswith(".doc"):
            return carregar_doc(caminho)
        else:
            print(f"⚠️ Tipo de arquivo não suportado: {caminho}")
            return ""

    def _processar_documento(self, texto_bruto, caminho, hash_doc):
        texto = extrair_texto(texto_bruto) if not caminho.endswith(".pdf") else texto_bruto
        chunks = dividir_em_chunks(texto)
        embeddings, metadados = gerar_embeddings_com_metadados(chunks, caminho, hash_doc)
        self.faiss_index.adicionar(embeddings, metadados)


    def responder(self, pergunta):
        emb_pergunta = gerar_embedding_pergunta(pergunta)
        similares = self.faiss_index.buscar_similares(emb_pergunta, top_k=3)

        trechos = [{"texto": s["metadado"]["texto"], "similaridade": 1 - s["distancia"]} for s in similares]
        
        historico = self.conversador.obter()
        resposta = responder_com_chatgpt(pergunta, trechos, historico)
        self.conversador.adicionar(pergunta, resposta)

        return resposta
