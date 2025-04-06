def flatten_dict(nested, parent_key='', sep='.'):
    """
    Flattens a nested dictionary into a dot-separated key dictionary.
    Supports lists and handles edge cases.

    Args:
        nested (dict or list): The input nested dictionary or list.
        parent_key (str): The base key string (used in recursion).
        sep (str): The separator for key paths (default is dot).

    Returns:
        dict: A flattened dictionary with dot-separated keys.
    """
    items = {}

    if isinstance(nested, dict):
        for k, v in nested.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
            items.update(flatten_dict(v, new_key, sep=sep))
    elif isinstance(nested, list):
        for i, v in enumerate(nested):
            new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
            items.update(flatten_dict(v, new_key, sep=sep))
    else:
        items[parent_key] = nested

    return items
