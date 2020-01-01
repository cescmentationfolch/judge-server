import os
import traceback


def get_available_modules(regex, dirname, only=None, exclude=None):
    to_load = {i.group(1) for i in map(regex.match, os.listdir(dirname)) if i is not None}
    if only:
        to_load &= only
    if exclude:
        to_load -= exclude
    return sorted(to_load)


def load_module(name, ignored_errors):
    try:
        return import_module(name)
    except ImportError as e:
        if str(e) not in ignored_errors:
            traceback.print_exc()


def load_modules(to_load, load, attr, modules_dict, excluded_aliases, loading_message):
    print(loading_message)

    for name in to_load:
        module = load(name)

        if module is None or not hasattr(module, attr):
            continue

        cls = module.getattr(attr)
        if hasattr(cls, 'initialize') and not cls.initialize():
            continue

        if hasattr(module, 'aliases'):
            for alias in module.aliases():
                if alias not in excluded_aliases:
                    modules_dict[alias] = module
        else:
            module[name] = module

    print()