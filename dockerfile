FROM python:3.13-slim

ENV TOKEN='Your Token'
ENV PYTHONUNBUFFERED=1

COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "bot.py"]