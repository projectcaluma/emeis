# emeis

[![Build Status](https://github.com/projectcaluma/emeis/workflows/Tests/badge.svg)](https://github.com/projectcaluma/emeis/actions?query=workflow%3ATests)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/projectcaluma/emeis/blob/main/setup.cfg#L50)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/projectcaluma/emeis)
[![License: GPL-3.0-or-later](https://img.shields.io/github/license/projectcaluma/emeis)](https://spdx.org/licenses/GPL-3.0-or-later.html)

A generic user management service.

The word emeis ([e̞ˈmis]) comes from greek (εμείς) and means `we`.

[Original RFC that led to emeis](docs/original_emeis_rfc.md)

### Configuration

It's important to configure the app before the first start. When running for the first
time, there is a data migration, that depends on settings from the config.

emeis is a [12factor app](https://12factor.net/) which means that configuration is
stored in environment variables.
Different environment variable types are explained at
[django-environ](https://github.com/joke2k/django-environ#supported-types).

#### Common

A list of configuration options which you might need to configure to get emeis started in your environment.

##### General
* `SECRET_KEY`: A secret key used for cryptography. This needs to be a random string of a certain length. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY).
* `ALLOWED_HOSTS`: A list of hosts/domains your service will be served from. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts).

##### Database
* `DATABASE_ENGINE`: Database backend to use. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-DATABASE-ENGINE). (default: django.db.backends.postgresql)
* `DATABASE_HOST`: Host to use when connecting to database (default: localhost)
* `DATABASE_PORT`: Port to use when connecting to database (default: 5432)
* `DATABASE_NAME`: Name of database to use (default: emeis)
* `DATABASE_USER`: Username to use when connecting to the database (default: emeis)
* `DATABASE_PASSWORD`: Password to use when connecting to database

##### i18n
* `LANGUAGE_CODE`: Language code of the default language (default: en)
* `LANGUAGES`: A list of supported languages (default: \[en\])


#### Additional options

Additional options you might want to configure

##### OIDC

For OIDC, a customized [mozilla-django-oidc](https://github.com/mozilla/mozilla-django-oidc) is used.

Most of the settings below are documented in it's [respective documentation](https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html).

* `OIDC_OP_USER_ENDPOINT`: Url of userinfo endpoint (see [spec](https://openid.net/specs/openid-connect-core-1_0.html#UserInfo))
* `OIDC_VERIFY_SSL`: Bool (default: true)
* `OIDC_BEARER_TOKEN_REVALIDATION_TIME`: Time in seconds before bearer token validity is verified again. For best security, token is validated on each request per default. It might be helpful though in case of slow Open ID Connect provider to cache it. It uses [cache](#cache) mechanism for memorizing userinfo result. Number has to be lower than access token expiration time. (default: 0)
* `OIDC_CREATE_USER`: Enables or disables automatic user creation during authentication (default: false). If set to false, users have to be created manually in emeis with the username set to the value that will be received in the `OIDC_USERNAME_CLAIM`.
* `OIDC_UPDATE_USER`: Enables or disables updating of the user email address based on the email claim (default: false)
* `OIDC_USERNAME_CLAIM`: Name of claim that contains the username (default: sub). This is needed for matching users from the received claims.
* `OIDC_EMAIL_CLAIM`: Name of claim that contains the email address (default: email). This is only needed if `OIDC_CREATE_USER` or `OIDC_UPDATE_USER` are `true`
* `OIDC_OP_INTROSPECT_ENDPOINT`: Url of introspection endpoint (optionally needed for Client Credentials Grant)
* `OIDC_RP_CLIENT_ID`: ID of the client (optionally needed for Client Credentials Grant)
* `OIDC_RP_CLIENT_SECRET`: Secret of the client (optionally needed for Client Credentials Grant)
* `EMEIS_OIDC_USER_FACTORY`: Optional, factory function (or class) that defines
   an OIDC user object. See also here: [Extending Emeis](docs/extending_emeis.md)

##### Cache

* `CACHE_BACKEND`: [cache backend](https://docs.djangoproject.com/en/1.11/ref/settings/#backend) to use (default: django.core.cache.backends.locmem.LocMemCache)
* `CACHE_LOCATION`: [location](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-CACHES-LOCATION) of cache to use

##### CORS headers

Per default no CORS headers are set but can be configured with following options.

* `CORS_ORIGIN_ALLOW_ALL`: If True, the whitelist will not be used and all origins will be accepted. (default: False)
* `CORS_ORIGIN_WHITELIST`: A list of origin hostnames (including the scheme and with optional port) that are authorized to make cross-site HTTP requests.

##### Logging

* `LOG_LEVEL`: The logging level of the console logging handler (default: INFO)

##### Anonymous write

* `ALLOW_ANONYMOUS_WRITE`: If set to `true`, unauthenticated users are allowed to write data (default: false)

Their request will also go through the permission layer and access can be restricted/denied from there.

This setting can be handy when setting up emeis or during development, when no OIDC provider is available.

This should always be `false` in production environments.

### Installation

**Requirements**
* docker
* docker-compose

After installing and configuring those, download [docker-compose.yml](https://raw.githubusercontent.com/projectcaluma/emeis/main/docker-compose.yml) and run the following command:

```bash
# only needs to be run once
echo UID=$UID > .env

docker-compose up -d
```

This will build the containers, start the services and run the database migrations. Additionally, it
creates a user, scope, role and and ACL for administration based on the settings [documented above](#Bootstrapping)

## Getting started

You can now access the api at [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/).

Read more about extending and configuring Emeis here: [Extending Emeis](docs/extending_emeis.md).

## Contributing

Look at our [contributing guidelines](CONTRIBUTING.md) to start with your first contribution.

## Maintainer's Handbook

Some notes for maintaining this project can be found in [the maintainer's handbook](MAINTAINING.md).
