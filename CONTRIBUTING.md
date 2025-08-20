# Contributing

Contributions to emeis are very welcome! Best have a look at the open [issues](https://github.com/projectcaluma/emeis)
and open a [GitHub pull request](https://github.com/projectcaluma/emeis/compare). See instructions below how to setup development
environment. Before writing any code, best discuss your proposed change in a GitHub issue to see if the proposed change makes sense for the project.

## Setup development environment

### Clone

To work on emeis you first need to clone

```bash
git clone https://github.com/projectcaluma/emeis.git
cd emeis
```

### Open Shell

Once it is cloned you can easily open a shell in the docker container to
open an development environment.

```bash
# needed for permission handling
# only needs to be run once
echo UID=$UID > .env
# open shell
docker-compose run --rm emeis bash
```

### Testing

Once you have shelled in docker container as described above
you can use common python tooling for formatting, linting, testing
etc.

```bash
# linting
ruff check .
# format code
ruff format .
# running tests
pytest
# create migrations
./manage.py makemigrations
# install debugger or other temporary dependencies
pip install --user pdbpp
```

Writing of code can still happen outside the docker container of course.

### Install new requirements

In case you're adding new requirements you simply need to build the docker container
again for those to be installed and re-open shell.

```bash
docker-compose build --pull
```

### Setup pre commit

Pre commit hooks is an additional option instead of executing checks in your editor of choice.

First create a virtualenv with the tool of your choice before running below commands:

```bash
pip install pre-commit
pip install -r requiements-dev.txt -U
pre-commit install
```
