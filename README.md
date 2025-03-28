# Archived Repository

This repository is no longer maintained and has been archived for reference purposes.


# Touchstone Manager

Manage and view Touchstone Files and Corresponding Test Objects.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pipeline status](https://gitlab.mn.tu-dresden.de/s3420145/touchstone-manager/badges/main/pipeline.svg)](https://gitlab.mn.tu-dresden.de/s3420145/touchstone-manager/commits/main)
[![coverage report](https://gitlab.mn.tu-dresden.de/s3420145/touchstone-manager/badges/main/coverage.svg)](https://gitlab.mn.tu-dresden.de/s3420145/touchstone-manager/commits/main)


License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy touchstone_manager

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### CSS compilation

This app uses tailwindcss for styling. To compile the css during development, run:

    $ npm run dev

To compile the minified css, run:

    $ npm run build

The latter will be run automatically while building the production docker image.

### Documentation

This project uses Sphinx documentation generator.

After you have set up to [develop locally with docker](https://cookiecutter-django.readthedocs.io/en/3.1.13/developing-locally-docker.html), run the follwing command:

    $ docker compose -f docs.yml up

Navigate to port 9000 on your host to see the documentation. This will be opened automatically at [localhost](http://localhost:9000) for local, non-docker development.

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd touchstone_manager
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd touchstone_manager
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd touchstone_manager
celery -A config.celery_app worker -B -l info
```

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
