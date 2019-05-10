from os import remove, makedirs
from os.path import join, isfile, dirname
from sys import exc_info
from six import reraise
from glob import glob
import gzip
from pickle import PickleError, dump, load, HIGHEST_PROTOCOL
from pystorage.providers.storage_service import StorageService


class GZipPickleStorageService(StorageService):
    """
    GZip Pickle Storage Service
    ===========================
    This service provides a mechanism for serializing and deserializing objects using the pickle protocol.
    Moreover, It have the feature to compress the pickle with GZip, saving disk space.
    You should initialize the Storage with a base folder, all the key/values are going to be
    saved in different files inside that selected folder.

    Example:
    - path = /tmp/test/
    storage['hello'] = 'world'    # > /tmp/test/hello.storage.pkl.gz (Create)
    storage['hello'] = 'country'  # > /tmp/test/hello.storage.gpk.gz (Override)
    storage['my'] = 'data'        # > /tmp/test/my.storage.pkl.gz (Create)
    data = storage['hello']       # < /tmp/test/hello.storage.pkl.gz (read)

    """
    def __init__(self, path, suffix='storage.pkl.gz'):
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
            with gzip.open(filename, 'r') as gzf:
                content = load(gzf)
        except (KeyError, IOError, PickleError, AttributeError, EOFError, ImportError, IndexError):
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
            makedirs(dirname(filename), exist_ok=True)
            with gzip.open(filename, 'wb') as pf:
                dump(value, pf, protocol=HIGHEST_PROTOCOL)
        except (KeyError, IOError, PickleError):
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
