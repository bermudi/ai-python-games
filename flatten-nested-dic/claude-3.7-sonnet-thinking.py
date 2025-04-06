def flatten_dict(nested_dict, prefix="", separator="."):
    """
    Transforms a nested dictionary into a flattened one with dot-separated path keys.

    Args:
        nested_dict: The nested dictionary or list to flatten
        prefix: The current key prefix (used in recursion)
        separator: The character to use between path segments (default ".")

    Returns:
        A flattened dictionary where keys represent paths to values

    Examples:
        >>> flatten_dict({"a": {"b": 1, "c": {"d": 2}}})
        {'a.b': 1, 'a.c.d': 2}

        >>> flatten_dict({"a": [{"b": 1}, {"c": 2}]})
        {'a.0.b': 1, 'a.1.c': 2}
    """
    result = {}

    # Handle non-dict/non-list value at top level
    if not isinstance(nested_dict, (dict, list)):
        if not prefix:  # Top-level scalar value
            return {"": nested_dict}
        result[prefix] = nested_dict
        return result

    # Handle empty collections
    if not nested_dict:
        if prefix:  # Only add if we have a prefix
            result[prefix] = nested_dict
        return result

    # Handle dictionary
    if isinstance(nested_dict, dict):
        for key, value in nested_dict.items():
            # Create new prefix - handle non-string keys by converting them
            key_str = str(key)
            new_prefix = f"{prefix}{separator}{key_str}" if prefix else key_str

            # Recursively flatten nested structures
            if isinstance(value, (dict, list)):
                if not value:  # Handle empty nested collections
                    result[new_prefix] = value
                else:
                    nested_result = flatten_dict(value, new_prefix, separator)
                    result.update(nested_result)
            else:
                result[new_prefix] = value

    # Handle list
    elif isinstance(nested_dict, list):
        for i, value in enumerate(nested_dict):
            # Create new prefix with index
            new_prefix = f"{prefix}{separator}{i}" if prefix else str(i)

            # Recursively flatten nested structures
            if isinstance(value, (dict, list)):
                if not value:  # Handle empty nested collections
                    result[new_prefix] = value
                else:
                    nested_result = flatten_dict(value, new_prefix, separator)
                    result.update(nested_result)
            else:
                result[new_prefix] = value

    return result
