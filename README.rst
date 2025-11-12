=======
rmfpapi
=======

Fake product RASENMAEHER integration API service. Serves as a reference implementation for a new integration into the deploy app ecosystem.

Helpful Tips for Using this Repo as a Reference
-----------------------------------------------

Each integration repository should include the API endpoints defined under the directory `src`, and a ui component under the directory `ui`

User Interface
^^^^^^^^^^^^^^

In the example here, we add a federated component through module federation + vite. In the wider `docker-rasenmaher-integration` context, there is a
shared docker volume `ui_files`. In production and local modes, the flow is as follows:

`Dockerfile`:
- Build and vite UI (into `ui/dist`)
- Copy `ui/dist` into `ui_build`
`entrypoint.sh`:
- Copy `ui_build` into docker volume `ui_files/{shortname}`

The last step is important if we want changes to the UI to reflect new builds without destroying the docker volumes in between, which is
desirable when developing. In development mode, the `entrypoint.sh` script is not used, and we must instead add the step of copying to
the docker volume to the command in the docker compose file (in `docker-rasenmaher-integration`).

For an integration to work correctly, we need to have consistency with the naming schemes. Especially the shortname needs to be consistent between
the URL where the API is found and the directory where the UI is stored within the docker volume. For this project, as an example, the shortname
is "fake"


Docker
------

For more controlled deployments and to get rid of "works on my computer" -syndrome, we always
make sure our software works under docker.

It's also a quick way to get started with a standard development environment.

SSH agent forwarding
^^^^^^^^^^^^^^^^^^^^

We need buildkit_::

    export DOCKER_BUILDKIT=1

.. _buildkit: https://docs.docker.com/develop/develop-images/build_enhancements/

And also the exact way for forwarding agent to running instance is different on OSX::

    export DOCKER_SSHAGENT="-v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock"

and Linux::

    export DOCKER_SSHAGENT="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK"

Creating a development container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build image, create container and start it::

    docker build --ssh default --target devel_shell -t rmfpapi:devel_shell .
    docker create --name rmfpapi_devel -p 4625:4625 -v `pwd`":/app" -it `echo $DOCKER_SSHAGENT` rmfpapi:devel_shell
    docker start -i rmfpapi_devel


In the shell you can start the uvicorn devel server with (binding to 0.0.0.0 is important!)::

    uvicorn "rmfpapi.app:get_app" --factory --host 0.0.0.0 --port 4625 --reload --log-level debug


pre-commit considerations
^^^^^^^^^^^^^^^^^^^^^^^^^

If working in Docker instead of native env you need to run the pre-commit checks in docker too::

    docker exec -i rmfpapi_devel /bin/bash -c "pre-commit install  --install-hooks"
    docker exec -i rmfpapi_devel /bin/bash -c "pre-commit run --all-files"

You need to have the container running, see above. Or alternatively use the docker run syntax but using
the running container is faster::

    docker run --rm -it -v `pwd`":/app" rmfpapi:devel_shell -c "pre-commit run --all-files"

Test suite
^^^^^^^^^^

You can use the devel shell to run py.test when doing development, for CI use
the "tox" target in the Dockerfile::

    docker build --ssh default --target tox -t rmfpapi:tox .
    docker run --rm -it -v `pwd`":/app" `echo $DOCKER_SSHAGENT` rmfpapi:tox

Production docker
^^^^^^^^^^^^^^^^^

There's a "production" target as well for running the application, remember to change that
architecture tag to arm64 if building on ARM::

    docker build --ssh default --target production -t rmfpapi:latest .
    docker run -it --name rmfpapi -p 4625:4625 rmfpapi:amd64-latest

Development
-----------

TLDR:

- Create and activate a Python 3.11 virtualenv (assuming virtualenvwrapper)::

    mkvirtualenv -p `which python3.11` my_virtualenv

- change to a branch::

    git checkout -b my_branch

- install Poetry: https://python-poetry.org/docs/#installation
- Install project deps and pre-commit hooks::

    poetry install
    pre-commit install --install-hooks
    pre-commit run --all-files

- Ready to go.

Remember to activate your virtualenv whenever working on the repo, this is needed
because pylint and mypy pre-commit hooks use the "system" python for now (because reasons).
