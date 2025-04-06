def flatten_dict(d):
    def _flatten(x, name, result):
        if isinstance(x, dict):
            for k in x:
                new_name = f"{name}.{k}" if name else k
                _flatten(x[k], new_name, result)
        elif isinstance(x, list):
            for i, item in enumerate(x):
                new_name = f"{name}[{i}]" if name else f"[{i}]"
                _flatten(item, new_name, result)
        else:
            result[name] = x

    result = {}
    _flatten(d, "", result)
    return result
