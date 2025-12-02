import json
import redis

# Redis configuration (NEW)
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
# Cache helper functions
CACHE_TTL = 300  # 5 minutes

def cache_product(product_id, product_dict):
    """
    Cache a single product.
    Key: "product:{id}"
    Value: JSON string of product dict
    TTL: 5 minutes
    """
    key = f"product:{product_id}"
    redis_client.setex(key,CACHE_TTL,json.dumps(product_dict))

def get_cached_product(product_id):
    """
    Retrieve cached product.
    Returns: dict if found, None if not in cache
    """
    key = f"product:{product_id}"
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def cache_all_products(products_list):
    """
    Cache list of all products.
    Key: "products:all"
    Value: JSON string of products list
    """
    key = "products:all"
    redis_client.setex(key, CACHE_TTL, json.dumps(products_list))

def get_cached_all_products():
    """
    Retrieve cached products list.
    Returns: list if found, None if not in cache
    """
    key = "products:all"
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def invalidate_cache(product_id=None):
    """
    Invalidate cache when data changes.
    If product_id provided: delete that product's cache
    Always delete "products:all" cache
    """
    # YOUR CODE: Use redis_client.delete()
    if product_id:
        redis_client.delete(f"product:{product_id}")
    redis_client.delete("products:all")