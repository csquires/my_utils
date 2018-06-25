import os


def ensure_dirs(paths):
    print(paths)
    if isinstance(paths, list):
        for path in paths:
            ensure_dirs(path)
    else:
        if not os.path.exists(os.path.dirname(paths)):
            os.makedirs(paths)


def save(save, load):
    def save_decorator(f):
        def wrapper(*args, **kwargs):
            if 'filename' in kwargs and kwargs['filename'] is not None:
                try:
                    return load(kwargs['filename'])
                except:
                    res = f(*args, **kwargs)
                    save(res, kwargs['filename'])
                    return res
            else:
                return f(*args, **kwargs)
        return wrapper

    return save_decorator


if __name__ == '__main__':
    # ensure_dirs usage
    ensure_dirs(['hi/hi/what.txt', 'test/hi.txt'])

    # @save decorator usage
    import numpy as np
    import json

    matrix_save = lambda mat, fn: np.savetxt(fn, mat)
    json_save = lambda obj, fn: json.dump(obj, open(fn, 'w'), indent=2)
    json_load = lambda fn: json.load(open(fn))


    @save(matrix_save, np.loadtxt)
    def rand_mat(filename=None):
        return np.random.uniform(size=(3,3))


    @save(json_save, json_load)
    def my_json(filename=None):
        return {'a': 1, 'b': [1, 2, 3]}

    a = rand_mat(filename='test_mat.txt')
    b = my_json()
    b = my_json(filename='test_json.json')
