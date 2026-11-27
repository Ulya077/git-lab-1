from unittest.mock import create_autospec
from lab3.storage.hero_repository import HeroRepository
from lab3.storage.caching_hero_repository import CachingHeroRepository

def test_loads_lazily():
    storage_mock = create_autospec(HeroRepository, instance=True)
    CachingHeroRepository(storage_mock)
    assert storage_mock.mock_calls == []

def test_reads_storage_only_once():
    storage_mock = create_autospec(HeroRepository, instance=True)
    storage_mock.find_all.return_value = []
    cache = CachingHeroRepository(storage_mock)

    cache.find_by_name("Артур")
    cache.find_by_name("Артур")

    storage_mock.find_all.assert_called_once_with()