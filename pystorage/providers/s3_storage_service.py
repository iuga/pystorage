from sys import exc_info
from six import reraise
from pystorage.providers.storage_service import StorageService
from pystorage.errors import StorageProviderError


class S3StorageService(StorageService):
    """
    AWS S3 Storage Service
    ======================
    This service provides a mechanism for storing objects in binary files on a S3 bucket.
    """
    def __init__(self, bucket='my.bucket', folder='my.folder', region='eu-west-1'):
        self.bucket = bucket
        self.folder = folder
        try:
            import boto3  # NOQA
            self.bucket = boto3.resource('s3', region_name=region).Bucket(bucket)
        except ModuleNotFoundError:
            raise StorageProviderError("AWS Client not installed. Please execute pip install boto3")

    def __getitem__(self, key):
        """
        Lookup/Retrieve a value given its key and raise KeyError if not present.

        :param key: string|numeric value used as unique key.
        :raise KeyError if the key/file was not found
        """
        try:
            obj = self.bucket.Object('{}{}'.format(self.folder, key))
            return obj.get()['Body'].read()
        except Exception:
            reraise(KeyError, KeyError("Error opening the content from S3"), exc_info()[2])

    def __setitem__(self, key, value):
        """
        Insert a key/value pair into the storage.

        :param key: string|integer key
        :param value: object to store
        :raise KeyError if there was a problem saving the key/value
        """
        try:
            obj = self.bucket.Object('{}{}'.format(self.folder, key))
            obj.put(Body=value)
        except Exception:
            reraise(KeyError, KeyError("Error saving the content"), exc_info()[2])

    def __contains__(self, key):
        """
        Test for membership. Does not affect the storage order.
        load() does a HEAD request for a single key, which is fast, even if the object in question
        is large or you have many objects in your bucket.

        :param key: string|integer key
        :return True if the key exists, False otherwise
        """
        try:
            print('{}{}'.format(self.folder, key))
            self.bucket.Object('{}{}'.format(self.folder, key)).load()
        except Exception as ex:
            return ex.response['Error']['Code'] == 404
        else:
            return True

    def __delitem__(self, key):
        """
        Remove an item from the storage.

        :param key: string|integer key
        """
        try:
            self.bucket.Object('{}{}'.format(self.folder, key)).delete()
        except Exception:
            reraise(KeyError, KeyError("Error deleting the content"), exc_info()[2])

    def __len__(self):
        """
        Returns the number of items stored.

        :return integer with the length of the collection
        """
        return len([_ for _ in self.bucket.objects.all() if self.folder in _.key])
