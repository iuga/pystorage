from pystorage.providers.storage_service import StorageService


class RedisStorageService(StorageService):
    """
    Redis Storage Service
    =====================
    In-memory data structure store, used as a database, cache and message broker.
    Expiration happens on any access, object is locked during cleanup from expired values.

    Example:
        import redis
        redis_client = redis.Redis(host='localhost', port=6379, db=0)

        storage = RedisStorageService(redis_client, expiration=5)

        storage['the_key'] = 'the_value'
        # The value is accessible for 5 seconds
        assert 'the_value' == storage['the_key']
        # After five seconds ( expiration time ) the value will be deleted
        assert 'the_key' not in storage['the_key']

    Note: Iteration over dict and also keys() do not remove expired values!
    """
    def __init__(self, redis_client, expiration=3600):
        """
        Initialize the Storage with a redis client and expiration

        :param expiration: seconds to keep the value alive.
        """
        self.redis_client = redis_client
        self.expiration = expiration

    def __getitem__(self, key):
        """
        Lookup/Retrieve a value given its key and raise KeyError if not present.
        If the key/value is expired raise a KeyError.

        :param key: string|numeric value used as unique key.
        :raise KeyError if the key/file was not found or is expired.
        """
        return self.redis_client.get(key)

    def __setitem__(self, key, value):
        """
        Insert a key/value pair into the storage.

        :param key: string|integer key
        :param value: object to store
        :raise KeyError if there was a problem saving the key/value
        """
        self.redis_client.set(key, value, ex=self.expiration)

    def __contains__(self, key):
        """
        Test for membership. Does not affect the storage expiration.

        :param key: string|integer key
        :return True if the key exists, False otherwise
        """
        return self.redis_client.exists(key)

    def __delitem__(self, key):
        """
        Remove an item from the storage.

        :param key: string|integer key
        """
        self.redis_client.delete(key)

    def __len__(self):
        """
        Returns the number of items stored in the cache.
        Note: It does not remove expired values!

        :return integer with the length of the collection
        """
        return len(self.redis_client.keys())
