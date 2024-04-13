FROM python:3.10

SHELL [ "/bin/bash", "-c"]

EXPOSE 8000

RUN pip install --upgrade pip

RUN useradd -rms /bin/bash fohow && chmod 777 /opt /run

WORKDIR /fohow

RUN mkdir /fohow/static && mkdir /fohow/media && chown -R fohow:fohow /fohow && chmod 777 /fohow

COPY --chown=fohow:fohow . .

COPY pyproject.toml poetry.lock /fohow/

RUN apt-get update

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi