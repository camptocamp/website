<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# How to add a new addons repository

External addons repositories such as the OCA ones are integrated in
the project using git submodules.

To add a new one, you only have to add the submodule:

```
git submodule add -b 10.0 git@github.com:OCA/sale-workflow.git odoo/external-src/sale-workflow
git add odoo/external-src/sale-workflow
```

And to add it in the `ADDONS_PATH` environment variable of the
[Dockerfile](../odoo/Dockerfile). As the `Dockerfile` is modified, a rebuild is
required.

Then commit the new submodule

```
git add odoo/Dockerfile
git commit -m"..."
```
