import requests

BASE_URL = 'https://hacker-news.firebaseio.com/v0/'
ITEM_URL = BASE_URL + 'item/'
TOP_STORIES_URL = BASE_URL + 'topstories.json'

# HackerNews' API refers to comments as kids
# https://github.com/HackerNews/API?tab=readme-ov-file#items
COMMENTS = 'kids'

def get_top_stories_ids():
  return requests.get(TOP_STORIES_URL).json()

def get_item(id):
  string_id = str(id)
  return requests.get(f'{ITEM_URL + string_id}.json').json()


def get_first_n_from_sequence(seq, n):
  return [x for i, x in enumerate(seq) if i < n]

def get_first_n_items_by_id(ids, n):
  first_n_ids = get_first_n_from_sequence(ids, n)
  return [get_item(x) for x in first_n_ids]

def get_top_n_stories(n):
  top_stories_ids = get_top_stories_ids()
  return get_first_n_items_by_id(top_stories_ids, n)

def get_first_n_comments_from_item(item, n):
  ids = item[COMMENTS]
  return get_first_n_items_by_id(ids, n)


stories = get_top_n_stories(5)
printable = [str(x) for x in stories] 
print('\n'.join(printable))

print

printable = [str(x) for x in get_first_n_comments_from_item(stories[1], 50)]
print('\n'.join(printable))

