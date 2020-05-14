# emeis

[![Build Status](https://travis-ci.com/projectcaluma/emeis.svg?branch=master)](https://travis-ci.com/projectcaluma/emeis)
[![Pyup](https://pyup.io/repos/github/projectcaluma/emeis/shield.svg)](https://pyup.io/account/repos/github/projectcaluma/emeis/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/projectcaluma/emeis)

user management

## Getting started

### Installation

**Requirements**
* docker
* docker-compose

After installing and configuring those, download [docker-compose.yml](https://raw.githubusercontent.com/projectcaluma/emeis/master/docker-compose.yml) and run the following command:

```bash
docker-compose up -d
```

You can now access the api at [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/).

### Configuration

Document Merge Service is a [12factor app](https://12factor.net/) which means that configuration is stored in environment variables.
Different environment variable types are explained at [django-environ](https://github.com/joke2k/django-environ#supported-types).

#### Common

A list of configuration options which you need

* `SECRET_KEY`: A secret key used for cryptography. This needs to be a random string of a certain length. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY).
* `ALLOWED_HOSTS`: A list of hosts/domains your service will be served from. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts).
* `DATABASE_ENGINE`: Database backend to use. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-DATABASE-ENGINE). (default: django.db.backends.postgresql)
* `DATABASE_HOST`: Host to use when connecting to database (default: localhost)
* `DATABASE_PORT`: Port to use when connecting to database (default: 5432)
* `DATABASE_NAME`: Name of database to use (default: emeis)
* `DATABASE_USER`: Username to use when connecting to the database (default: emeis)
* `DATABASE_PASSWORD`: Password to use when connecting to database

## Contributing

Look at our [contributing guidelines](CONTRIBUTION.md) to start with your first contribution.
