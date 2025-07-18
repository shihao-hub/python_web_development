from apps.core.utils import Cache

if __name__ == '__main__':
    cache = Cache()
    cache.set("1", "2")
    cache.set("1", "3")
    print(cache)
    print(cache.get("1"))
