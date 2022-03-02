FROM python:3.9

RUN sudo apt-get update
RUN sudo apt-get install -y coinor-cbc
RUN sudo apt-get install glpk-utils libglpk-dev glpk-doc python-glpk

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ensysmod /code/ensysmod

EXPOSE 8080

CMD ["uvicorn", "ensysmod.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]