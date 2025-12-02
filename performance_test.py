import requests
import time
import statistics

BASE_URL = "http://localhost:5000"


def measure_endpoint(url, num_requests=10):
    """Measure response times for an endpoint"""
    times = []
    cache_hits = 0

    for i in range(num_requests):
        start = time.time()
        response = requests.get(url)
        elapsed = time.time() - start

        times.append(elapsed)
        cache_status = response.headers.get('X-Cache-Status', 'UNKNOWN')
        if cache_status == 'HIT':
            cache_hits += 1

        print(f"Request {i + 1}: {elapsed * 1000:.2f}ms - Cache: {cache_status}")

    print(f"\n{'=' * 50}")
    print(f"Total requests: {num_requests}")
    print(f"Cache hits: {cache_hits}")
    print(f"Cache hit rate: {cache_hits / num_requests * 100:.1f}%")
    print(f"Average time: {statistics.mean(times) * 1000:.2f}ms")
    print(f"Median time: {statistics.median(times) * 1000:.2f}ms")
    print(f"Min time: {min(times) * 1000:.2f}ms")
    print(f"Max time: {max(times) * 1000:.2f}ms")
    print(f"{'=' * 50}\n")


if __name__ == "__main__":
    print("Performance Test: GET /products\n")
    measure_endpoint(f"{BASE_URL}/products", num_requests=10)