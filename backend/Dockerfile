FROM python:3.9-alpine

WORKDIR /app/

# Install Python dependencies
COPY ./requirements.txt /app/
COPY ./scripts/entrypoint.sh .

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev
RUN pip install psycopg2-binary
RUN pip install uwsgi
RUN pip install -r requirements.txt

# Add the rest of the code
COPY . /app/

EXPOSE $PORT


ENV SECRET_KEY='test'
RUN python manage.py collectstatic --noinput

ENV UWSGI_HTTP=:$PORT UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# Number of uWSGI workers and threads per worker (customize as needed):
ENV UWSGI_WORKERS=2 UWSGI_THREADS=4

# uWSGI static file serving configuration (customize or comment out if not needed):
ENV UWSGI_STATIC_MAP="/static/=/app/static/" UWSGI_STATIC_EXPIRES_URI="/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000"

# Deny invalid hosts before they get to Django (uncomment and change to your hostname(s)):
# ENV UWSGI_ROUTE_HOST="^(?!localhost:8000$) break:400"

# Change to a non-root user
# USER ${APP_USER}:${APP_USER}

# Uncomment after creating your docker-entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Start uWSGI
CMD ["uwsgi", "--show-config"]

# RUN sed -i 's/\r$//g' ./entrypoint.sh && chmod +x ./entrypoint.sh

# CMD ["./entrypoint.sh"]