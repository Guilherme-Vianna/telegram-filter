FROM python:3.13-slim

# Instala curl (necessário pro uv)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Instala uv
RUN curl -Ls https://astral.sh/uv/install.sh | sh

# Adiciona uv ao PATH
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copia apenas pyproject primeiro (melhora cache)
COPY pyproject.toml ./

# Instala dependências
RUN uv sync

# Copia o resto do projeto
COPY . .

CMD ["uv", "run", "python", "main.py"]
