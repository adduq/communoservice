FROM python:3.9-alpine

ARG APP_USER=communoservice
RUN addgroup -S ${APP_USER} && adduser -S ${APP_USER} -G ${APP_USER}

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


ENV SECRET_KEY='test'
RUN python manage.py collectstatic --noinput


# Change to a non-root user
USER ${APP_USER}:${APP_USER}

# Uncomment after creating your docker-entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

# RUN sed -i 's/\r$//g' ./entrypoint.sh && chmod +x ./entrypoint.sh

# CMD ["./entrypoint.sh"]


# Build argument allowing to change Python version
# ARG PYTHON_VERSION=3.7

# # Build dependencies in separate container
# FROM python:${PYTHON_VERSION}-alpine AS builder
# ENV WORKDIR /app
# COPY requirements.txt ${WORKDIR}/

# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev
# RUN pip install psycopg2-binary
# RUN pip install uwsgi
# RUN pip install -r ${WORKDIR}/requirements.txt

# # Create the final container with the app
# FROM python:${PYTHON_VERSION}-alpine

# ENV USER=docker \
#     GROUP=docker \
#     UID=12345 \
#     GID=23456 \
#     HOME=/app \
#     PYTHONUNBUFFERED=1
# WORKDIR ${HOME}

# # Create user/group
# RUN addgroup --gid "${GID}" "${GROUP}" \
#     && adduser \
#     --disabled-password \
#     --gecos "" \
#     --home "$(pwd)" \
#     --ingroup "${GROUP}" \
#     --no-create-home \
#     --uid "${UID}" \
#     "${USER}"

# # Run as docker user
# USER ${USER}
# # Copy installed packages
# COPY --from=builder /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages
# # Copy uWSGI binary
# COPY --from=builder /usr/local/bin/uwsgi /usr/local/bin/uwsgi
# # Copy the application
# COPY --chown=docker:docker . .
# # Collect static files
# RUN python manage.py collectstatic --noinput

# ENV UWSGI_MODULE=config.wsgi:application
# ENV UWSGI_PROCESSES=10
# ENV UWSGI_THREADS=2
# ENV UWSGI_OFFLOAD_THREADS=10
# ENV UWSGI_STATIC_EXPIRES=86400

# ENTRYPOINT [ "uwsgi", "--ini", "uwsgi.ini" ]
# EXPOSE $PORT