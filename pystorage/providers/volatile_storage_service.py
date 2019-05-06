from time import time
from threading import RLock
from pystorage.providers.storage_service import StorageService


class VolatileStorageService(StorageService):
    """
    Volatile Storage Service
    ========================
    Dictionary with auto-expiring values for caching purposes.
    Expiration happens on any access, object is locked during cleanup from expired values.

    Example:
        storage = VolatileStorageService(expiration=5)
        storage['the_key'] = 'the_value'
        # The value is accessible for 5 seconds
        assert 'the_value' == storage['the_key']
        # After five seconds ( expiration time ) the value will be deleted
        assert 'the_key' not in storage['the_key']

    Note: Iteration over dict and also keys() do not remove expired values!
    """
    def __init__(self, storage={}, expiration=3600):
        """
        Initialize the Storage with a Thread locking mechanism. Also, sets the expiration in
        seconds. The stored values not live more than that time.

        :param expiration: seconds to keep the value alive.
        """
        self.expiration = expiration
        self.storage = storage
        self.lock = RLock()

    def __getitem__(self, key):
        """
        Lookup/Retrieve a value given its key and raise KeyError if not present.
        If the key/value is expired raise a KeyError.

        :param key: string|numeric value used as unique key.
        :raise KeyError if the key/file was not found or is expired.
        """
        with self.lock:
            value = self.storage[key]
            print(time())
            print(value[0])
            print(time() - value[0])
            if (time() - value[0]) > self.expiration:
                del self.storage[key]
                raise KeyError(key)
            return value[1]

    def __setitem__(self, key, value):
        """
        Insert a key/value pair into the storage.

        :param key: string|integer key
        :param value: object to store
        :raise KeyError if there was a problem saving the key/value
        """
        with self.lock:
            self.storage[key] = (time(), value)

    def __contains__(self, key):
        """
        Test for membership. Does not affect the storage expiration.

        :param key: string|integer key
        :return True if the key exists, False otherwise
        """
        try:
            self[key]
        except KeyError:
            return False
        return True

    def __delitem__(self, key):
        """
        Remove an item from the storage.

        :param key: string|integer key
        """
        with self.lock:
            del self.storage[key]

    def __len__(self):
        """
        Returns the number of items stored in the cache.
        Note: It does not remove expired values!

        :return integer with the length of the collection
        """
        with self.lock:
            return len(self.storage)
