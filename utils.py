import operator as op
import random


def ix_map_from_list(l):
    return {e: i for i, e in enumerate(l)}


def random_max(d: dict, minimize=False):
    """
    Return a random key amongst the items in a dictionary with the maximum value.
    """
    if minimize:
        optimal_val = min(d.items(), key=op.itemgetter(1))[1]
    else:
        optimal_val = max(d.items(), key=op.itemgetter(1))[1]
    eligible_keys = [key for key, val in d.items() if val == optimal_val]
    return random.choice(eligible_keys)
