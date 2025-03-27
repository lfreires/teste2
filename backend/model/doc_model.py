import re

def extrair_texto(texto):
    texto = re.sub(r'[ \t]+', ' ', texto)  # substitui espaços e tabs em excesso
    paragrafos = segmentar_por_paragrafos(texto, delimitador="\n")
    return paragrafos  # ou ' '.join(paragrafos) se quiser uma string

def segmentar_por_paragrafos(texto, delimitador="\n"):
    return [p.strip() for p in texto.split(delimitador) if len(p.strip()) > 0]
