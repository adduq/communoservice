FROM python:3.9-alpine

WORKDIR /app/

# Install Python dependencies
COPY ./requirements.txt /app/
COPY ./scripts/entrypoint.sh .

# ? Ajout ?
# RUN pip install --upgrade pip

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev jpeg-dev zlib-dev
RUN apk add mailcap
RUN pip install psycopg2-binary
RUN pip install uwsgi -I --no-cache-dir
RUN pip install -r requirements.txt

# Add the rest of the code
COPY . /app/

EXPOSE $PORT

RUN sed -i 's/\r$//g' ./entrypoint.sh && chmod +x ./entrypoint.sh

CMD ["./entrypoint.sh"]