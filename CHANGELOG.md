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
