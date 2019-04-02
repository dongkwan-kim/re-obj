import pickle
import os
from collections.abc import Iterable, Sized, Callable

from termcolor import cprint


class ReusableObject(object):
    
    def dump(self, file_name: str, file_path="./", msg=None, color="blue"):
        with open(os.path.join(file_path, file_name), 'wb') as f:
            pickle.dump(self, f)

        if msg is None:
            msg = "Dump {} ({})".format(os.path.join(file_path, file_name), self.__class__.__name__)
        elif msg and isinstance(msg, Callable):
            msg = msg(self)
        cprint(msg, color)

    def load(self,
             file_name: str,
             attr_black_list: list = None,
             attr_white_list: list = None,
             file_path="./",
             msg=None,
             color="green") -> bool:
        try:
            with open(os.path.join(file_path, file_name), 'rb') as f:
                loaded = pickle.load(f)
                for k, v in loaded.__dict__.items():
                    if (attr_black_list is None and attr_white_list is None) or \
                       (attr_black_list and k not in attr_black_list) or \
                       (attr_white_list and k in attr_white_list):
                        setattr(self, k, v)
            ret = True
        except Exception as e:
            print('Load Failed: {0}.\n'.format(file_name), str(e))
            ret = False

        if msg is None:
            if ret:
                msg = "Load {} ({})".format(os.path.join(file_path, file_name), self.__class__.__name__)
            else:
                msg = "Load Failed {} ({})".format(os.path.join(file_path, file_name), self.__class__.__name__)
        elif msg and isinstance(msg, Callable):
            msg = msg(self, ret)

        cprint(msg, color)
        return ret

    def dump_dist(self, file_prefix: str, num: int, file_path="./"):
        for i in range(num):
            iterable_key_to_size = {k: len(v) for k, v in self.__dict__.items()
                                    if isinstance(v, Iterable) and isinstance(v, Sized)}
        # TODO
        raise NotImplementedError

    def load_dist(self, file_prefix: str, file_path="./"):
        # TODO
        for i, file in enumerate([f for f in os.listdir(file_path) if f.startswith(file_prefix)]):
            pass
        raise NotImplementedError
