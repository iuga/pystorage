from pystorage.errors import StorageProviderError
from pystorage.providers.gzip_pickle_storage_service import GZipPickleStorageService
from pystorage.providers.volatile_storage_service import VolatileStorageService
from pystorage.providers.lru_storage_service import LRUStorageService
from pystorage.providers.json_storage_service import JSONStorageService
from pystorage.providers.pickle_storage_service import PickleStorageService
from pystorage.providers.s3_storage_service import S3StorageService
from pystorage.providers.disklru_storage_service import DiskLRUStorageService
from pystorage.providers.redis_storage_service import RedisStorageService
from pystorage.providers.redis_json_storage_service import RedisJSONStorageService


class StorageProvider(object):
    """
    Storage Provider
    ==============
    It's a factory instance that you can use to create and instantiate new storages.
    As a good practive, any new storage instance must be created through this provider.
    Also, it provides the mechanisms to extend registering new storages and use them.
    """
    STORAGE_LRU = 'storage.lru'
    STORAGE_JSON = 'storage.json'
    STORAGE_PICKLE = 'storage.pickle'
    STORAGE_PICKLE_GZIP = 'storage.pickle.gzip'
    STORAGE_VOLATILE = 'storage.volatile'
    STORAGE_S3 = 'storage.s3'
    STORAGE_DISKLRU = 'storage.disklru'
    STORAGE_REDIS = 'storage.redis'
    STORAGE_REDIS_JSON = 'storage.redis.json'

    def __init__(self):
        """
        Initialize the StorageProvider with a couple of know storage methods.
        """
        self.providers = {
            self.STORAGE_PICKLE_GZIP: GZipPickleStorageService,
            self.STORAGE_VOLATILE: VolatileStorageService,
            self.STORAGE_LRU: LRUStorageService,
            self.STORAGE_JSON: JSONStorageService,
            self.STORAGE_PICKLE: PickleStorageService,
            self.STORAGE_S3: S3StorageService,
            self.STORAGE_DISKLRU: DiskLRUStorageService,
            self.STORAGE_REDIS: RedisStorageService,
            self.STORAGE_REDIS_JSON: RedisJSONStorageService
        }

    def register(self, name, provider):
        """
        Register a new Storage into the Provider. After the registry you
        can use the provider to create new instances as a Factory.

        :example
            provider = StorageProvider().register('my.storage', MyStorage)

        :param name: the provider name. Please, use the convention. <type>.<name>
        :param provider: the provider class
        :returns self for concatenation
        """
        self.providers[name] = provider
        return self

    def create(self, name, *args, **kwargs):
        """
        Create a new instance of a Storage given by the name.
        *args and **kwargs are passed directly to the class constructor to
        generate the new instance.
        """
        try:
            return self.providers[name](*args, **kwargs)
        except KeyError:
            raise StorageProviderError("The storage method {} was not recognized".format(name))
