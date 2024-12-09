##
# Dockerfile
#
# If there is a need to clone or install packages from private code repositories in this Dockerfile:
#   - Start the SSH agent on the host machine where the Docker image is being built and add the SSH key,
#     e.g. `eval $(ssh-agent) && ssh-add /home/python/.ssh/key-used-for-cloning-private-repository.id_rsa`
#   - Forward the SSH agent from the host machine when building the Docker image,
#     e.g. `DOCKER_BUILDKIT=1 docker build --ssh default .`
#   - Install SSH client and Git in this Dockerfile, e.g. `apt-get install --yes openssh-client git`
#   - Add github.com to known_hosts in this Dockerfile to avoid prompt to authenticate the domain when downloading the
#     private repos via SSH, e.g. `RUN mkdir -p -m 0600 /home/python/.ssh && ssh-keyscan github.com >> /home/python/.ssh/known_hosts`
#   - Mount the SSH agent for RUN commands in this Dockerfile when installing dependencies or cloning the private repos,
#     e.g. `RUN --mount=type=ssh poetry install --no-root --no-ansi --without dev`
#     or `RUN --mount=type=ssh git clone git@github.com:zionsg/test-private-package.git`
##

# Debian Linux
FROM python:3.11.10-slim-bookworm

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive POETRY_VERSION=1.8.5

# Create non-root user - regular users start with user ID 1000 (https://www.baeldung.com/linux/user-ids-reserved-values)
# Adapted from https://github.com/nodejs/docker-node/blob/main/22/bookworm-slim/Dockerfile
RUN groupadd --gid 1000 python \
    && useradd --uid 1000 --gid python --shell /bin/bash --create-home python

# Install system packages: cURL (used in healthcheck), dumb-init (used in Dockerfile),
# nano/vim (editor), git/OpenSSH (used for installing packages from private repositories),
# pipx (for installing Poetry)
# To test connection to Redis/database servers without their CLI tools (telnet not installed for security reasons):
#   - Redis: curl --verbose --output - telnet://myapp-redis-server:6379
#       + Enter "PING" and it should respond with "PONG", enter "quit" to exit.
#   - MySQL: curl --verbose --output - telnet://myapp-db-mysql-server:3306
#       + "--output -" needed to display binary output. Press Ctrl-C to quit.
#   - PostgreSQL: curl --verbose telnet://myapp-db-postgresql-server:5432
#       + Press Enter to close connection.
RUN apt-get --yes update \
    && apt-get --yes --no-install-recommends install curl dumb-init nano pipx vim \
    && rm -rf /var/lib/apt/lists/*

# Switch to non-root user before installing Poetry else will have issues installing dependencies and running app
# All paths use /home/python explictly as $HOME and ~ do not seem to be resolved after switching user
# Need to set PATH env var (as ensurepath needs relogin) else can't run Poetry after installation via Pipx
USER python
ENV PATH="/home/python/.local/bin:$PATH"
RUN pipx ensurepath \
    && pipx install "poetry==$POETRY_VERSION" \
    && poetry --version

# Create app directory and switch to it
RUN mkdir -p /home/python/app/log \
    && mkdir -p /home/python/app/src \
    && mkdir -p /home/python/app/tmp
WORKDIR /home/python/app

# Copy only essential files and folders, including client-specific custom code that may be bundled with application
# Docker recommends using COPY instruction over ADD.
# Placing the copy commands explicitly here is easier to troubleshoot
# than using .dockerignore. Do NOT copy .env inside here, use docker-compose.yml
# or Docker CLI to set environment variables for the container instead.
COPY --chown=python:python src/ /home/python/app/src/
COPY --chown=python:python .python-version poetry.lock poetry.toml pyproject.toml /home/python/app/

# Install production dependencies
# Config in poetry.toml ensures dependencies are created inside the app directory and that a new
# virtual environment is created as we will not be running as root (see
# https://www.reddit.com/r/learnpython/comments/13pq62l/comment/jlaya2d for more info)
RUN poetry install --no-root --no-ansi --without dev

# Set "python" user as owner of app directory as the container will not be run as root
RUN chown -R python:python /home/python/app/

# Using dumb-init allows proper terminating of application in Docker container
# CMD can be overridden via `command` in docker-compose.yml while ENTRYPOINT ensures CMD/command go thru dumb-init
# Run as non-root - see https://snyk.io/blog/10-best-practices-to-containerize-nodejs-web-applications-with-docker
ENTRYPOINT ["dumb-init", "--"]
CMD ["poetry", "run", "python", "src/index.py"]
