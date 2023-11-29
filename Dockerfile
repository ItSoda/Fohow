FROM python:3.10

SHELL [ "/bin/bash", "-c"]

RUN pip install --upgrade pip

RUN useradd -rms /bin/bash fohow && chmod 777 /opt /run

WORKDIR /fohow

RUN mkdir /fohow/static && mkdir /fohow/media && chown -R fohow:fohow /fohow && chmod 777 /fohow

COPY --chown=fohow:fohow . .

COPY pyproject.toml poetry.lock /fohow/

RUN apt-get update && apt-get install -y wget \
    && wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz \
    && rm dockerize-linux-amd64-v0.6.1.tar.gz

RUN wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.tgz \
    && tar -xzf ngrok-stable-linux-amd64.tgz \
    && mv ngrok /usr/local/bin/ \
    && rm ngrok-stable-linux-amd64.tgz

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi