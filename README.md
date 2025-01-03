# Demo Python Project

**Disclaimer** This is just a personal hobbyist project to experiment with
creating/Dockerizing a Python application with a simple structure without the
use of bloated frameworks.

Paths in all documentation, even those in subfolders, are relative to the root
of the repository. Shell commands are all run from the root of the repository.

## Sections
- [Requirements](#requirements)
- [API Documentation](#api-documentation)
- [Installation](#installation)
- [Application Design](#application-design)

## Requirements
- [Docker Engine](https://docs.docker.com/engine/release-notes/) >= 27.3.1
- [Docker Compose](https://docs.docker.com/compose/release-notes/) >= 2.29.7
    + Docker Compose v3 not used as it does not support the `extends` key.
    + Docker Compose v1 not used as it does not support the `depends_on` key.
    + Note that Docker Compose v2 uses the `docker compose` command (without
      hyphen) via the Compose plugin for Docker whereas Docker Compose v1 uses
      the `docker-compose` command (with hyphen).
        * [Install Docker Compose v2 plugin on Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)
- [Python](https://www.python.org/) >= 3.11
    + Released 2024-04-24, EOL 2027-10, system-installed version in Debian 12
      (Bookworm).
    + For development purposes, it is recommended that
      [pyenv](https://github.com/pyenv/pyenv) be used to install Python as it
      can switch between multiple versions if need be for different projects,
      e.g. `pyenv install 3.11.10` to install a specific version and
      `pyenv local 3.11.10` to set the version to be used inside a project
      directory and its subdirectories.
        * Note that Python build dependencies should be installed before
          attempting to install a new Python version (see
          https://github.com/pyenv/pyenv/wiki#suggested-build-environment
          for more info).
    + For the base Docker image, `python:3.11.10-slim-bookworm` is used.
      As of Nov 2024, the stable release for Debian is version 12, codenamed
      Bookworm, released 2023-06-10 (see https://wiki.debian.org/DebianReleases
      for more info). Alpine Linux is not used as standard PyPI wheels do not
      work on Alpine, can cause unexpected runtime bugs, make builds slower
      and create larger Docker images (see
      https://pythonspeed.com/articles/alpine-docker-python/ for more info).
- [Poetry](https://python-poetry.org/) >= 1.8.3
    + This is used for dependency management.
    + [uv](https://github.com/astral-sh/uv) is not used for the following
      reasons:
        * As of Nov 2024, uv is still at version 0.5. Poetry 1.0.0 was released
          on 13 Dec 2019.
        * uv touts to be a "single tool to replace pip, pip-tools, pipx, poetry,
          pyenv, twine, virtualenv", covering Python version management,
          virtual environments, dependency management, publishing of packages,
          etc. In contrast, pyenv states that it "follows the UNIX tradition of
          single-purpose tools that do one thing well". As the quote goes, "If
          you try to please everyone you'll please no one".
        * uv is written in Rust and maintained by Astral. As this
          [article](https://martynassubonis.substack.com/p/python-project-management-primer-a55)
          mentions, "This choice, while technically sound, could narrow the pool
          of potential maintainers, limiting community support and increasing
          risk if Astral's involvement lessens". As another
          [article](https://gist.ly/youtube-summarizer/is-uv-the-future-of-python-packaging-exploring-uv-030-features)
          mentions, "Another significant concern is that Astral, backed by
          venture capital, might create a monoculture around UV and later
          disengage due to financial pressures".
- [Quart](https://github.com/pallets/quart) >= 0.19.9
    + This is an async Python micro framework for building web applications.
    + Quart is chosen over [Flask](https://flask.palletsprojects.com/en/stable/)
      as it is recommended in the Flask
      [docs](https://flask.palletsprojects.com/en/stable/async-await/#when-to-use-quart-instead)
      for its more performant async support.
    + [FastAPI](https://fastapi.tiangolo.com/) is not used for the following
      reasons:
        * Path/query/body/cookie parameters from the request are
          [automagically provided](https://fastapi.tiangolo.com/tutorial/body/#request-body-path-query-parameters)
          to the route handler via named method parameters. This can be a
          security vulnerability as a malicious actor can overwrite certain
          parameters, e.g. use a query parameter with the same name as a path
          parameter, similar to how the `$_REQUEST` superglobal in PHP is
          often avoided (see https://stackoverflow.com/a/2143042 for more info).
          In contrast, Express in Node.js provides the request
          parameters while indicating their sources, i.e. via `request.params`,
          `request.query`, `request.body` and `request.cookies`.
        * The use of Pydantic models restricts the flexibility of JSON in
          request bodies, especially when consuming external APIs which may
          add/remove keys or change types in various nesting levels without
          warning.
- [Hypercon](https://github.com/pgjones/hypercorn)
    + Web server for Python.
    + Hypercon is chosen for the following reasons:
        * It was initially part of Quart before being separated out into a
          standalone server and hence would work best with Quart.
        * It can be used programmatically, i.e. the server can be started from
          within the source code just like how the Express web server is
          used in Node.js.
- Documentation Tools:
    + [apiDoc](https://apidocjs.com/) is used for documenting API endpoints.
        * [Swagger](https://swagger.io/) is not used for the following
          reasons:
            - It is overly complex and takes more time/effort, which can
              deter developers who do not like to do documentation in the
              first place.
            - The documentation sits in a YAML/JSON file far away from the
              API route handlers in the source code, making it hard for
              developers to see the docs in its context.
    + [Sphinx](https://jsdoc.app/) is used for documenting Python code.
        * See https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html
          on docstring format.
        * See https://www.sphinx-doc.org/en/master/usage/domains/python.html#info-field-lists
          for list of possible docblock annotations.
- Testing Tools:
    + [Pylint](https://github.com/pylint-dev/pylint) is used for linting.
        * Chosen for its similarity to ESLint for Node.js.
    + [Pytest](https://github.com/pytest-dev/pytest) is used for tests.

## API Documentation
- See [`docs/apidoc/index.md`](/docs/apidoc/index.md) or open
  [`docs/apidoc/index.html`](/docs/apidoc/index.html) in a browser to
  view documentation for API endpoints.
    + The webpage does not allow making of sample requests as that would require
      running of a localhost server to serve the webpage.
- Run `npm run doc` to regenerate the API documentation in `docs/apidoc` folder.
    + This only processes files in `src/api` folder, i.e. the API component.
    + The header in the generated documentation is from
      [`docs/apidoc/APIDOC-HEADER.md`](/docs/apidoc/APIDOC-HEADER.md).
- Note that most of the endpoints, if not all, are marked as private as
  they are for internal use only and will not show up in generated docs if
  the `private` option is not used with apiDoc.

## Installation
- This section is meant for software developers working on the source code
  in this repository.
- Install and configure Poetry for dependency management.

    ```
    # Bash shell commands assume Debian/Ubuntu operating system
    python3 --version

    # Install pipx
    sudo apt install pipx
    pipx ensurepath
    source ~/.bashrc

    # Install Poetry using pipx
    pipx install poetry
    poetry --version

    # Create a new virtual environment if one doesn't already exist
    # Set to true (default) else dependencies will be installed into the
    # operating system's Python environment & potentially wreck system packages
    poetry config virtualenvs.create true

    # Create the virtual environment inside the project's root directory
    # Set to true else the virtual environment will be created in Poetry's
    # cache directory, complicating troubleshooting of project dependencies
    poetry config virtualenvs.in-project true

    # Do not install non-project dependencies
    poetry config virtualenvs.options.no-pip true
    poetry config virtualenvs.options.no-setuptools true

    # List final Poetry configuration
    poetry config --list
    ```

- Clone this repository, e.g. `git clone git@github.com:zionsg/demo-python-project.git`.
- Copy `.env.example` to `.env`. This will be read by Docker Compose and the
  application. The file `.env` will not be committed to the repository.
    + To make it easier to identify which env vars were changed, and to be
      consistent with server deployments, it is recommended that env vars
      be overridden in `docker-compose.override.yml` instead of updating `.env`.
- Run `poetry install` to install the project dependencies.
- To run the application locally:
    + For consistency with production environment, the application should be run
      using Docker during local development (which settles all dependencies)
      and not directly using `poetry run python src/index.py`.
        * May need to run Docker commands as `sudo` depending on machine
          (see https://docs.docker.com/engine/install/linux-postinstall/).
        * If you see a stacktrace error when running a Docker command in
          Windows Subsystem for Linux (WSL),
          e.g. "Error: ENOENT: no such file or directory, uv_cwd",
          try running `cd .` and run the Docker command again.
    + Create a `docker-compose.override.yml` which will be automatically used by
      Docker Compose to override specified settings in `docker-compose.yml`.
      This is used to temporarily tweak the Docker Compose configuration on the
      local machine and will not be committed to the repository. See
      https://docs.docker.com/compose/extends for more info.
        * Bare minimum contents for the application to run locally (overriding
          of ports & env vars not necessary but included to be consistent
          with server deployments):

          ```
          # docker-compose.override.yml in root of repository
          name: local # override Compose project name to follow Docker tag used here

          services:
            demo-app:
              # Use "local" tag for Docker image instead of "production" tag in docker-compose.yml
              image: demo-app:local
              ports: !override
                # use !override as modifying DEMO_PORT_* under `environment` attribute below without modifying .env
                - 10000:9000
              environment:
                - DEMO_ENV=local
                - DEMO_PORT_EXTERNAL=10000
                - DEMO_PORT_INTERNAL=9000
          ```

        * A common use case during local development would be to use the `local`
          tag for the Docker image and enabling live reload inside the Docker
          container when changes are made to the source code on a Windows host
          machine.

          ```
          # docker-compose.override.yml in root of repository
          name: local # override Compose project name to follow Docker tag used here

          services:
            demo-app:
              # Use "local" tag for Docker image instead of "production" tag in docker-compose.yml
              image: demo-app:local
              ports: !override
                # use !override as modifying DEMO_PORT_* under `environment` attribute below without modifying .env
                - 10000:9000
              environment:
                - DEMO_ENV=local
                - DEMO_PORT_EXTERNAL=10000
                - DEMO_PORT_INTERNAL=9000
              volumes:
                # Cannot use the shortform "- ./src/:/var/lib/app/src" on Windows
                # Use the .venv and site-packages folders inside container not host
                # cos packages may use Linux native libraries and not work on host platform
                - type: bind
                  source: /mnt/c/Users/Me/localhost/www/demo-python-project/pyproject.toml
                  target: /home/python/app/pyproject.toml
                - type: bind
                  source: /mnt/c/Users/Me/localhost/www/demo-python-project/src
                  target: /home/python/app/src
              command: poetry run poe dev
          ```

    + Run `poetry run poe build-local` 1st to build the Docker image with "local" tag.
        * Always run this after modifying `pyproject.toml`, e.g. installing of
          packages.
    + Run `docker compose up` to start the Docker container. May need to run as
      `sudo` depending on machine, due to Docker command.
    + Run `docker compose down` to stop the Docker container or just press
      `Ctrl+C`. However, the former should be used as it will properly shut down
      the container, else it may have problems restarting later.
    + The API can be accessed via `http://localhost:10000` using
      [cURL](https://curl.se/) or [Postman](https://www.postman.com/).
        * See `DEMO_PORT_*` env vars for port settings.
        * When using cURL on Windows, values need to be enclosed in
          double quotes instead of single quotes, hence double quotes inside
          request body (e.g. if sending JSON) need to be escaped.
        * When using Postman, if an empty response is returned with status code
          400, check that the checkbox for the "Content-Length" header is
          ticked.
- Additional stuff:
    + Run `poetry run poe lint` to perform linting checks.
    + To generate API documentation:
        * Node.js and NPM need to be installed.
            - For development purposes, it is recommended that
              [nvm](https://nodejs.org/en/download/package-manager/#nvm) be used
              to install Node.js and npm as it can switch between multiple
              versions if need be for different projects,
              e.g. `nvm install 22.12.0` to install a specific version
              and `nvm alias default 22.12.0` to set the default version.
        * Run `npm install` to install frontend dependencies.
        * Run `npm run doc` to regenerate API documentation.

## Application Design
- Use only `None` when setting default values for optional method parameters
  of mutable object type in function definitions and assign the actual desired
  default inside the function code, e.g. write `def append_to(element, to=None)`
  instead of `def append_to(element, to=[])`. This is because Python's default
  arguments are evaluated once when the function is defined, not each time the
  function is called.
    + https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments
    + https://www.cs.toronto.edu/~david/course-notes/csc110-111/06-memory-model/03-mutable-data-types.html
    + https://florimond.dev/en/posts/2018/08/python-mutable-defaults-are-the-source-of-all-evil
    + https://www.valentinog.com/blog/tirl-python-default-arguments/
- Each `.py` file corresponds to 1 module and should only contain 1 top-level
  function, or 1 top-level class with an optional top-level instance of the
  class. There should be no other top-level variables in the file. This is to
  avoid pollution of the global namespace and unnecessary exposure of internal
  classes/functions/variables.
- For private properties and methods in classes, prefix their names with
  double underscores, e.g. `__foo`, `def __bar(self)`.
    + https://www.hacksoft.io/blog/underscores-dunders-and-everything-nice
    + https://www.pythonmorsels.com/every-dunder-method/
- Directory structure for project
  (diagram generated using `tree --charset unicode --dirsfirst -a -n -I ".git|.venv|__pycache__|node_modules"`):

    ```
    .
    |-- docs  # Except for README/CHANGELOG, all documentation and linked images/files should be placed here
    |   `-- apidoc  # Generated API documentation
    |       |-- APIDOC-HEADER.md  # Header used when generating API documentation
    |       |-- index.html
    |       `-- index.md
    |-- src  # Source code
    |   |-- api
    |   |   |-- api_response.py
    |   |   `-- routes.py
    |   |-- app
    |   |   |-- config.py  # Application configuration
    |   |   |-- helper.py  # Server-side helper functions
    |   |   `-- logger.py  # Logger
    |   `-- index.py  # Application entrypoint
    |-- tests  # Test suites
    |-- .dockerignore
    |-- .env.example  # List of all environment variables for application, to be copied to .env
    |-- .gitattributes
    |-- .gitignore
    |-- .python-version  # Created by pyenv, indicates Python version to use for virtual environment
    |-- Dockerfile
    |-- README.md
    |-- docker-compose.yml
    |-- poetry.lock
    |-- poetry.toml     # Local Poetry configuration created using `poetry config --local`
    `-- pyproject.toml  # Project configuration
    ```

- Workflow
    + Application startup:
        * Docker container starts with entrypoint being `src/index.py`.
        * `main()` called.
        * Routes from `src/api/routes.py` loaded.
        * Hypercorn server started.
    + Request journey:
        * User calls `http://localhost:10000/healthcheck`.
        * Request goes to Docker container > `src/index.py` >
          `src/api/routes.py` > `@app.route('/healthcheck')` >
          `healthcheck()` which is the route handler.
        * JSON response returned by route handler > Hypercorn server > user.
