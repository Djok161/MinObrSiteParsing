FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


RUN pip install huggingface-hub
RUN python -c 'from huggingface_hub import HfFolder; HfFolder.save_token("${HF_API_KEY}")'

CMD uvicorn main:app --host 0.0.0.0 --port 1111