from itertools import chain

def register_mapping(func, *args):
    for (model, admin) in chain(*args):
        func(model, admin)
