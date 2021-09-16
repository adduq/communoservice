FROM python:3.9

RUN adduser communoservice
USER communoservice

# python envs
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# python dependencies
COPY ./requirements.txt /
RUN pip install -r ./requirements.txt

# upload scripts
COPY --chown=communoservice:communoservice ./scripts/entrypoint.sh ./scripts/start.sh ./scripts/gunicorn.sh /tmp/

# Fix windows docker bug, convert CRLF to LF
RUN sed -i 's/\r$//g' /tmp/start.sh && chmod +x /tmp/start.sh &&\
    sed -i 's/\r$//g' /tmp/entrypoint.sh && chmod +x /tmp/entrypoint.sh &&\
    sed -i 's/\r$//g' /tmp/gunicorn.sh && chmod +x /tmp/gunicorn.sh

WORKDIR /app

ENTRYPOINT ["/tmp/entrypoint.sh"]