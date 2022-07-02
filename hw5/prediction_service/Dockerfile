FROM python:3.9.7-slim

RUN pip install -U pip

WORKDIR /app

COPY [ "requirements.txt", "app.py", "lin_reg.bin", "./" ]

RUN pip install -r requirements.txt

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "app:app" ]