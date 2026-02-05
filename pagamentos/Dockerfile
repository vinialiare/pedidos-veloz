FROM python:3.12-slim

# Evita geração de .pyc e garante logs imediatos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cria grupo e usuário não-root
RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /app

# Copia dependências primeiro para melhor uso de cache
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY app.py .

# Ajusta permissões do diretório de trabalho
RUN chown -R app:app /app

USER app

EXPOSE 5000

CMD ["python", "app.py"]
