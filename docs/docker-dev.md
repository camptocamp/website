<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
-->
# Working on the project as developers

## Pre-requisite

Be sure to [install Docker and docker-compose](prerequisites.md) before going any further.

Before starting, be aware of [the documentation of the core
image](https://github.com/camptocamp/docker-odoo-project).

## Starting, git submodules

1. Clone the project

        git clone git@github.com:camptocamp/smartliberty_odoo.git smartliberty

2. Submodules

    You have two options:

    1. Clone the submodules from scratch

    ```bash
    git submodule update --init
    ```

    If you have an error because a ref cannot be found, it is probably that the
    remote has changes, you just need to run the following command that will update
    the remote:

    ```bash
    git submodule sync
    ```

    2. Use existing cloned repositories

    The Odoo repo `odoo/src` will take quite some time if pulled from scratch.
    If you already have a local checkout of one or more submodules
    you can save a lot of time avoiding to download the whole repos, by doing this:

    ```
    cp -r path/to/odoo odoo/src
    cp -r path/to/server-tools odoo/external-src/
    git submodule update --init
    ```
    Be aware that path/to/odoo (or path/to/server-tools) has to be a local clone
    of a repository, because it won't work if you copy a submodule from another project.

## Docker

### Build of the image

In a development environment, building the image is rarely necessary. The
production images are built by Travis. Furthermore, In the development
environment we share the local (source code) folders with the container using
`volumes` so we don't need to `COPY` the files in the container.

Building the image is required when:

* you start to work on the project
* the base image (`camptocamp/odoo-project:10.0`) has been updated and you need
  the new version
* the local Dockerfile has been modified (for example when dependency or addons
  repository is added)

Building the image is a simple command:

```bash
# build the docker image locally (--pull pulls the base images before building the local image)
docker-compose build --pull
```

You could also first pull the base images, then run the build:

```bash
docker-compose pull
docker-compose build
```


### Usage

When you need to launch the services of the composition, you can either run them in foreground or in background.

```bash
docker-compose up
```
Will run the services (postgres, odoo, nginx) in foreground, mixing the logs of all the services.

```bash
docker-compose up -d
```
Will run the services (postgres, odoo, nginx) in background.

When it is running in background, you can show the logs of one service or all of them (mixed):

```bash
docker-compose logs odoo      # show logs of odoo
docker-compose logs postgres  # show logs of postgres
docker-compose logs nginx     # show logs of nginx
docker-compose logs           # show all logs
```

And you can see the details of the running services with:

```bash
docker-compose ps
```

In the default configuration, the Odoo port changes each time the service is
started.  Some prefer to always have the same port, if you are one of them, you
can create your own configuration file or adapt the default one locally.

To know the port of the running Odoo, you can use the command `docker ps` that
shows information about all the running containers or the subcommand `port`:

```bash
docker ps
docker-compose port odoo 8069  # for the service 'odoo', ask the corresponding port for the container's 8069 port
```

This command can be used to open directly a browser which can be nicely aliased (see later).

```bash
export BROWSER="chromium-browser --incognito" # or firefox --private-window
$BROWSER $(docker-compose port odoo 8069)
```

Last but not least, we'll see other means to run Odoo, because `docker-compose
up` is not really good when it comes to real development with inputs and
interactions such as `pdb`.

**docker-compose exec** allows to *enter* in a already running container, which
can be handy to inspect files, check something, ...

```bash
# show odoo configuration file (the container name is found using 'docker ps')
docker-compose exec odoo cat /opt/odoo/etc/odoo.cfg
# run bash in the running odoo container
docker exec odoo bash
```

**docker run** spawns a new container for a given service, allowing the
interactive mode, which is exactly what we want to run Odoo with pdb.
This is probably the command you'll use the most often.

The `--rm` option drops the container after usage, which is usually what we
want.

```bash
# start Odoo (use workers=0 for dev)
docker-compose run --rm odoo odoo --workers=0 ... additional arguments
# start Odoo and expose the port 8069 to the host on the port 80
docker-compose run --rm -p 80:8069 odoo odoo
# open an odoo shell
docker-compose run --rm odoo odoo shell
```

`workers=0` let you use your `pdb` interactive mode without trouble otherwise
you will have to deal with one trace per worker that catched a breakpoint.
Plus, it will stop the annoying `bus is not available` errors.

### Handy aliases

Finally, a few aliases suggestions:

```bash
alias doco='docker-compose'
alias docu='docker-compose up -d'
alias docl='docker-compose logs'
alias docsh='docker-compose run --rm odoo odoo shell'
alias dood='docker-compose run --rm odoo odoo'
alias bro='chromium-browser --incognito $(docker-compose port odoo 8069)'
# run anthem song. Just run `dood_anthem songs.install.foo::baz`
alias dood_anthem='docker-compose run --rm odoo anthem'
# run odoo w/ connector jobrunner. Just run `dood_conn` instead of dood (connector v9)
alias dood_conn='docker-compose run --rm odoo odoo --workers=0 --load=web,connector'
# run odoo w/ queue_job jobrunner. Just run `dood_queue` instead of dood (connector v10)
alias dood_queue='docker-compose run --rm odoo odoo --workers=0 --load=web,queue_job'
# run odoo without marabunta migration. Just run `dood_nomig`
alias dood_nomig='docker-compose run --rm -e MIGRATE=False odoo odoo --workers=0'
```

and to speed up your testing sessions (see [core images' test doc](https://github.com/camptocamp/docker-odoo-project#running-tests)):

```bash
# setup test database. Just run `dood_test_setup`
alias dood_test_setup='docker-compose run --rm -e DB_NAME=testdb odoo testdb-gen -i base'
# reuse testdb and install or update modules on demand. Just run `dood_test_update -i/u something`
alias dood_test_update='docker-compose run --rm -e DB_NAME=testdb odoo testdb-update'
# run tests using pytest. Just run `dood_test_run path/to/your/module`
# NOTE: you need to run dood_test_update 1st IF xml or models have been updated
alias dood_test_run='docker-compose run --rm -e DB_NAME=testdb odoo pytest -s'
# run tests using std odoo test machinery (eg: you need an HttpCase). Just run `dood_test_run_odoo -u module`
alias dood_test_run_odoo='docker-compose run --rm -e DEMO=True -e DB_NAME=testdb -e MIGRATE=False odoo odoo --workers=0 --test-enable --stop-after-init'
```

Usage of the aliases / commands:
```bash

# Start all the containers in background
docu

# Show status of containers
doco ps

# show logs of odoo or postgres
docl odoo
docl db

# run a one-off command in a container
doco run --rm odoo bash

# open a chromium browser on the running odoo
bro

# stop all the containers
doco stop

# upgrade module and or run tests
dood -u my_module [--test-enable]

# if you are using the `connector` remember to pass the `load` attribute
dood --load=web,connector
```

### Working with several databases

The Docker image only starts on one database and does not allow switching
databases at runtime. However, you can and should use several databases on your
postgres container for enabling databases for different usages or development.

This can be very well combined with [restoration of databases from
dumps](how-to-backup-and-restore-volumes.md#backup-and-restore-with-dumps).

The default database name will be the one configured in the variable `DB_NAME`
in `docker-compose.yml` (usually `odoodb`).

So if you just start a new odoo container:

```
docker-compose run --rm odoo
```

You will work on `odoodb`. Now let's say you want to work on a database with odoo demo data and no marabunta migration:

```
docker-compose run --rm -e MIGRATE=False -e DB_NAME=odoo_demo odoo
```

And then you restore a dump in a `prod` database. You can start it with:

```
docker-compose run --rm -e DB_NAME=prod odoo
```

If you inspect the databases, you should find your 3 databases:

```
$ docker-compose run --rm odoo psql -l
[...]
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges
-----------+----------+----------+------------+------------+-----------------------
 odoo      | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 odoodb    | odoo     | UTF8     | en_US.utf8 | en_US.utf8 |
 prod      | odoo     | UTF8     | en_US.utf8 | en_US.utf8 |
 odoo_demo | odoo     | UTF8     | en_US.utf8 | en_US.utf8 |
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
```

And you can work as you want on any of them by changing the `DB_NAME`.


### Extra dev packages

You might want to use additional python packages while developing (eg: pdbpp, ipdb, etc).
You can easily add them in `odoo/dev_requirements.txt` and build again odoo container:

```bash
echo "pdbpp" >> odoo/dev_requirements.txt
doco build odoo
```
