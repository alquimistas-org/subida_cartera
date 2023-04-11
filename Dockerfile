FROM python:3.10-slim

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy --ignore-pipfile

COPY . .

CMD ["python3", "src/subida.py"]
