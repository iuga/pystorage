import pytest
from pystorage.errors import StorageProviderError
from pystorage.providers.service_provider import ServiceProvider
from pystorage.providers.services.lru_storage_service import LRUStorageService


def test_getting_a_lrustorage_instance_works_correctly():
    """
    Test that a LRUStorageService instance was created correctly.
    """
    service = ServiceProvider().create(ServiceProvider.STORAGE_LRU)
    assert isinstance(service, LRUStorageService)


def test_getting_an_invalid_service():
    """
    If I try to create an invalid service, ServiceProviderError should be raised.
    """
    with pytest.raises(StorageProviderError):
        ServiceProvider().create('not.found')
