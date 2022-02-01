## v1.0.0 (1 February 2022)

## Update to Django 3.2
Bump to latest Django LTS and lift other dependencies while giving some slack on the version requirements in `setup.py` so it won't be too hard to bump to this release.

### Feature
* **core** Rename the basemodel's `meta` field to `metainfo` in order to respect reserved words of [django-restframework-json-api](https://github.com/django-json-api/django-rest-framework-json-api/blob/main/CHANGELOG.md#430---2021-12-10) ([`be444a6`](https://github.com/projectcaluma/emeis/pull/298/commits/be444a622b05139df041b2530018672cb95dad91))

### Breaking
* Rename basemodel's `meta` field to `metainfo`

## v0.6.0 (14 January 2022)

### Feature
* Case insensitive ordering ([`f0570ab`](https://github.com/projectcaluma/emeis/commit/f0570ab9a25e02d8e5aff96a8eb30a48b5d24692))
* Add user list export as xlsx file ([`190c2a6`](https://github.com/projectcaluma/emeis/commit/190c2a6d2ca05a7f862d84623d4675a730b03ad4))

## v0.5.0 (14 December 2021)

### Feature
* Expose full scope name on api ([`3465b97`](https://github.com/projectcaluma/emeis/commit/3465b97862e1b56a7ebfe6f4e2aeb273025141b7))
* New create_scope command ([`6813833`](https://github.com/projectcaluma/emeis/commit/68138334729d7cf53bc90acf629a7e0ade1ff56b))


## v0.4.0 (31 August 2021)

### Feature

* Expose full scope name on api ([`3465b97`](https://github.com/projectcaluma/emeis/commit/3465b97862e1b56a7ebfe6f4e2aeb273025141b7))
* new `create_scope` command ([`93fa60`](https://github.com/projectcaluma/emeis/commit/93fa6058b885c5215e3264564eae66c5250406d6))
  Note: The settings `ADMIN_USERNAME`, `ADMIN_ROLE_SLUG`, and `ADMIN_SCOPE_NAME`
  have been removed. Use `manage.py createsuperuser` and `manage.py create_scope`
  instead.


##  v0.3.0 (27 August 2021)

### Feature
* **permissions:** Introduce django generic api permissions ([`ff5aa2f`](https://github.com/projectcaluma/emeis/commit/ff5aa2f5f016d2236f669a0b8f3ea72ac5e67e72))
* **auth:** Introduce user factory setting and oidc user object ([`0716162`](https://github.com/projectcaluma/emeis/commit/0716162bf8963d7e167a8935e1f0dd3aff79a91d))
* Add filters on User endpoint ([`95b15d2`](https://github.com/projectcaluma/emeis/commit/95b15d2172a2b7a7bb3d189e6399f4ac97bc576a))
* **scopes:** Expose level on api ([`ddc36ee`](https://github.com/projectcaluma/emeis/commit/ddc36ee9682bb89f1f1f4697cd36e75215cb1a87))


## v0.2.2 (26 July 2021)

### Fixes

* add missing migration for new manager on user model

## v0.2.1 (22 July 2021)

### Fixes

*  auth: make emeis user model able to authenticate (#249)

## v0.2.0 (22 July 2021)

Various bugfixes to make Emeis usable as a Django app


## v0.1.0 (22 July 2021)

Initial release
