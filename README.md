# jubilant-robot
HackerNews API Aggregator

# Setup

- Create a venv: `virtualenv -p python3 venv`
- Enter your venv: `source ./venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

# Usage

- Enter your venv: `source ./venv/bin/activate`
- Run the server: `python main.py`. This will start the server on localhost, port 4000.
- You can access the endpoints however you like. e.g. using curl: `curl 0.0.0.0:4000/endpoint_1`
- The HackerNews endpoints will return HTTP status 503 Service Unavailable until the program has retrieved sufficient data from the HN API.
- There is a "hello world" url you can use to test the server is running in the meantime: `curl 0.0.0.0:4000/hello`

# Design

The logic in this exercise is relatively simple. The hard part is dealing with slow queries to an API that is out of our control. I considered caching items once they'd been retrieved, but that would ignore comments that were added after initial retrieval. I settled for a background job that calculates each result and stores it in a cache. The endpoints just return the most recently cached values. 

To add testing, the HackerNewsAPI should be changed so that the data collection methods are passed in to the module. This would probably mean wrapping the module in a class. This would mean that the class could operate on fake, canned data, making it deterministic and testable.

There are many improvements that could be made. 
- It could be packaged in a Docker container
- It could be made configurable (job frequency, ports, etc)
- Split logic from IO more agressively

# Assumptions
- "10 most used words for the first 100 comments for the top 30 stories" means the most used words across _all_ of those 3000 comments; this endpoint returns 10 words.
- Endpoint 3 should return the _10_ most used words in all comments; this number is not specified.
