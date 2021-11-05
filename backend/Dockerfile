FROM python:3.9-alpine

WORKDIR /app/

# Install Python dependencies
COPY ./requirements.txt /app/
# COPY ./scripts/entrypoint.sh .

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev
RUN pip install psycopg2-binary
RUN pip install uwsgi
RUN pip install -r requirements.txt

# Add the rest of the code
COPY . /app/

EXPOSE $PORT


RUN python3 manage.py collectstatic --no-input

CMD ["uwsgi", '--http 0.0.0.0:$PORT', '--module config.wsgi:application', '--master', '--processes 4', '--threads 2']

# RUN sed -i 's/\r$//g' ./entrypoint.sh && chmod +x ./entrypoint.sh

# CMD ["./entrypoint.sh"]