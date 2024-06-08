from collections import Counter
from functools import cache
from itertools import chain
import requests

BASE_URL = 'https://hacker-news.firebaseio.com/v0/'
ITEM_URL = BASE_URL + 'item/'
TOP_STORIES_URL = BASE_URL + 'topstories.json'

# HackerNews' API refers to comments as kids
# https://github.com/HackerNews/API?tab=readme-ov-file#items
COMMENTS = 'kids'
TEXT = 'text'

def get_top_stories_ids():
  return requests.get(TOP_STORIES_URL).json()

@cache
def get_item(id):
  string_id = str(id)
  return requests.get(f'{ITEM_URL + string_id}.json').json()

def get_first_n_items_by_id(ids, n):
  first_n_ids = get_first_n_from_sequence(ids, n)
  return [get_item(x) for x in first_n_ids]

def get_top_n_stories(n):
  top_stories_ids = get_top_stories_ids()
  return get_first_n_items_by_id(top_stories_ids, n)

def get_first_n_comments_from_item(item, n):
  ids = item.get(COMMENTS, [])
  return get_first_n_items_by_id(ids, n)



# functions below this comment should be pure
def get_first_n_from_sequence(seq, n):
  return [x for i, x in enumerate(seq) if i < n]

def endpoint_1():
  top_stories_ids = get_top_stories_ids()
  stories = get_first_n_items_by_id(top_stories_ids, 100)
  comments = chain.from_iterable(get_first_n_comments_from_item(x, 50) for x in stories)
  return comments


def endpoint_2():
    top_stories_ids = get_top_stories_ids()
    stories = get_first_n_items_by_id(top_stories_ids, 30)
    comments = chain.from_iterable(get_first_n_comments_from_item(x, 100) for x in stories)
    texts = [x[TEXT] for x in comments if TEXT in x]
    words = chain.from_iterable(x.split() for x in texts)
    counted_words = Counter(words)
    return counted_words.most_common(10)
