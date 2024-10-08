#!/usr/bin/python3
import os
import subprocess
import boto3
import uuid
import requests

## Atualizar repositórios e pacotes
# sudo apt update
# sudo apt upgrade -y

## Instalar o Python e o pip
# sudo apt install python3 python3-pip -y

## Verificar a versão do Python instalada
# python3 --version

## Verificar a versão do pip instalada
# pip3 --version

# pip install boto3


# Configurações do MySQL crontab -e
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""
DB_NAME_D3Acessorios = ""
DB_NAME_ForteImoveis = ""

# Configurações da DigitalOcean Spaces
DO_SPACES_ENDPOINT = "https://nyc3.digitaloceanspaces.com"
DO_SPACES_BUCKET = "storage"
DO_ACCESS_KEY = ""
DO_SECRET_KEY = ""

# Configurações API de Email
APIEmail_Url = "https://api-send-emails.com.br/api/Email/send-informativo"
APIEmail_ApiKey = ""
APIEmail_Emails = "teste@gmail.com.br,teste1@gmail.com.br"

BACKUP_DIR = "/var/backups/dumps-mysql/"


def fazer_dump_mysql(name_backup, name_db):
    arquivo_backup = os.path.join(BACKUP_DIR, name_backup)
    comando_dump = (
        f"mysqldump --single-transaction --routines --triggers --no-tablespaces "
        f"-h {DB_HOST} -u {DB_USER} -p{DB_PASS} {name_db} > {arquivo_backup}"
    )
    subprocess.run(comando_dump, shell=True)

    return arquivo_backup


def enviar_para_digitalocean(arquivo_backup, space_folder):
    session = boto3.session.Session()

    client = session.client(
        "s3",
        endpoint_url=DO_SPACES_ENDPOINT,
        aws_access_key_id=DO_ACCESS_KEY,
        aws_secret_access_key=DO_SECRET_KEY,
    )

    nome_arquivo = os.path.basename(arquivo_backup)
    caminho_arquivo = "{}/{}".format(space_folder, nome_arquivo)
    client.upload_file(arquivo_backup, DO_SPACES_BUCKET, caminho_arquivo)

    return nome_arquivo


def remover_backup_local(arquivo_backup):
    os.remove(arquivo_backup)


def sendEmail(title, bodyJson):
    body = {"json": bodyJson, "emailTo": APIEmail_Emails, "titulo": title}

    headers = {"Content-Type": "application/json", "Dev-Senas-Key": APIEmail_ApiKey}

    # Fazendo a requisição POST
    response = requests.post(APIEmail_Url, json=body, headers=headers)

    # Verificando o status da resposta
    if response.status_code == 200:
        print("Email enviado com sucesso!")
    else:
        print(f"Erro ao enviar email: {response.text}")


def d3Acessorios():
    try:
        guid = str(uuid.uuid4())

        # Fazer o dump do banco de dados MySQL
        arquivo_backup = fazer_dump_mysql(
            f"db_d3acessorios_backup_{guid}.sql", DB_NAME_D3Acessorios
        )

        # Enviar o arquivo de backup para a DigitalOcean Spaces
        nome_arquivo = enviar_para_digitalocean(arquivo_backup, "Backups/D3_Acessorios")

        # Remover o arquivo de backup do sistema local
        remover_backup_local(arquivo_backup)

        print(
            f"Backup do banco de dados ({nome_arquivo}) realizado com sucesso e enviado para a DigitalOcean Spaces. O arquivo local foi removido."
        )

        return True, None
    except requests.exceptions.RequestException as e:
        return False, e


def main():
    body = ""

    sucessoD3, erroD3 = d3Acessorios()

    if sucessoD3:
        body = "Envio do backup do D3 Acessórios com sucesso para a DigitalOcean.\n"
    else:
        body = f"Erro ao enviar backup do D3 Acessórios para a DigitalOcean. Erro: {erroD3}\n"

    sendEmail("Backup realizado", body)


if __name__ == "__main__":
    main()
