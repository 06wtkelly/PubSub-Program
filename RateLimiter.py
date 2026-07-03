from datetime import datetime, timedelta

class RateLimiter:

    def __init__(self):
        self.limits = {}

    def add_limit(self, topic: str, rate: int):
        limit = self.Limit(rate)
        self.limits[topic] = limit

    def get_limits(self):
        return self.limits

    def is_limited(self, topic) -> bool:
        limit = self.limits.get(topic, 0)
        timediff = (datetime.now() - limit.last_publish_time).total_seconds()
        return timediff < limit.rate

    def reset_limit(self, topic):
        limit = self.limits.get(topic, None)
        if limit: limit.update_last_publish_time()

    class Limit:

        def __init__(self, rate: int):
            self.rate = rate
            self.last_publish_time = datetime.now() - timedelta(seconds=self.rate)

        def update_last_publish_time(self):
            self.last_publish_time = datetime.now()
