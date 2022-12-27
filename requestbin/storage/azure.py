from ..models import Bin

from requestbin import config
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

class AzureBlobStorage():
    def __init__(self, bin_ttl):
        credential = DefaultAzureCredential()
        container_name = config.AZURE_BLOB_CONTAINER_NAME
        self.prefix = config.AZURE_BLOB_PREFIX
        blob_client = BlobServiceClient(config.AZURE_BLOB_STORAGE_URL, credential=credential)
        self.client = blob_client.get_container_client(container_name)

    def _blob_name(self, name):
        return '{}bins/{}'.format(self.prefix, name)

    def _write(self, bin):
        blob_name = self._blob_name(bin.name)
        self.client.upload_blob(blob_name, data=bin.dump(), overwrite=True)

    def create_bin(self, private=False):
        bin = Bin(private)
        self._write(bin)
        return bin

    def create_request(self, bin, request):
        bin.add(request)
        self._write(bin)

    def count_bins(self):
        return None

    def count_requests(self):
        return None

    def avg_req_size(self):
        return None

    def lookup_bin(self, name):
        blob_name = self._blob_name(name)
        blob = self.client.download_blob(blob_name)
        serialized_bin = blob.readall()
        try:
            bin = Bin.load(serialized_bin)
            return bin
        except TypeError:
            self.client.delete_blob(blob_name) # clear bad data
            raise KeyError("Bin not found")
