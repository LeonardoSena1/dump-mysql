# Script de Backup e Upload para DigitalOcean Spaces

Este script em Python faz backup de bancos de dados MySQL, envia os arquivos de backup para o DigitalOcean Spaces e envia um e-mail com as informações sobre o processo.

## Funcionalidades

1. Faz o **dump** de um banco de dados MySQL especificado.
2. Envia o arquivo de backup para o **DigitalOcean Spaces**.
3. Remove o arquivo de backup do sistema local após o envio.
4. Envia um e-mail informativo com o status da operação via uma **API de E-mail**.

## Requisitos

- **Python 3.x** instalado.
- **MySQL** instalado e configurado.
- Conexão com o serviço **DigitalOcean Spaces**.
- Uma **API de e-mail** configurada para envio de notificações.

### Dependências

As bibliotecas Python necessárias para executar o script são:

- **boto3**: Para integração com o DigitalOcean Spaces.
- **requests**: Para enviar as requisições à API de e-mail.

Instale as dependências executando o comando:

```bash
pip install boto3 requests

```

## Configurações

Antes de executar o script, você deve configurar as variáveis de ambiente no código:

- **DB_HOST = "localhost"**
- **DB_USER = "root"**
- **DB_PASS = "sua_senha"**
- **DB_NAME_D3Acessorios = "nome_do_banco_d3acessorios"**
- **DB_NAME_ForteImoveis = "nome_do_banco_forteimoveis"**


## Configurações da DigitalOcean Spaces

- **DO_SPACES_ENDPOINT = "https://nyc3.digitaloceanspaces.com"**
- **DO_SPACES_BUCKET = "nome_do_bucket"**
- **DO_ACCESS_KEY = "sua_access_key"**
- **DO_SECRET_KEY = "sua_secret_key"**


## Configurações da API de E-mail

- **APIEmail_Url = "https://api-send-emails.com.br/api/Email/send-informativo"**
- **APIEmail_ApiKey = "sua_chave_api"**
- **APIEmail_Emails = "email1@gmail.com,email2@gmail.com"**


## Diretório de Backup

Defina o diretório onde os arquivos de backup serão temporariamente armazenados antes de serem enviados:

- **BACKUP_DIR = "/var/backups/dumps-mysql/"**

### Como Usar

- **Clone ou copie o script para o seu ambiente.**
- **Configure as variáveis descritas acima com as informações do seu ambiente.**
- **Execute o script para realizar o backup e enviá-lo para o DigitalOcean Spaces.**
```bash
python3 dump.py
```



Esse `README.md` fornece informações claras sobre as funcionalidades, configurações, dependências e uso do script Python para backup e upload.
