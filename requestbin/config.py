import os
from urllib.parse import urlparse

PORT_NUMBER = 4000

ENABLE_CORS = False
CORS_ORIGINS = "*"

BIN_TTL = 48*3600
MAX_RAW_SIZE = int(os.environ.get('MAX_RAW_SIZE', 1024*10))
MAX_REQUESTS = 20
CLEANUP_INTERVAL = 3600

STORAGE_BACKEND = "requestbin.storage.memory.MemoryStorage"
REDIS_URL = os.environ.get("REDIS_URL")
if REDIS_URL is not None:
    STORAGE_BACKEND = "requestbin.storage.redis.RedisStorage"
    _url_parts = urlparse(REDIS_URL)
    REDIS_HOST = _url_parts.hostname
    REDIS_PORT = _url_parts.port
    REDIS_PASSWORD = _url_parts.password
    REDIS_DB = _url_parts.fragment
    REDIS_PREFIX = "requestbin"

REVERSE_PROXY = os.environ.get('REVERSE_PROXY', None)

REALM = os.environ.get('REALM', 'local')

if REALM == 'prod':
    DEBUG = False
    FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", FLASK_SESSION_SECRET_KEY)
    BUGSNAG_KEY = os.environ.get("BUGSNAG_KEY", BUGSNAG_KEY)
    IGNORE_HEADERS = """
X-Varnish
X-Forwarded-For
X-Heroku-Dynos-In-Use
X-Request-Start
X-Heroku-Queue-Wait-Time
X-Heroku-Queue-Depth
X-Real-Ip
X-Forwarded-Proto
X-Via
X-Forwarded-Port
""".split("\n")[1:-1]

else:
    DEBUG = True
    FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", "N1BKhJLnBqLpexOZdklsfDKFJDKFadsfs9a3r324YB7B73AglRmrHMDQ9RhXz35")
    BUGSNAG_KEY = ""
    IGNORE_HEADERS = []
