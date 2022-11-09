from azure.data.tables import TableClient
from azure.identity import DefaultAzureCredential
import time

from ..models import Bin

from requestbin import config

class AzureTableStorage():
    def __init__(self, bin_ttl):
        self.bin_ttl = bin_ttl
        self.client = TableClient(endpoint="", credential=DefaultAzureCredential())

    def _bin_key(self, name):
        return f"bin:{name}"

    def create_bin(self, private=False):
        # self.created = time.time()
        # self.private = private
        # self.color = random_color()
        # self.name = tinyid(8)
        # self.favicon_uri = solid16x16gif_datauri(*self.color)
        # self.requests = []
        # self.secret_key = os.urandom(24) if self.private else None
        bin = Bin(private)
        key = self._bin_key(bin.name)
        expiry = int(bin.created * 1000) + self.bin_ttl * 1000
        self.client.create_entity({
            "PartitionKey": key,
            "RowKey": "self",
            "expires": expiry,
            "created": bin.created,
            "private": bin.private,
        })
        self.client.create_entity({
            "PartitionKey": "expires",
            "RowKey": f"ts:{expiry}",
            "bin_key": key,
        })
        return bin

    def create_request(self, bin, request):
        bin_key = self._bin_key(bin.name)
        now = int(time.time())
        self.client.create_entity({
            "PartitionKey": bin_key,
            "RowKey": f"request:{now}",
            "request": request,
        })

    def count_bins(self):
        keys = self.redis.keys(self._bin_key("*"))
        return len(keys)

    def count_requests(self):
        return int(self.redis.get(self._request_count_key()) or 0)

    def avg_req_size(self):
        info = self.redis.info()
        return info['used_memory'] / info['db0']['keys'] / 1024

    def lookup_bin(self, name):
        key = self._bin_key(name)
        serialized_bin = self.redis.get(key)
        try:
            bin = Bin.load(serialized_bin)
            return bin
        except TypeError:
            self.redis.delete(key) # clear bad data
            raise KeyError("Bin not found")
