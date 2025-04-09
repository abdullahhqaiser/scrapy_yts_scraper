import scrapy
import os
import json


class YtsSpider(scrapy.Spider):
    name = "yts"
    start_page = 1
    state_file = "yts_state.json"

    custom_settings = {
        "CONCURRENT_REQUESTS": 32,  # Run multiple requests at once
        "CONCURRENT_REQUESTS_PER_DOMAIN": 16,  # Limit requests to same domain
        "DOWNLOAD_TIMEOUT": 15,  # Don't wait too long for responses
        "RETRY_TIMES": 3,  # Try again if request fails
    }

    def start_requests(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                state = json.load(f)
                self.start_page = state.get("last_page", 1)
        else:
            self.log("State file not found. Starting from page 1.")

        url = f"https://yts.mx/api/v2/list_movies.json?&order_by=asc&page={self.start_page}&limit=50"

        yield scrapy.Request(
            url=url, callback=self.parse, meta={"page": self.start_page}
        )

    def save_state(self, page):
        state = {"last_page": page}
        with open(self.state_file, "w") as f:
            json.dump(state, f)

    def parse(self, response):
        data = response.json()

        movies = data.get("data", {}).get("movies", [])
        page = response.meta["page"]

        if movies:
            # Yield movie items
            for movie in movies:
                yield {
                    "id": movie.get("id"),
                    "title": movie.get("title"),
                    "year": movie.get("year"),
                    "rating": movie.get("rating"),
                    "genres": movie.get("genres"),
                }

            next_page = page + 1
            next_url = f"https://yts.mx/api/v2/list_movies.json?&order_by=asc&page={next_page}&limit=50"
            yield scrapy.Request(
                url=next_url, callback=self.parse, meta={"page": next_page}
            )
        else:
            self.log("No more movies found. Stopping the crawler.")
