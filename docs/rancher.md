# Automated Rancher build

## Travis deployment

When committing on master branch, if tests pass, Travis will:

1. Build a docker image
2. Push it on DockerHub with the tag: `latest`
3. Upgrade the stack on rancher with image `latest`

Thus, the test server will be continuously upgraded.

## Rancher templates

The templates for rancher are defined in [rancher folder](../rancher).

In which we find [latest](../rancher/latest). This templates defines the
rancher stack automatically upgraded by Travis.

## Rancher environment setup

In order to configure the variables for the container built on Rancher by
Travis, the files `rancher.env.gpg` are used. Each environment in `rancher/` contains its own file.

For every operation below, a password will be asked. The passwords are stored in Lastpass in the following sites:

* Rancher: latest/rancher.env.gpg
* Rancher: integration/rancher.env.gpg
* Rancher: production/rancher.env.gpg

If you've just created the rancher.env files, you should create the corresponding Lastpass secure note of type database.
You should also add rancher.env in project .gitignore file, only rancher.env.gpg should be commited.

To decrypt a file, run:

```
$ gpg rancher.env.gpg
```

Or directly source the content of a file (which is only composed of environment variables used by `rancher-compose`) with:

```
$ source <(gpg2 -d rancher.env.gpg)
```

When you have to modify the file, you have to re-encrypt the file, which is done with:

```
$ gpg2 --symmetric --cipher-algo AES256 rancher.env
```

## Travis

Each succeeded build on the master branch triggers:

* push of a new `latest` image on the Docker Hub
* deploy of the `latest` image on the test environment

The password to decrypt the gpg environment file (Rancher:
latest/rancher.env.gpg) is needed by Travis, so we store it in a `secure`
environment.

To get this secure variable:
 * Install, if needed, the travis command line client

 ```bash
 sudo gem install travis
 ```

 * Authenticate yourself on travis server with your github account.

 ```bash
 travis login
 ```

 * Then ask Travis to encrypt your gpg password (stored on Lastpass)

 ```bash
 travis encrypt -r camptocamp/<repository_name> rancher_env_password=xxxxxxx
 ```

The output of this command (should be like `secure=encrypted key`should be added in the `global` section in `env` of
`travis.yml`.

