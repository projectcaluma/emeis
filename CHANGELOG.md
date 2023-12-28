## v1.3.1 (28 December 2023)

### Fix
* **deps:** update dependencies([`8890b3b`](https://github.com/projectcaluma/emeis/commit/8890b3beb5b31c7f36d5dd71b69afedc10ecf2f9))

## v1.3.0 (12 October 2023)

### Feature
* **export:** Add filtering support ([`7830dc3`](https://github.com/projectcaluma/emeis/commit/7830dc3c96fdc5ee376576eab434e6e6f22eb85f))
* **tests:** Verify that creating circular scope structures fails ([`629c20e`](https://github.com/projectcaluma/emeis/commit/629c20eb81d3cb0510777a5999b6a7826fb36592))

## v1.2.2 (4 April 2023)

### Fix
* **scopes:** Update subscope's full names when scope changes ([`4f125ce`](https://github.com/projectcaluma/emeis/commit/4f125cee8f2191f4410d333eea951e47317270d0))


## v1.2.1 (2 December 2022)

### Fix
* **signals:** Do not crash while loading fixtures ([`be45eff`](https://github.com/projectcaluma/emeis/commit/be45eff565e25c060dd0ddb9f2a4962e692e7b35))


## v1.2.0 (17 November 2022)

### Feature
* **views:** Apply localized default ordering ([`7e1265c`](https://github.com/projectcaluma/emeis/commit/7e1265ccdd3f2a81dba3060320f58ab7d99b2dde))

### Fix
* **models:** Set scope full_name correctly in all situations ([`47ff9b5`](https://github.com/projectcaluma/emeis/commit/47ff9b502eeeaa056113bd40966b6052491384b6))
* **ordering:** Correct ordering when forced local is in use ([`a7ee5d3`](https://github.com/projectcaluma/emeis/commit/a7ee5d3bc8e93d5f778b452530aa12219ba9ab15))


## v1.1.0 (23. September 2022)

### Feature
* **scopes:** Denormalize full_name and use it for sorting ([`4921028`](https://github.com/projectcaluma/emeis/commit/49210282c2dca850f895cb6e2b394f9ed35171bc))
* **visibilities:** Respect visibilities in includes & relationships ([`1ef2a88`](https://github.com/projectcaluma/emeis/commit/1ef2a881e7350935779e495d2edc6afaade4e75b))
* Add advanced filters for ACL model ([`184c9a2`](https://github.com/projectcaluma/emeis/commit/184c9a26a29443e7036dc4f23f8589cc8e4cffd5))
* Add "is_active" filter for user model ([`8efbdc0`](https://github.com/projectcaluma/emeis/commit/8efbdc0a6cb3d5d0b74fa92aa9e5801f9ab270e5))
* Search by metainfo fields ([`be26f41`](https://github.com/projectcaluma/emeis/commit/be26f415c5f9813e66e297ebee8c7f71bb055e66))
* Order by metainfo fields ([`17a9849`](https://github.com/projectcaluma/emeis/commit/17a98492cf0743727fcae6322641fd4fc839d070))
* Add id__in filter for scopes ([`b7602a9`](https://github.com/projectcaluma/emeis/commit/b7602a9a82fc3a5972047137a866bc971cbf7ff8))
* **models:** Add is_active property for scope ([`cf5f01f`](https://github.com/projectcaluma/emeis/commit/cf5f01fed61cf4adefbf05b37ff3e8f0b1ad129f))
* **search:** Search for user's roles and scopes ([`5418e18`](https://github.com/projectcaluma/emeis/commit/5418e18756a855ada4c1c039bb9e72e75efc53f0))
* **search:** Enable forcing models to be monolingual in search ([`1dc55fd`](https://github.com/projectcaluma/emeis/commit/1dc55fd83c534bb5949ccecadc1dbc04877d9c7f))

### Fix
* **dev-env:** Start runserver  with keep-meta-shutdown ([`749ee20`](https://github.com/projectcaluma/emeis/commit/749ee208df3475dffe885d186986cd389e6c96c9))
* Remove subtree when removing scope ([`fc1e4ff`](https://github.com/projectcaluma/emeis/commit/fc1e4ff577d95d245375f8c16ca17a49f5dd39a7))
* Rename translation in export ([`4b4a4c0`](https://github.com/projectcaluma/emeis/commit/4b4a4c066e0e30dadf56db84db7756c90d22f531))
* Xlsx file on pypi, take 3 ([`5e9262b`](https://github.com/projectcaluma/emeis/commit/5e9262b5ccd9cbba61d2b8aeb9cab98ca4a439b2))


## v1.0.5 (15 February 2022)

### Fix
* Include xlsx file in pypi publish, take 2 ([`5acc687`](https://github.com/projectcaluma/emeis/commit/5acc68780a6ce2403c6780fd8766f1b99d299e50))

## v1.0.4 (15 February 2022)

### Fix
* Add xlsx template to pip package ([`532b379`](https://github.com/projectcaluma/emeis/commit/532b379edfcebc6d8a7ea6ff6c176682a0b74806))

## v1.0.3 (11 February 2022)

### Fix
* Set correct content-disposition header in export ([`35e0f09`](https://github.com/projectcaluma/emeis/commit/35e0f09aa99d552d70f6920ce61df989fb9d01ad))

## v1.0.2 (3 February 2022)

This release upgrades dependency pinnings and loosens requirement ranges in `setup.py`.

### Fixes
* **core** Alter deprecated postgres JSON field to Django's own ([`f6cded9`](https://github.com/projectcaluma/emeis/commit/f6cded94a602ff16842f85340ece0dfa55ad12dc))

## v1.0.1 (2 February 2022)

Release only pinning dependency version, not adding any features.
* chore: upgrade dependency psycopg2 to 2.9.3

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
