# YTS Movie Data Scraper

This project is a web scraper built with Scrapy that extracts movie data from the YTS API. It collects basic information about movies including titles, release years, ratings, and genres.

## Workflow

![Get State](https://github.com/user-attachments/assets/3c8908c4-e4f2-4222-b7a8-d35222214f14)


## Features

- Scrapes movie data from the YTS API
- Collects movie ID, title, year, rating, and genres
- Implements pagination to gather data across multiple pages
- Saves crawling state to allow resuming from the last page scraped
- Configures concurrency settings for efficient crawling

## Project Structure

```
yts_data/
├── scrapy.cfg               # Scrapy configuration file
├── yts_data/                # Project Python package
│   ├── __init__.py
│   ├── items.py             # Data structure definitions
│   ├── middlewares.py       # Custom middleware components
│   ├── pipelines.py         # Data processing components
│   ├── settings.py          # Project settings
│   └── spiders/             # Spider directory
│       ├── __init__.py
│       └── yts.py           # Main spider for YTS data
```

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install scrapy
   ```

## Usage

Run the spider with:

```
scrapy crawl yts -o movies.json
```

This command will start the scraper and save the output to a JSON file named `movies.json`.

To continue a previous crawl (the spider will automatically detect where it left off):

```
scrapy crawl yts -o movies.json -a resume=true
```

## Configuration

The spider includes the following custom settings:

- `CONCURRENT_REQUESTS`: 32 (Run multiple requests at once)
- `CONCURRENT_REQUESTS_PER_DOMAIN`: 16 (Limit requests to same domain)
- `DOWNLOAD_TIMEOUT`: 15 seconds (Don't wait too long for responses)
- `RETRY_TIMES`: 3 (Try again if request fails)

You can modify these settings in the spider file or in the project's `settings.py` file.

## How It Works

1. The spider starts by checking if a state file exists to determine the starting page
2. It makes requests to the YTS API to retrieve movie data
3. For each movie found, it extracts the ID, title, year, rating, and genres
4. It continues to the next page until no more movies are found
5. The state is saved after each page to allow resuming the crawl

## License

[Add your license information here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
