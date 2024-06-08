from collections import Counter
from itertools import chain
import requests

BASE_URL = "https://hacker-news.firebaseio.com/v0/"
ITEM_URL = BASE_URL + "item/"
TOP_STORIES_URL = BASE_URL + "topstories.json"

# HackerNews' API refers to comments as kids
# https://github.com/HackerNews/API?tab=readme-ov-file#items
COMMENTS = "kids"
TEXT = "text"
TYPE = "type"

TYPE_STORY = "story"


def get_top_stories_ids():
    return requests.get(TOP_STORIES_URL).json()

def get_item(id):
    string_id = str(id)
    return requests.get(f"{ITEM_URL + string_id}.json").json()


def get_first_n_items_by_id(ids, n):
    first_n_ids = get_first_n_from_sequence(ids, n)
    return [get_item(x) for x in first_n_ids]

def get_top_n_stories(n):
    top_stories_ids = get_top_stories_ids()
    stories = []
    while len(stories) < n and len(top_stories_ids) > 0:
        id = top_stories_ids.pop(0)
        item = get_item(id)
        if TYPE in item and item[TYPE] == TYPE_STORY:
            stories.append(item)
    return stories


def get_first_n_comments_from_item(item, n):
    ids = item.get(COMMENTS, [])
    return get_first_n_items_by_id(ids, n)


def get_all_comments_from_item_recursive(item):
    if COMMENTS not in item:
        return []
    else:
        all_comments = []
        comments = [get_item(x) for x in item[COMMENTS]]
        all_comments.extend(comments)
        for comment in comments:
            all_comments.extend(get_all_comments_from_item_recursive(comment))
        return all_comments


def endpoint_1():
    stories = get_top_n_stories(100)
    comments = chain.from_iterable(
        get_first_n_comments_from_item(x, 50) for x in stories
    )
    return list(comments)


def endpoint_2():
    stories = get_top_n_stories(30)
    comments = chain.from_iterable(
        get_first_n_comments_from_item(x, 100) for x in stories
    )
    texts = [x[TEXT] for x in comments if TEXT in x]
    words = chain.from_iterable(x.split() for x in texts)
    counted_words = Counter(words)
    return counted_words.most_common(10)


def endpoint_3():
    stories = get_top_n_stories(10)
    comments = chain.from_iterable(
        get_all_comments_from_item_recursive(x) for x in stories
    )
    texts = [x[TEXT] for x in comments if TEXT in x]
    words = chain.from_iterable(x.split() for x in texts)
    counted_words = Counter(words)
    return counted_words.most_common(10)


# functions below this comment should be pure
def get_first_n_from_sequence(seq, n):
    return [x for i, x in enumerate(seq) if i < n]
