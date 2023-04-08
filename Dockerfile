FROM python:3.10-slim

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy --ignore-pipfile

ENV file_directory="Subida Osiris"

COPY . .

CMD ["python3", "src/subida.py"]
