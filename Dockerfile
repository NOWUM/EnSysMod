FROM python:3.9

RUN apt-get update
RUN apt-get install -y glpk-utils python3-swiglpk

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ensysmod /code/ensysmod

EXPOSE 8080

CMD ["uvicorn", "ensysmod.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]