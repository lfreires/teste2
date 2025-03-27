import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region = os.getenv("AWS_REGION")
bucket_name = "chatbothackaton2025"

s3 = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)

def sincronizar_bidirecional_s3(chave_s3, caminho_local, bucket=bucket_name):
    try:
        obj_s3 = s3.head_object(Bucket=bucket, Key=chave_s3)
        tamanho_s3 = obj_s3["ContentLength"]
        existe_s3 = True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            existe_s3 = False
            tamanho_s3 = -1
        else:
            raise e

    existe_local = os.path.exists(caminho_local)
    tamanho_local = os.path.getsize(caminho_local) if existe_local else -1

    if existe_s3 and existe_local:
        if tamanho_local == tamanho_s3:
            print(f"✅ '{caminho_local}' já sincronizado com S3.")
        elif tamanho_local > tamanho_s3:
            print("Local é maior → Enviando para o S3...")
            s3.upload_file(caminho_local, bucket, chave_s3)
        else:
            print("S3 é maior → Baixando para local...")
            s3.download_file(bucket, chave_s3, caminho_local)

    elif existe_local and not existe_s3:
        print("Enviando arquivo novo para o S3...")
        s3.upload_file(caminho_local, bucket, chave_s3)

    elif existe_s3 and not existe_local:
        print("Baixando arquivo que só existe no S3...")
        s3.download_file(bucket, chave_s3, caminho_local)

    else:
        print("Arquivo não existe localmente nem no S3.")

def sincronizar_pasta_com_s3(pasta_local, prefixo_s3, bucket="chatbothackaton2025"):
    s3 = boto3.client("s3")

    # 1. Lista arquivos locais
    arquivos_locais = {
        nome: os.path.join(pasta_local, nome)
        for nome in os.listdir(pasta_local)
        if os.path.isfile(os.path.join(pasta_local, nome))
    }

    # 2. Lista arquivos no S3 com aquele prefixo
    objetos_s3 = s3.list_objects_v2(Bucket=bucket, Prefix=prefixo_s3)
    arquivos_s3 = {}

    for obj in objetos_s3.get("Contents", []):
        key = obj["Key"]
        nome_arquivo = key.replace(prefixo_s3, "")
    
        # Ignora "pastas" vazias
        if nome_arquivo == "" or key.endswith("/") or obj["Size"] == 0:
            continue
        
        arquivos_s3[nome_arquivo] = obj["Size"]


    # 3. Comparar e sincronizar
    for nome, caminho_local in arquivos_locais.items():
        chave_s3 = prefixo_s3 + nome
        tamanho_local = os.path.getsize(caminho_local)

        if nome in arquivos_s3:
            tamanho_s3 = arquivos_s3[nome]

            if tamanho_local == tamanho_s3:
                print(f"✅ {nome} já está sincronizado.")
            elif tamanho_local > tamanho_s3:
                print(f"📤 {nome} local é mais recente → enviando...")
                s3.upload_file(caminho_local, bucket, chave_s3)
            else:
                print(f"📥 {nome} do S3 é mais recente → baixando...")
                s3.download_file(bucket, chave_s3, caminho_local)
        else:
            print(f"📤 {nome} só existe localmente → enviando para S3...")
            s3.upload_file(caminho_local, bucket, chave_s3)

    # 4. Baixar arquivos que existem no S3 mas não estão localmente
    for nome in arquivos_s3:
        if nome not in arquivos_locais:
            print(f"📥 {nome} só existe no S3 → baixando para local...")
            caminho_local = os.path.join(pasta_local, nome)
            chave_s3 = prefixo_s3 + nome
            s3.download_file(bucket, chave_s3, caminho_local)

