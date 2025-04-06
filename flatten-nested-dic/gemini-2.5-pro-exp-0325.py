import collections.abc # Used for robust type checking (Mapping, Sequence)

def flatten_dict(nested_dict, parent_key='', sep='.'):
    """
    Flattens a nested dictionary or list into a single-level dictionary.

    Keys in the flattened dictionary represent the path to the original value,
    separated by the specified separator. List elements are accessed by their index.

    Args:
        nested_dict (dict or list): The dictionary or list to flatten.
        parent_key (str, optional): The base key string to prepend to flattened keys.
                                    Used internally for recursion. Defaults to ''.
        sep (str, optional): The separator to use between keys in the path.
                             Defaults to '.'.

    Returns:
        dict: A flattened dictionary.

    Raises:
        TypeError: If the initial input `nested_dict` is not a dictionary or list
                   (unless it's a base case value during recursion).

    Examples:
        >>> flatten_dict({"a": {"b": 1, "c": {"d": 2}}})
        {'a.b': 1, 'a.c.d': 2}

        >>> flatten_dict({"a": [1, {"b": 2}, 3]})
        {'a.0': 1, 'a.1.b': 2, 'a.2': 3}

        >>> flatten_dict({})
        {}

        >>> flatten_dict({"a": None, "b": []})
        {'a': None} # Empty lists result in no keys

        >>> flatten_dict({"key.with.dots": 1, "nested": {"n": 2}})
        {'key.with.dots': 1, 'nested.n': 2}

        >>> flatten_dict([{"a": 1}, {"b": 2}]) # Handles top-level list
        {'0.a': 1, '1.b': 2}

        >>> flatten_dict({"a": {"b": {}}}, sep='_')
        {} # Empty inner dict results in no keys

        >>> flatten_dict(5) # Raises TypeError on initial call
        Traceback (most recent call last):
            ...
        TypeError: Input must be a dictionary or list for top-level call.
    """
    items = {}

    # Helper function for recursion to manage scope and initial type check
    def _flatten_recursive(obj, current_prefix):
        nonlocal items # Modify the 'items' dict in the outer scope

        # --- Dictionary Handling ---
        if isinstance(obj, collections.abc.Mapping):
            # If the dictionary is empty, it contributes no keys to the flattened dict
            if not obj:
                # Optional: uncomment below if you want empty dicts represented,
                # e.g., {'a': {}} -> {'a': {}} or {'a': None}
                # if current_prefix: # Avoid adding empty key for top-level empty dict
                #     items[current_prefix] = {} # or None, or a special marker
                pass
            else:
                for k, v in obj.items():
                    # Create the new key path
                    # Use str(k) to handle non-string keys gracefully
                    new_key = f"{current_prefix}{sep}{str(k)}" if current_prefix else str(k)
                    # Recurse
                    _flatten_recursive(v, new_key)

        # --- List/Sequence Handling (excluding strings) ---
        # We check for Sequence but explicitly exclude str and bytes which are sequences too
        elif isinstance(obj, collections.abc.Sequence) and not isinstance(obj, (str, bytes)):
             # If the list is empty, it contributes no keys
            if not obj:
                 # Optional: uncomment below if you want empty lists represented
                 # if current_prefix:
                 #    items[current_prefix] = [] # or None, or a special marker
                 pass
            else:
                for i, v in enumerate(obj):
                    # Create the new key path using the index
                    new_key = f"{current_prefix}{sep}{str(i)}" if current_prefix else str(i)
                    # Recurse
                    _flatten_recursive(v, new_key)

        # --- Base Case: Non-dict, Non-list Value ---
        else:
            # Only add if there's a key (handles the case of flattening a primitive directly)
            # Although the main function checks the top-level type, this ensures
            # correctness during recursion if the structure is unusual.
            if current_prefix: # Ensure we don't add an item with an empty key
                items[current_prefix] = obj
            # If the initial call was with a primitive and no parent_key,
            # 'items' would remain empty, which is reasonable behavior.

    # --- Initial Call & Type Check ---
    # Check if the top-level object is suitable for flattening
    # Allow dicts and lists as top-level inputs
    if not isinstance(nested_dict, (collections.abc.Mapping, list)):
         # If the very first item passed isn't a dict or list, it cannot be "flattened"
         # in the intended way. Raise an error.
         # Note: Primitives encountered *during* recursion are handled by the base case.
         raise TypeError("Input must be a dictionary or list for top-level call.")

    _flatten_recursive(nested_dict, parent_key)
    return items

# --- Examples ---
print("Example 1:")
print(flatten_dict({"a": {"b": 1, "c": {"d": 2}}}))
# Expected: {'a.b': 1, 'a.c.d': 2}

print("\nExample 2 (with list):")
print(flatten_dict({"a": [1, {"b": 2, "c": [3, 4]}, 5]}))
# Expected: {'a.0': 1, 'a.1.b': 2, 'a.1.c.0': 3, 'a.1.c.1': 4, 'a.2': 5}

print("\nExample 3 (empty dict):")
print(flatten_dict({}))
# Expected: {}

print("\nExample 4 (empty inner structures):")
print(flatten_dict({"a": None, "b": [], "c": {"d": {}}}))
# Expected: {'a': None}

print("\nExample 5 (keys with dots):")
print(flatten_dict({"key.with.dots": 1, "nested": {"n": 2}}))
# Expected: {'key.with.dots': 1, 'nested.n': 2}

print("\nExample 6 (custom separator):")
print(flatten_dict({"a": {"b": 1, "c": 2}}, sep='_'))
# Expected: {'a_b': 1, 'a_c': 2}

print("\nExample 7 (top-level list):")
print(flatten_dict([{"a": 1}, {"b": 2}, 3]))
# Expected: {'0.a': 1, '1.b': 2, '2': 3}

print("\nExample 8 (non-string keys):")
print(flatten_dict({1: {"a": "val1"}, "key": {2: "val2"}}))
# Expected: {'1.a': 'val1', 'key.2': 'val2'}

# Example demonstrating the initial type error
try:
    print("\nExample 9 (invalid top-level input):")
    flatten_dict(123)
except TypeError as e:
    print(f"Caught expected error: {e}")
