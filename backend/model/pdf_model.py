import fitz  # PyMuPDF
import tiktoken
import pytesseract
from PIL import Image
import io
import tiktoken

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extrair_texto_pdf(caminho_pdf):
    doc = fitz.open(caminho_pdf)
    texto = ""

    for pagina in doc:
        conteudo = pagina.get_text().strip()
        if conteudo:
            texto += conteudo + "\n"
        else:
            print("🔍 Página sem texto detectado — aplicando OCR...")

            # Converte a página para imagem
            pix = pagina.get_pixmap(dpi=300)
            imagem = Image.open(io.BytesIO(pix.tobytes("png")))

            # Faz OCR com pytesseract
            ocr_texto = pytesseract.image_to_string(imagem, lang='por')  # ou 'eng'
            texto += ocr_texto + "\n"

    return texto.strip()


def dividir_em_chunks(texto, max_tokens=500):
    tokenizer = tiktoken.encoding_for_model("text-embedding-3-small")
    if '\n' in texto:
        palavras = texto.split()
    else:
        palavras = texto
    chunks = []
    chunk = []

    for palavra in palavras:
        chunk.append(palavra)
        tokens = len(tokenizer.encode(" ".join(chunk)))
        if tokens >= max_tokens:
            chunks.append(" ".join(chunk))
            chunk = []
    if chunk:
        chunks.append(" ".join(chunk))
    return chunks
