FROM agrigorev/zoomcamp-model:mlops-3.9.7-slim

RUN pip install -U pip
RUN pip install pipenv 

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "score_hw.py", "./" ]

RUN pipenv install --system --deploy

ENTRYPOINT [ "python", "score_hw.py", "fhv", "2021", "5", "hw" ]


# docker run \
# -e AWS_ACCESS_KEY_ID="__" \
# -e AWS_SECRET_ACCESS_KEY="__" \
# mlops-zoomcamp-model-hw4:v1