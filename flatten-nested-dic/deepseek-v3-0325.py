def flatten_dict(nested_dict, parent_key='', sep='.'):
    """
    Flatten a nested dictionary, with keys as dot-separated paths.
    Handles nested dictionaries, lists, and edge cases.

    Args:
        nested_dict: The dictionary to flatten
        parent_key: Used internally for recursion (default '')
        sep: Separator between keys (default '.')

    Returns:
        A flattened dictionary with dot-separated keys
    """
    flattened = {}

    for key, value in nested_dict.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key

        if isinstance(value, dict):
            # Recursively flatten dictionaries
            flattened.update(flatten_dict(value, new_key, sep))
        elif isinstance(value, (list, tuple)):
            # Handle lists by converting them to dict with indices as keys
            list_dict = {str(i): v for i, v in enumerate(value)}
            flattened.update(flatten_dict(list_dict, new_key, sep))
        else:
            # Base case: add the non-dict, non-list value
            flattened[new_key] = value

    return flattened


# Example usage and test cases
if __name__ == "__main__":
    # Basic test
    nested = {"a": {"b": 1, "c": {"d": 2}}}
    print(flatten_dict(nested))  # {'a.b': 1, 'a.c.d': 2}

    # Test with lists
    nested_with_list = {"a": {"b": [10, 20, 30], "c": {"d": 2}}}
    print(flatten_dict(nested_with_list))  # {'a.b.0': 10, 'a.b.1': 20, 'a.b.2': 30, 'a.c.d': 2}

    # Edge case: empty dictionary
    print(flatten_dict({}))  # {}

    # Edge case: already flat dictionary
    print(flatten_dict({"a": 1, "b": 2}))  # {'a': 1, 'b': 2}

    # Edge case: dictionary with None values
    print(flatten_dict({"a": None, "b": {"c": None}}))  # {'a': None, 'b.c': None}

    # Edge case: dictionary with mixed types
    mixed = {
        "user": {
            "name": "Alice",
            "age": 25,
            "hobbies": ["reading", "hiking"],
            "address": {
                "street": "123 Main",
                "zip": 12345
            },
            "metadata": None
        }
    }
    print(flatten_dict(mixed))
    # Output:
    # {
    #     'user.name': 'Alice',
    #     'user.age': 25,
    #     'user.hobbies.0': 'reading',
    #     'user.hobbies.1': 'hiking',
    #     'user.address.street': '123 Main',
    #     'user.address.zip': 12345,
    #     'user.metadata': None
    # }
