FROM python:3.10

COPY ./requirements.txt /project/requirements.txt
WORKDIR /project
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /project/app
WORKDIR /project/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

