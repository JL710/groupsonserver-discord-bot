import os
import json
import discord


class Settings(dict):
    def __init__(self, file_path):
        self.file_path = file_path
        if os.path.isfile(self.file_path):
            with open(self.file_path, "r") as file:
                content = json.load(file)
        else:
            with open(self.file_path, "w") as file:
                json.dump({}, file) 
                content = {}
        self.update(content)

    def __setitem__(self, key, item):
        with open(self.file_path, "w") as file:
            json.dump(self, file)
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))


def load_token(path: str):
    with open(path, "r") as file:
        return file.read()


def error_embed(title: str, message: str):
    return discord.Embed(title=title, description=message, color=discord.Color.from_rgb(255, 0, 0))


def create_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
