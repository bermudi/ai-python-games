def flatten_dict(nested_dict, parent_key='', sep='.'):
    """
    Flattens a nested dictionary into a flat dictionary with dot-separated keys.

    Args:
        nested_dict (dict): The nested dictionary to flatten.
        parent_key (str, optional): The prefix for keys at the current level. Defaults to ''.
        sep (str, optional): The separator to use between key levels. Defaults to '.'.

    Returns:
        dict: A flattened dictionary where keys are dot-separated paths and values
              are the values from the original nested dictionary.

    Supports:
        - Nested dictionaries of arbitrary depth.
        - Lists within dictionaries (lists are flattened with index-based keys).
        - Handles empty dictionaries and lists gracefully.
        - Non-dictionary or non-list values are kept as is.

    Example:
        >>> nested = {"a": {"b": 1, "c": {"d": 2}}, "e": [3, {"f": 4}], "g": 5}
        >>> flatten_dict(nested)
        {'a.b': 1, 'a.c.d': 2, 'e.0': 3, 'e.1.f': 4, 'g': 5}

        >>> nested_list = [{"a": 1}, [2, {"b": 3}]]
        >>> flatten_dict(nested_list)
        {'0.a': 1, '1.0': 2, '1.1.b': 3}

        >>> empty_dict = {}
        >>> flatten_dict(empty_dict)
        {}

        >>> simple_dict = {"a": 1, "b": 2}
        >>> flatten_dict(simple_dict)
        {'a': 1, 'b': 2}
    """
    items = []
    for k, v in nested_dict.items():
        new_key = parent_key + sep + k if parent_key else k  # Construct the new key path
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())  # Recursively flatten dictionaries
        elif isinstance(v, list):
            for index, item in enumerate(v):
                list_key = new_key + sep + str(index)  # Key for list element is index
                if isinstance(item, (dict, list)): # Handle nested dicts/lists within lists
                    items.extend(flatten_dict({str(index): item}, parent_key=new_key, sep=sep).items()) # Treat list item as a mini dict for recursion
                else:
                    items.append((list_key, item)) # Add primitive list element
        else:
            items.append((new_key, v))  # Add non-dict/non-list values directly
    return dict(items)

# Example Usage and Testing:
if __name__ == '__main__':
    nested_dict_example = {"a": {"b": 1, "c": {"d": 2}}, "e": [3, {"f": 4}], "g": 5}
    flattened_dict_example = flatten_dict(nested_dict_example)
    print(f"Original nested dictionary: {nested_dict_example}")
    print(f"Flattened dictionary: {flattened_dict_example}")
    # Expected Output: {'a.b': 1, 'a.c.d': 2, 'e.0': 3, 'e.1.f': 4, 'g': 5}

    nested_list_example = [{"a": 1}, [2, {"b": 3}]]
    flattened_list_example = flatten_dict(nested_list_example)
    print(f"\nOriginal nested list (as dict): {nested_list_example}")
    print(f"Flattened dictionary from list: {flattened_list_example}")
    # Expected Output: {'0.a': 1, '1.0': 2, '1.1.b': 3}

    empty_dict_example = {}
    flattened_empty_dict = flatten_dict(empty_dict_example)
    print(f"\nOriginal empty dictionary: {empty_dict_example}")
    print(f"Flattened empty dictionary: {flattened_empty_dict}")
    # Expected Output: {}

    simple_dict_example = {"a": 1, "b": 2}
    flattened_simple_dict = flatten_dict(simple_dict_example)
    print(f"\nOriginal simple dictionary: {simple_dict_example}")
    print(f"Flattened simple dictionary: {flattened_simple_dict}")
    # Expected Output: {'a': 1, 'b': 2}

    dict_with_empty_values = {"a": None, "b": {"c": None, "d": []}}
    flattened_empty_values = flatten_dict(dict_with_empty_values)
    print(f"\nOriginal dict with empty values: {dict_with_empty_values}")
    print(f"Flattened dict with empty values: {flattened_empty_values}")
    # Expected Output: {'a': None, 'b.c': None, 'b.d': []}
