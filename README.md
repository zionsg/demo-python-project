# Demo Python Project

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
- Run `poetry run poe start` to start the application server.
- The API can be accessed via `http://localhost:10000`.
- Additional stuff:
    + Run `poetry run poe lint` to perform linting checks.

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
- Directory structure for project
  (diagram generated using `tree --charset unicode --dirsfirst -a -n -I ".git|.venv"`):

    ```
    .
    |-- src  # Source code
    |   `-- index.py  # Application entrypoint
    |-- tests  # Test suites
    |-- .gitattributes
    |-- .gitignore
    |-- .python-version  # Created by pyenv, indicates Python version to use for virtual environment
    |-- README.md
    |-- poetry.lock
    |-- poetry.toml  # Created by Poetry for local Poetry configuration
    `-- pyproject.toml  # Project configuration
    ```
