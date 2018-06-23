

def ix_map_from_list(l):
    return {e: i for i, e in enumerate(l)}


def print_iteration(i, wait, message='Iteration {:,}'):
    if i % wait == 0:
        print(message.format(i))

