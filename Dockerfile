# Usar uma imagem oficial do Python como imagem base
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

RUN apt-get update -y && apt-get install -y ssh fzf

COPY requirements.txt .
RUN pip install --root-user-action=ignore --upgrade pip && pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Copia o script Python para o diretório de trabalho atual dentro do contêiner
COPY async_lista_macs_extreme.py .

# Define o comando padrão para executar o script
# O ENTRYPOINT permite que você passe argumentos adicionais ao comando docker run
ENTRYPOINT ["python", "async_lista_macs_extreme.py"]
# ENTRYPOINT ["python", "--version"]
