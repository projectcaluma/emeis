FROM python:3.9.7-slim-buster@sha256:76eaa9e5bd357d6983a88ddc9c4545ef4ad64c50f84f081ba952c7ed08e3bdd6
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

ARG REQUIREMENTS=requirements-prod.txt
COPY requirements-base.txt requirements-prod.txt requirements-dev.txt $APP_HOME/
RUN pip install --upgrade --no-cache-dir --requirement $REQUIREMENTS --disable-pip-version-check

USER emeis

COPY . $APP_HOME

EXPOSE 8000

CMD /bin/sh -c "wait-for-it.sh $DATABASE_HOST:${DATABASE_PORT:-5432} -- ./manage.py migrate && gunicorn --workers 10 --access-logfile - --limit-request-line 16384 --bind :8000 emeis.wsgi"
