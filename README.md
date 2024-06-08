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

# Assumptions
- "10 most used words for the first 100 comments for the top 30 stories" means the most used words across _all_ of those 3000 comments; this endpoint returns 10 words.
- Endpoint 3 should return the _10_ most used words in all comments; this number is not specified.
