import time
from fastapi import HTTPException  # Правильный импорт для FastAPI
from prometheus_client import Counter, Histogram

REQUEST_COUNTER = Counter(
    'api_requests_total',
    'Total number of API requests',
    ['endpoint', 'method', 'status_code']
)

LATENCY_HISTOGRAM = Histogram(
    'api_request_duration_seconds',
    'Histogram of request duration in seconds',
    ['endpoint'],
    buckets=[0.1, 0.3, 0.5, 1.0, 2.0, 5.0]
)

def measure_latency(endpoint_name: str):
    def decorator(func):

        async def wrapper(*args, **kwargs):
            start_time = time.time()
            status_code = 500

            try:
                request = None
                for arg in args:
                    if hasattr(arg, 'method'):
                        request = arg
                        break
                if request is None:
                    for key, value in kwargs.items():
                        if hasattr(value, 'method'):
                            request = value
                            break

                method = request.method if request else 'unknown'

                result = await func(*args, **kwargs)
                status_code = 200
                return result

            except HTTPException as e:
                status_code = e.status_code
                raise

            except Exception:
                raise

            finally:
                latency = time.time() - start_time
                LATENCY_HISTOGRAM.labels(endpoint=endpoint_name).observe(latency)
                REQUEST_COUNTER.labels(
                    endpoint=endpoint_name,
                    method=method,
                    status_code=status_code
                ).inc()

        return wrapper
    return decorator
