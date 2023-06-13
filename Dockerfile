FROM python:3.10-slim

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --dev --system

ENV DEBUG="0"

ENV WEB_APP_PATH="/web-app"

ENV SENTRY_DSN=${SENTRY_DSN}

COPY . .

EXPOSE 8050

CMD ["python", "web-app/main.py"]
