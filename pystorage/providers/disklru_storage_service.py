from os import remove, stat
from os.path import join
from glob import glob
from pystorage.providers.storage_service import StorageService


class DiskLRUStorageService(StorageService):
    """
    On Disk LRU Storage
    ===================
    This storage will store values in a internal pickle storage {storage}, until
    the lenght limit is reached. When the limit is reached, it purges the files removing the least
    accessed file considering the "time of most recent access" to determine the "least recently used" file.
    """
    def __init__(self, path='/tmp', suffix='storage.pkl', limit=100):
        from pystorage.storage_provider import StorageProvider
        self.storage = StorageProvider().create(
            StorageProvider.STORAGE_PICKLE,
            path=path,
            suffix=suffix
        )
        self.path = path
        self.suffix = suffix
        self.limit = limit

    def __getitem__(self, key):
        """
        Lookup/Retrieve a value given its key and raise KeyError if not present.

        :param key: string|numeric value used as unique key.
        :raise KeyError if the key/file was not found
        """
        return self.storage[key]

    def __setitem__(self, key, value):
        """
        Insert a key/value pair into the storage.

        :param key: string|integer key
        :param value: object to store
        :raise KeyError if th
        ere was a problem saving the key/value
        """
        self.purge()
        self.storage[key] = value

    def __contains__(self, key):
        """
        Test for membership. Does not affect the storage order.

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
        del self.storage[key]

    def __len__(self):
        """
        Returns the number of items stored.

        :return integer with the length of the collection
        """
        return len(self.storage)

    def purge(self):
        """
        Did the number reached the limit?
        Purge the least recently used file
        """
        if len(glob(join(self.path, '*.{}'.format(self.suffix)))) >= self.limit:
            file_sizes = [(stat(f).st_atime, f) for f in glob(join(self.path, '*.{}'.format(self.suffix)))]
            file_sizes = sorted(file_sizes, key=lambda t: t[0])
            remove(file_sizes[0][1])
