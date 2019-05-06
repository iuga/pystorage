class StorageService(object):
    """
    Storage Service (Interface)
    ===========================
    Define an abstract interface for all the storage services using the Python container types.
    You should inherit from this class if you want to define your own storage methodology.
    """
    def __getitem__(self, key):
        """
        Called to implement evaluation of self[key]:
        Lookup/Retrieve a value given its key and raises KeyError if key is not present.
        :param key: string|numeric value used as unique key.
        """
        raise NotImplementedError

    def __setitem__(self, key, value):
        """
        Called to implement assignment to self[key]:
        Insert a key/value pair into the storage.
        :param key: string|integer key
        :param value: object to store
        """
        raise NotImplementedError

    def __contains__(self, key):
        """
        Test for membership. Does not affect the storage order.
        :param key: string|integer key
        """
        raise NotImplementedError

    def __delitem__(self, key):
        """
        Remove an item from the storage.
        """
        raise NotImplementedError

    def __len__(self):
        """
        Called to implement the built-in function len().
        Should return the length of the object, an integer >= 0
        """
        raise NotImplementedError
