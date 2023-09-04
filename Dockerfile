# Use a imagem base oficial do Python
FROM python:3.8

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o conteúdo do diretório local para o contêiner
COPY . /app

# Instale as dependências do projeto
RUN pip install -r requirements.txt

# Rodar o programa assim que executar a imagem
CMD ["python", "src/main.py"]