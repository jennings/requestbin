# RequestBin

Accepts HTTP requests and displays what was received to you.

Originally Created by [Jeff Lindsay](http://progrium.com)

# License

MIT


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

If you want to store data in Redis instead of in memory, provided the REDIS_URL
environment variable:

```
Simple:
    redis://server.example.com

Full syntax:
    redis://unused:secret@redis-server.example.com:6379#0
    Server:     redis-server.example.com:6379
    Password:   secret
    Database:   0
```

## Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Deploy your own instance using Heroku
Create a Heroku account if you haven't, then grab the RequestBin source using git:

`$ git clone git://github.com/Runscope/requestbin.git`

From the project directory, create a Heroku application:

`$ heroku create`

Add Heroku's redis addon:

`$ heroku addons:add heroku-redis`

Set an environment variable to indicate production:

`$ heroku config:set REALM=prod`

Now just deploy via git:

`$ git push heroku master`

It will push to Heroku and give you a URL that your own private RequestBin will be running.



Contributors
------------
 * Barry Carlyon <barry@barrycarlyon.co.uk>
 * Jeff Lindsay <progrium@gmail.com>
