from datetime import datetime, timedelta


class FlightResult(object):

    def __init__(self, provider, price, flight_num,
                 depart_time, arrive_time):
        self.provider = provider
        self.price = price
        self.flight_num = flight_num
        self.depart_time = depart_time
        self.arrive_time = arrive_time

    @property
    def agony(self):
        duration = self.arrive_time - self.depart_time
        return duration.total_seconds() / self.price

    def serialize(self):
        return {
            "provider": self.provider,
            "agony": self.agony,
            "price": self.price,
            "flight_num": self.flight_num,
            "depart_time": self.depart_time.isoformat(),
            "arrive_time": self.arrive_time.isoformat(),
        }


class Scraper(object):

    provider = None

    def run(self):
        self.results = []

        self.load_results()

        self.results.sort(key=lambda r: r.agony)

        return self.results

    def load_results(self):
        raise NotImplementedError

    def load_fake_results(self, range_iter):
        now = datetime.utcnow().replace(second=0, microsecond=0)
        for i in range_iter:
            price = 1000 - 10 * i
            flight_num = "UA%s" % (1000 + i)
            depart_time = now + timedelta(hours=i)
            arrive_time = depart_time + timedelta(hours=1, minutes=5 * i)
            self.add_result(
                price,
                flight_num,
                depart_time,
                arrive_time,
            )

    def add_result(self, price, flight_num,
                   depart_time, arrive_time):
        result = FlightResult(
            self.provider,
            price,
            flight_num,
            depart_time,
            arrive_time,
        )
        self.results.append(result)
