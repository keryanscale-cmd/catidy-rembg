FROM python:3.11-slim

WORKDIR /app

# Dépendances système pour rembg
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pré-télécharger le modèle u2net au build (évite le téléchargement au runtime)
RUN python -c "from rembg import remove; from PIL import Image; import io; \
    img = Image.new('RGB', (10,10), color='white'); \
    buf = io.BytesIO(); img.save(buf, format='PNG'); \
    remove(Image.open(io.BytesIO(buf.getvalue())))"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
