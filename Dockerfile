# Stage 1 - Preparation
FROM python:3.13.2-slim AS preparation

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt

# Stage 2 - Deploy \
FROM python:3.13.2-slim AS deploy

WORKDIR /app

COPY Final /app

COPY --from=preparation /venv /venv

ENV PATH="/venv/bin:$PATH"
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["flask", "run"]
