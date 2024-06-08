import requests

BASE_URL = 'https://hacker-news.firebaseio.com/v0/'
ITEM_URL = BASE_URL + 'item/'
TOP_STORIES_URL = BASE_URL + 'topstories.json'

def get_top_stories_ids():
  return requests.get(TOP_STORIES_URL).json()

def get_item(id):
  string_id = str(id)
  return requests.get(f'{ITEM_URL + string_id}.json').json()

def get_top_n_stories(n):
  top_stories_ids = get_top_stories_ids()
  top_n_ids = [x for i, x in enumerate(top_stories_ids) if i < n]
  return [get_item(x) for x in top_n_ids]

printable = [str(x) for x in get_top_n_stories(5)]
print('\n'.join(printable))
