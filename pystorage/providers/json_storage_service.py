import json
from os import remove
from os.path import join, isfile
from sys import exc_info
from six import reraise
from glob import glob
from pystorage.providers.storage_service import StorageService


class JSONStorageService(StorageService):
    """
    JSON Storage Service
    ======================
    This service provides a mechanism for storing dictionary-like objects in json files.
    Please remember to enforce de UTF-8/LATIN-1 policy, as the content is stored in a text-like format.

    Example:
    - path = /tmp/test/
    storage['hello'] = 'world'    # > /tmp/test/hello.storage.json (Create)
    storage['hello'] = 'country'  # > /tmp/test/hello.storage.json (Override)
    storage['my'] = 'data'        # > /tmp/test/my.storage.json (Create)
    data = storage['hello']       # < /tmp/test/hello.storage.json (read)

    """
    def __init__(self, path='/tmp', suffix='storage.json'):
        self.path = path
        self.suffix = suffix

    def __getitem__(self, key):
        """
        Lookup/Retrieve a value given its key and raise KeyError if not present.

        :param key: string|numeric value used as unique key.
        :raise KeyError if the key/file was not found
        """
        filename = join(self.path, '{}.{}'.format(key, self.suffix))
        try:
            with open(filename, 'r') as pf:
                content = json.load(pf)
        except (KeyError, IOError, UnicodeDecodeError, AttributeError, EOFError, ImportError, IndexError):
            reraise(KeyError, KeyError("Error opening the content from {}".format(filename)), exc_info()[2])
        return content

    def __setitem__(self, key, value):
        """
        Insert a key/value pair into the storage.

        :param key: string|integer key
        :param value: object to store
        :raise KeyError if there was a problem saving the key/value
        """
        filename = join(self.path, '{}.{}'.format(key, self.suffix))
        try:
            with open(filename, 'w') as pf:
                json.dump(value, pf)
        except (KeyError, IOError, UnicodeDecodeError):
            reraise(KeyError, KeyError("Error saving the content in {}".format(filename)), exc_info()[2])

    def __contains__(self, key):
        """
        Test for membership. Does not affect the storage order.

        :param key: string|integer key
        :return True if the key exists, False otherwise
        """
        filename = join(self.path, '{}.{}'.format(key, self.suffix))
        return isfile(filename)

    def __delitem__(self, key):
        """
        Remove an item from the storage.

        :param key: string|integer key
        """
        filename = join(self.path, '{}.{}'.format(key, self.suffix))
        remove(filename)

    def __len__(self):
        """
        Returns the number of items stored.

        :return integer with the length of the collection
        """
        return len(glob(join(self.path, '*.{}'.format(self.suffix))))
