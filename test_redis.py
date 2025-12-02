import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Test basic operations
r.set('test_key', 'Hello Redis!')
value = r.get('test_key')
print(f"Retrieved from Redis: {value}")

# Test with expiration
r.setex('temp_key', 10, 'This expires in 10 seconds')
print(f"Temp key exists: {r.exists('temp_key')}")