FROM continuumio/miniconda3:4.9.2

WORKDIR /code

COPY ./requirements.yml /code/requirements.yml

RUN conda env create -f /code/requirements.yml

# Make RUN commands use the new environment:
# SHELL ["conda", "run", "-n", "EnSysMod-env", "/bin/bash", "-c"]

COPY ./ensysmod /code/ensysmod

EXPOSE 8080

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "EnSysMod-env", "uvicorn", "ensysmod.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]