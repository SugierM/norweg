FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Problem with psycopg2 and git? --- maybe binary version was enough to investigate 
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/* 

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download nb_core_news_md

COPY app/ ./app/
COPY img/ ./img/
COPY norw_dictionaries/ ./norw_dictionaries/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]