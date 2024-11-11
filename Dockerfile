# Usa uma imagem base do Python
FROM python:3.9

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo de dependências para o contêiner
COPY requirements.txt requirements.txt

# Instala as dependências do Python
RUN pip install -r requirements.txt

# Copia o código da aplicação para o contêiner
COPY . .

# Expõe a porta 5000 para a aplicação Flask
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]
