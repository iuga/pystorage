# PyStorage
Lightweight Python Cache Storage Library

## Installing

Install and update using GitHub:

```
pip install git+https://github.com/iuga/pystorage.git
```

## Loading and Creating Storages
The `StorageProvider` class a factory instance that you should use to create and instantiate new Services.

```python
from pystorage.storage_provider import StorageProvider

# Create a new instance of a LRU Storage Service:
service = StorageProvider().create(
    StorageProvider.STORAGE_LRU,
    *args, **kwargs
)
```

It also provides a mechanism to register new custom services and use them:

```python
# Register a new Service into the ServiceProvider. Then create a new instance.
provider = ServiceProvider().register('my.service', MyStorageService)
service = provider.create('my.service', 5)
```

### Built-in providers
There are a few services that you get out of the box. All of these are contained in the `StorageProvider`:
- **Storage Services**: Define an abstract interface for all the storage services using the Python container types. If you want to define your own storage inherit this class.
- **JSONStorageService** `STORAGE_JSON`: This service provides a mechanism for storing key - values objects using a JSON file.
- **LRUStorageService** `STORAGE_LRU`: When accessing large amounts of data is deemed too slow, a common speed up technique is to keep a small amount of the data in memory. The first time a particular piece of data is accessed, the slow method must be used. However, the data is then stored in the cache so that the next time you need it you can access it much more quickly. The goal is to retain those items that are more likely to be retrieved again soon. A good approximation to the optimal algorithm is based on the observation that data that have been heavily used in the last few instructions will probably be heavily used again in the next few. When performing LRU caching, you always throw out the data that was least recently used.
- **PickleStorageService** `STORAGE_PICKLE`: This service provides a mechanism for serializing and deserializing a group of objects into disk using the pickle protocol.
- **GZipPickleStorageService** `STORAGE_PICKLE_GZIP`: This service provides a mechanism for serializing and deserializing a group of objects into disk using the pickle protocol and compressing it using Lempel-Ziv coding (GZIP). This method should be slower than the pickle storage but should save some disk space.
- **S3StorageService** `STORAGE_S3`: This service provides a mechanism for serializing and deserializing a group of binary objects on AWS S3.
- **DiskLRUStorageService** `STORAGE_DISKLRU`: Set a file count limit and remove the least recently used file when the limit is reached.
- **VolatileStorageService** `STORAGE_VOLATILE`: Dictionary storage with auto-expiring values for caching purposes. Expiration happens on any access, object is locked during cleanup from expired values.
- **RedisStorageService** `STORAGE_REDIS`: In-memory data structure store, used as a database, cache and message broker on plain text.
- **RedisJSONStorageService** `STORAGE_REDIS`: In-memory data structure store, used as a database, cache and message broker on json format.

## Use-Case: Simple Storage
Let's store our dictionary information in `json` format:
```python
>>> from pystorage.storage_provider import StorageProvider
>>> storage = StorageProvider().create(StorageProvider.STORAGE_JSON)
>>> storage['some_key'] = {
        'text': 'Hello World!'
    }
>>> storage['some_key']
```
```
{'text': 'Hello World!'}
```
While the file `/tmp/some_key.storage.json` contains:
```
{"text": "Hello World!"}
```
We can check the size of the storage:
```python
>>> len(storage)
```
```
1
```
While if we want to remove the entry:
```python
>>> del storage['some_key']
>>> storage['some_key']
```
Will raise a `KeyError` exception because the key does not exist anymore.

## Use-Case: Storage with expiration (Volatile)
Let's store our dictionary information using any provider, like `pickle`, but removing the data after some provided expiration time in seconds:

```python
>>> from pystorage.storage_provider import StorageProvider
>>> pkl_storage = StorageProvider().create(StorageProvider.STORAGE_PICKLE)
>>> storage = StorageProvider().create(
        StorageProvider.STORAGE_VOLATILE,
        storage=pkl_storage,
        expiration=5
    )
>>> storage['key'] = 'value'
>>> storage['key']
```
```
'value'
```
After 5 seconds the same command will raise a `KeyError` and the pickle file will not exist anymore.

## Use-Case: Store files on Amazon S3
Let's use AWS S3 storage to save and load files from a specific bucket:
```python
>>> from pystorage.storage_provider import StorageProvider
>>> pkl_storage = StorageProvider().create(
        StorageProvider.STORAGE_S3,
        bucket='my.bucket',
        folder='some/folder/'
    )
>>> with open('test.html', 'rb') as fp:
        storage['test.html'] = fp.read()
>>> 'test.html' in storage
```
```
True
```
```python
>>> with open('test_download.html', 'wb') as fp:
        fp.write(storage['test.html'])
```

## Use-Case: Store with a file count limit
Special for cases when your local storage is limited, you can use this method to storage files locally until you reach a desired file count limit. When this limit is reached the least recenlty used key is removed to make space.
```python
>>> from pystorage.storage_provider import StorageProvider
>>> storage = StorageProvider().create(
        StorageProvider.STORAGE_DISKLRU
        limit=100
    )
>>> for i in range(0, 150):
>>>     storage[f'key.{i}'] = f'value.{i}'
>>> len(storage)
```
```
100
```

## Use-Case: Store on Redis

```python
import redis

redis_client = redis.from_url("redis://localhost:6379")

storage = StorageProvider().create(
    StorageProvider.STORAGE_REDIS,
    redis_client=redis_client
)

>>> storage['key'] = 'value'
>>> storage['key']
```
```
'value'
```
