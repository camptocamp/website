# How to run a test server, the short way

This method is mostly for project managers or functional testers because it uses the pre-generated Docker images. Developers will prefer to use [Docker in development mode](development.md).

## Pre-requisite

Be sure to [install Docker and docker-compose](prerequisite.md) before going any further.

## Steps

1. Clone the project

        git clone git@github.com:camptocamp/smartliberty_odoo.git smartliberty

2. Login to Docker Hub (create an account on https://hub.docker.com/ if you
   don't have one yet and ask to be added to the Camptocamp team because this
   is a private project)

        docker login
        # answer to the questions

3. Start the composition

        cd smartliberty
        docker-compose -f test.yml -f local.yml pull
        docker-compose -f test.yml -f local.yml up

4. Open a browser on http://localhost (only one odoo instance at a time can be
   started because it uses the port 80, this can be changed in the
   configuration file if needed)

4. In `test.yml` you might want to adapt the odoo `image` version (so replace `latest` by a specific tag or branch).

5. If you want to drop your database, run:

        docker-compose -f test.yml -f local.yml rm -v
