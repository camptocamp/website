<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
-->
# Using automated tasks with Invoke

This project uses `invoke` to run some automated tasks.

First, install it with:

```bash

$ sudo pip install invoke

```

You can now see the list of tasks by running at the root directory:

```bash

$ invoke --list

```

The tasks are defined in `tasks.py`.

## Some tasks

### release.bump

release.bump is used to bump the current version number:
(see [releases.md](docs/releases.md#versioning-pattern) for more informations about versionning)

```
invoke release.bump --feature
# or
invoke release.bump --patch
```

--feature will change the minor version number (eg. 9.1.0 to 9.2.0).
--patch will change the patch version number (eg 9.1.0 to 9.1.1).

bump.release changes following files (which must be commited):
 * [odoo/VERSION](../odoo/VERSION): just contains the project version number, so this version is changed.
 * [HISTORY.rst](../HISTORY.rst): Rename Unreleased section with the new version number and create a new unreleased section.
 * rancher/integration/docker-compose.yml: Change the version of the docker image to use for the integration stack.

### project.sync

Copy files (such as docs) from the
[odoo-template](https://github.com/camptocamp/odoo-template).
It should be run at a regular basis.

```
invoke project.sync
```

### translate.generate

It generates or updates the pot translation file for an addon.
A new database will be created by the task, in which the addon will be
installed, so we guaranteed to have clean terms.

```
invoke translate.generate odoo/local-src/my_addon
# or
invoke translate.generate odoo/external-src/sale-workflow/my_addon
```

## Custom tasks

Alongside the core namespaces (release, project. translate), you can create
your own namespace for the need of the project. Dropping a Python file with an
invoke `@task` in the `tasks` directory will make it available in the `invoke`
commands. The namespace will be the name of the file. Let's say you add a
function named `world` decorated with `@task` in a file named `hello.py`, then
the command will be `invoke hello.world`.
