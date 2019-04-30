import pickle
import os
from collections.abc import Iterable, Sized, Callable

from termcolor import cprint

try:
    from .utils import is_savable
except ImportError:
    from utils import is_savable


class ReusableObject(object):

    # TODO: Distributively dump/load

    def dump(self,
             file_name: str,
             file_path=None,
             msg=None,
             color="blue"):

        file_path_and_name = os.path.join(file_path, file_name) if file_path is not None else file_name

        if file_path_and_name.startswith("~"):
            file_path_and_name = file_path_and_name.replace("~", os.path.expanduser("~"), 1)

        # Make the directory if it does not exist.
        real_dir = os.path.dirname(file_path_and_name)
        if not os.path.isdir(real_dir):
            os.makedirs(real_dir, exist_ok=False)

        # Handle non-savable attributes
        for k, v in self.__dict__.items():
            if not is_savable(v):
                setattr(self, k, None)

        # Dump
        with open(file_path_and_name, 'wb') as f:
            pickle.dump(self, f)

        # Print messages
        if msg is None:
            msg = "Dump {} ({})".format(file_path_and_name, self.__class__.__name__)
        elif msg and isinstance(msg, Callable):
            msg = msg(self)
        cprint(msg, color)

    def load(self,
             file_name: str,
             file_path=None,
             attr_black_list: list = None,
             attr_white_list: list = None,
             msg=None,
             color="green") -> bool:

        # Load
        file_path_and_name = os.path.join(file_path, file_name) if file_path is not None else file_name
        if file_path_and_name.startswith("~"):
            file_path_and_name = file_path_and_name.replace("~", os.path.expanduser("~"), 1)
        try:
            with open(file_path_and_name, 'rb') as f:
                loaded = pickle.load(f)
                for k, v in loaded.__dict__.items():
                    # Check black list and white list
                    if (attr_black_list is None and attr_white_list is None) or \
                       (attr_black_list and k not in attr_black_list) or \
                       (attr_white_list and k in attr_white_list):
                        setattr(self, k, v)
            err, ret = None, True
        except Exception as e:
            err, ret = str(e), False

        # Print messages
        if msg is None:
            if ret:
                msg = "Load {} ({})".format(file_path_and_name, self.__class__.__name__)
            else:
                msg = "Load Failed {} ({})\n{}".format(file_path_and_name, self.__class__.__name__, err)
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
