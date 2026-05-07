# syntax=docker/dockerfile:1.1.7-experimental
#############################################
# Tox testsuite for multiple python version #
#############################################
FROM advian/tox-base:debian-bookworm AS tox
ARG PYTHON_VERSIONS="3.11"
ARG UV_VERSION="0.11.6"
RUN export RESOLVED_VERSIONS=`pyenv_resolve $PYTHON_VERSIONS` \
    && echo RESOLVED_VERSIONS=$RESOLVED_VERSIONS \
    && for pyver in $RESOLVED_VERSIONS; do pyenv install -s $pyver; done \
    && pyenv global $RESOLVED_VERSIONS \
    && pip install -U "uv==$UV_VERSION" tox tox-uv \
    && apt-get update && apt-get install -y \
        git \
    && rm -rf /var/lib/apt/lists/* \
    && true


######################
# Base builder image #
######################
FROM python:3.11-bookworm AS builder_base
COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /usr/local/bin/

ENV \
  # locale
  LC_ALL=C.UTF-8 \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # uv:
  UV_PROJECT_ENVIRONMENT=/.venv \
  UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y \
        curl \
        git \
        bash \
        build-essential \
        libffi-dev \
        libssl-dev \
        libzmq3-dev \
        tini \
        openssh-client \
        cargo \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    # githublab ssh
    && mkdir -p -m 0700 ~/.ssh && ssh-keyscan gitlab.com github.com | sort > ~/.ssh/known_hosts \
    && true

SHELL ["/bin/bash", "-lc"]

# Copy only requirements, to cache them in docker layer:
WORKDIR /pysetup
COPY ./uv.lock ./pyproject.toml ./README.rst /pysetup/
# Install runtime deps into the project venv (without installing the project itself yet)
RUN --mount=type=ssh uv venv /.venv \
    && echo 'source /.venv/bin/activate' >>/root/.profile \
    && uv sync --frozen --no-install-project --no-dev \
    && true


####################################
# Base stage for production builds #
####################################
FROM builder_base AS production_build
# Copy entrypoint script
COPY ./docker/entrypoint.sh /docker-entrypoint.sh
COPY ./docker/container-init.sh /container-init.sh
# Only files needed by production setup
COPY ./uv.lock ./pyproject.toml ./README.rst /app/
COPY ./src /app/src
WORKDIR /app
# Build the wheel package with uv
RUN --mount=type=ssh source /.venv/bin/activate \
    && mkdir -p /tmp/wheelhouse \
    && uv build --wheel --out-dir /tmp/wheelhouse \
    && chmod a+x /docker-entrypoint.sh \
    && chmod a+x /container-init.sh \
    && true


#########################
# Main production build #
#########################
FROM python:3.11-slim-bookworm AS production
COPY --from=pvarki/kw_product_init:latest /kw_product_init /kw_product_init
COPY --from=production_build /tmp/wheelhouse /tmp/wheelhouse
COPY --from=production_build /docker-entrypoint.sh /docker-entrypoint.sh
COPY --from=production_build /container-init.sh /container-init.sh
WORKDIR /app
RUN --mount=type=ssh apt-get update && apt-get install -y \
        bash \
        libffi8 \
        tini \
        git \
        openssh-client \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && chmod a+x /docker-entrypoint.sh \
    && chmod a+x /container-init.sh \
    && WHEELFILE=`echo /tmp/wheelhouse/rmfpapi-*.whl` \
    && pip3 install --index-url https://nexus.dev.pvarki.fi/repository/python/simple "$WHEELFILE" \
    && rm -rf /tmp/wheelhouse/ \
    && true
ENTRYPOINT ["/usr/bin/tini", "--", "/docker-entrypoint.sh"]


#####################################
# Base stage for development builds #
#####################################
FROM builder_base AS devel_build
# Install deps
COPY . /app
WORKDIR /app
RUN --mount=type=ssh source /.venv/bin/activate \
    && uv sync --frozen \
    && true


#0############
# Run tests #
#############
FROM devel_build AS test
WORKDIR /app
ENTRYPOINT ["/usr/bin/tini", "--", "docker/entrypoint-test.sh"]
# Re run install to get the service itself installed
RUN --mount=type=ssh source /.venv/bin/activate \
    && uv sync --frozen \
    && ln -s /app/docker/container-init.sh /container-init.sh \
    && docker/pre_commit_init.sh \
    && true


###########
# Hacking #
###########
FROM devel_build AS devel_shell
# Copy everything to the image
COPY --from=pvarki/kw_product_init:latest /kw_product_init /kw_product_init
WORKDIR /app
RUN apt-get update && apt-get install -y zsh \
    && sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
    && echo "source /root/.profile" >>/root/.zshrc \
    && pip3 install git-up \
    && ln -s /app/docker/container-init.sh /container-init.sh \
    && true
ENTRYPOINT ["/bin/zsh", "-l"]
