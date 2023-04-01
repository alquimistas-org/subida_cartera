FROM python:3.10-slim

WORKDIR /app

COPY requeriments.txt requirements.txt

RUN pip install --no-cache -r requirements.txt

COPY . .

CMD ["python3", "src/subida.py"]
