FROM python:3.6.12-slim-buster@sha256:09bb81730d8d3f1b208d9c5ba4be66747ef29323597bedab6404b884a016685d
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev wget build-essential \
&& wget -q https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /usr/local/bin \
&& chmod +x /usr/local/bin/wait-for-it.sh \
&& mkdir -p /app \
&& useradd -u 901 -r emeis --create-home \
# all project specific folders need to be accessible by newly created user but also for unknown users (when UID is set manually). Such users are in group root.
&& chown -R emeis:root /home/emeis \
&& chmod -R 770 /home/emeis

# needs to be set for users with manually set UID
ENV HOME=/home/emeis

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE emeis.settings
ENV APP_HOME=/app
ENV UWSGI_INI /app/uwsgi.ini

ARG REQUIREMENTS=requirements-prod.txt
COPY requirements-base.txt requirements-prod.txt requirements-dev.txt $APP_HOME/
RUN pip install --upgrade --no-cache-dir --requirement $REQUIREMENTS --disable-pip-version-check

USER emeis

COPY . $APP_HOME

EXPOSE 8000

CMD /bin/sh -c "wait-for-it.sh $DATABASE_HOST:${DATABASE_PORT:-5432} -- ./manage.py migrate && uwsgi"
