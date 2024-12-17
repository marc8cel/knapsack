FROM python:3.9-slim AS base

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt && \
    apt-get update && \
    apt-get -y install glpk-utils && \
    rm -rf ~/.cache/pip

FROM base AS final

COPY app.py /app/app.py
COPY main.py /app/main.py

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
