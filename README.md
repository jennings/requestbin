# RequestBin

Accepts HTTP requests and displays what was received. Useful for testing
webhooks or other requests made by an application.

Originally Created by [Jeff Lindsay](http://progrium.com)

# License

MIT

# Configuration

Configuration is set via environment variables.

The only value that must be set in production is `SECRET_KEY`. This is the key
used by Flask to sign session data. Not setting this allows sessions to be
forged and the "private" flag on a bin will not be safe.

| Environment variable | Description                                                               | Default      |
| -------------------- | ------------------------------------------------------------------------- | ------------ |
| `SECRET_KEY`         | Signing key used by Flask to sign session cookies.                        | (see source) |
| `MAX_RAW_SIZE`       | Maximum incoming request size to save. Larger requests will be truncated. | 10240        |

In addition, mutliple storage backends are supported.

## Redis backend

If the environment variable `REDIS_URL` is set, the Redis backend is used.

| Environment variable | Description                                                | Default         |
| -------------------- | ---------------------------------------------------------- | --------------- |
| `REDIS_URL`          | Redis connection string `redis://127.0.0.1:6379`           | N/A             |
| `BIN_TTL`            | Number of seconds that bins will be kept with no activity. | 172800 (2 days) |

## Azure Blob Storage backend

If the environment variable `AZURE_BLOB_STORAGE_URL` is set, the Azure Blob Storage backend is used.

| Environment variable        | Description                                                                 | Default      |
| --------------------------- | --------------------------------------------------------------------------- | ------------ |
| `AZURE_BLOB_STORAGE_URL`    | Storage account URL, like `https://<accountname>.blob.core.windows.net`     | N/A          |
| `AZURE_BLOB_CONTAINER_NAME` | Blob container to use.                                                      | "requestbin" |
| `AZURE_BLOB_PREFIX`         | Prefix to prepend to blob names. Include a trailing slash: `"my/requests/"` | No prefix    |

Azure Blob storage does not support automatically expiring blobs, so you should
configure a [lifecycle policy][lifecycle-management] to delete old blobs:

[lifecycle-management]: https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-overview

```json
{
  "rules": [
    {
      "name": "DeleteOldBins",
      "enabled": true,
      "type": "Lifecycle",
      "definition": {
        "filters": {
          "blobTypes": ["blockBlob"],
          "prefixMatch": ["requestbin/bins/"]
        },
        "actions": {
          "baseBlob": {
            "delete": { "daysAfterModificationGreaterThan": 2 }
          }
        }
      }
    }
  ]
}
```

## Memory backend

If no other backend is configured, bins will be stored in memory and lost when the process stops.

# Hosting

## Docker

There's a [Docker image](https://hub.docker.com/r/jennings/requestbin/) you can
use. The service in the container listens on port 8000:

```bash
cp .env.sample /path/to/environment_variables.txt
nano /path/to/environment_variables.txt

# Create and start the container
docker container run -d --name requestbin                           \
                     -p 8000:8000                                   \
                     --env-file /path/to/environment_variables.txt  \
                     --restart unless-stopped                       \
                     jennings/requestbin
```

If you want to store data in Redis instead of in memory, set the REDIS_URL
environment variable, using the syntax
`redis://h:<password>@<hostname>:<port>/<db>`. For example, to use db3 with no
password: `redis://redis.example.com/3`

## Heroku

### Via deploy button

Click this and follow the instructions:

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

### Via manual labor

Clone this repository. From the project directory, create a Heroku application:

`$ heroku create`

Add Heroku's redis addon:

`$ heroku addons:add heroku-redis`

Set an environment variable to indicate production:

`$ heroku config:set REALM=prod`

Now just deploy via git:

`$ git push heroku master`

It will push to Heroku and give you a URL that your own private RequestBin will be running.

## Contributors

- Barry Carlyon <barry@barrycarlyon.co.uk>
- Jeff Lindsay <progrium@gmail.com>
