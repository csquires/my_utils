import os
from scipy import sparse


# DECORATORS
def save_class(filename, saver, loader):
    def save_dec(f):
        def wrapper(self, *args, **kwargs):
            if callable(filename):
                signature = inspect.signature(f)
                kwargs_ = {
                    k: v.default
                    for k, v in signature.parameters.items() if v.default is not inspect.Parameter.empty
                }
                kwargs_.update(kwargs)
                full_filename = self.data_folder + filename(kwargs_)
            else:
                full_filename = self.data_folder + filename
            if os.path.exists(full_filename):
                return loader(full_filename)
            else:
                print('Generating %s' % full_filename)
                res = f(self, *args, **kwargs)
                print('Saving %s' % full_filename)
                saver(res, full_filename)
                return res
        return wrapper
    return save_dec


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


# READ/WRITE
def sparse_save(sparse_mat, filename):
    save_types = (sparse.csc_matrix, sparse.csr_matrix, sparse.bsr_matrix, sparse.dia_matrix, sparse.coo_matrix)
    if not isinstance(sparse_mat, save_types):
        sparse_mat = sparse_mat.tocoo()
    sparse.save_npz(filename, sparse_mat)


def np_save(mat, filename):
    np.save(filename, mat)


def write_list(l, filename):
    with open(filename, 'w') as f:
        for item in l:
            f.write('%s\n' % item)


def read_list(filename):
    l = []
    with open(filename) as f:
        for line in f.readlines():
            l.append(line.rstrip())
    return l


def write_set(s, filename):
    write_list(s, filename)


def read_set(s, filename):
    s = set()
    with open(filename) as f:
        for line in f.readlines():
            s.add(line.rstrip())
    return s


# OTHER
def ensure_dirs(paths):
    if isinstance(paths, list):
        for path in paths:
            ensure_dirs(path)
    else:
        if not os.path.exists(os.path.dirname(paths)):
            os.makedirs(paths)


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
