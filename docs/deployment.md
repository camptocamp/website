# Deployment

As we use GitHub private repositories and the private Docker Hub, you must be
able to connect to both of them. This guide is not complete yet as the
deployment process is not yet a thing.

### Docker
```bash
docker login
# answer to the questions
```

### GitHub

Ensure to have a private SSH key with the authorizations to connect to our
private GitHub.  You can also spare to clone the repository and only transfer
the `test.yml` file.

### Deploy

The first time:
```bash
git clone git@github.com:camptocamp/smartliberty_odoo.git -b 10.0.x smartliberty-test  # use the tag you want to deploy
cd smartliberty-test
docker-compose -f test.yml up -d
```

For the next times:

If the application is not yet in production and you need to delete the database
to run again the setup scenario, you have to run (**it drops the database, be
cautious**):
```bash

# DO NOT RUN THIS ON THE DEFINITIVE PRODUCTION SERVER
docker-compose -f test.yml rm -v

```

Upgrade:
```bash
cd smartliberty-test
git fetch origin
git checkout 10.0.x  # use the tag you want to deploy
docker-compose -f test.yml up -d
```
