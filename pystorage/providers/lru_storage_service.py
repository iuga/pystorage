from pylru import lrucache
from pystorage.providers.storage_service import StorageService


class LRUStorageService(StorageService):
    """
    Least recently used (LRU) Storage Service
    =========================================
    When accessing large amounts of data is deemed too slow, a common speed up technique is to keep
    a small amount of the data in memory. The first time a particular piece of data is accessed, the
    slow method must be used. However, the data is then stored in the cache so that the next time you
    need it you can access it much more quickly.
    The goal is to retain those items that are more likely to be retrieved again soon.
    A good approximation to the optimal algorithm is based on the observation that data that have been
    heavily used in the last few instructions will probably be heavily used again in the next few.
    When performing LRU caching, you always throw out the data that was least recently used.
    """
    def __init__(self, memory_blocks=10):
        """
        Initialize the LRU storage with the maximum number of key/value pairs you want the storage to hold.

        :param memory_blocks: Integer size of the storage.
        """
        self.storage = lrucache(memory_blocks)

    def __getitem__(self, key):
        """
        Lookup/Retrieve a value given its key and raise KeyError if not present.

        :param key: string|numeric value used as unique key.
        :return object
        :raises KeyError if the key was not found
        """
        return self.storage[key]

    def __setitem__(self, key, value):
        """
        Insert a key/value pair into the storage.

        :param key: string|integer key
        :param value: object to store
        """
        self.storage[key] = value

    def __contains__(self, key):
        """
        Test for membership. Does not affect the storage order.

        :param key: string|integer key
        :return True if the key exists, False otherwise
        """
        return key in self.storage

    def __delitem__(self, key):
        """
        Remove an item from the storage.

        :param  key: string|integer key
        """
        del self.storage[key]

    def __len__(self):
        """
        Returns the number of items stored in the cache.
        x will be less than or equal to the defined memory_blocks

        :return integer with the length of the collection
        """
        return len(self.storage)
