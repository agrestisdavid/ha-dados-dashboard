# This file is part of Dictdiffer.
#
# Copyright (C) 2015 CERN.
# Copyright (C) 2017, 2019 ETH Zurich, Swiss Data Science Center, Jiri Kuncar.
#
# Dictdiffer is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more
# details.

"""Utils gathers helper functions, classes for the dictdiffer module."""

import math
import sys

num_types = int, float
EPSILON = sys.float_info.epsilon


class PathLimit:
    """Class to limit recursion depth during the dictdiffer.diff execution."""

    def __init__(self, path_limits=None, final_key=None) -> None:
        """Initialize a dictionary structure to determine a path limit.

        :param path_limits: list of keys (tuples) determining the path limits
        :param final_key: the key used in the dictionary to determin if the
                          path is final

            >>> pl = PathLimit( [('foo', 'bar')] , final_key='!@#$%FINAL')
            >>> pl.dict
            {'foo': {'bar': {'!@#$%FINAL': True}}}
        """
        self.final_key = final_key if final_key else "!@#$FINAL"
        self.dict = {}
        if path_limits:
            for key_path in path_limits:
                containing = self.dict
                for key in key_path:
                    try:
                        containing = containing[key]
                    except KeyError:
                        containing[key] = {}
                        containing = containing[key]

                containing[self.final_key] = True

    def path_is_limit(self, key_path):
        """Query the PathLimit object if the given key_path is a limit.

        >>> pl = PathLimit( [('foo', 'bar')] , final_key='!@#$%FINAL')
        >>> pl.path_is_limit( ('foo', 'bar') )
        True
        """
        containing = self.dict
        for key in key_path:
            try:
                containing = containing[key]
            except KeyError:
                try:
                    containing = containing["*"]
                except KeyError:
                    return False

        return containing.get(self.final_key, False)


def create_dotted_node(node):
    """Create the *dotted node* notation for the dictdiffer.diff patches.

    >>> create_dotted_node( ['foo', 'bar', 'baz'] )
    'foo.bar.baz'
    """
    if all(isinstance(x, str) for x in node):
        return ".".join(node)
    return list(node)


def get_path(patch):
    """Return the path for a given dictdiffer.diff patch."""
    if patch[1] != "":
        keys = patch[1].split(".") if isinstance(patch[1], str) else patch[1]
    else:
        keys = []
    keys = [*keys, patch[2][0][0]] if patch[0] != "change" else keys
    return tuple(keys)


def dot_lookup(source, lookup, parent=False):
    """Allow you to reach dictionary items with string or list lookup.

    Recursively find value by lookup key split by '.'.

        >>> from dictdiffer.utils import dot_lookup
        >>> dot_lookup({'a': {'b': 'hello'}}, 'a.b')
        'hello'

    If parent argument is True, returns the parent node of matched
    object.

        >>> dot_lookup({'a': {'b': 'hello'}}, 'a.b', parent=True)
        {'b': 'hello'}

    If node is empty value, returns the whole dictionary object.

        >>> dot_lookup({'a': {'b': 'hello'}}, '')
        {'a': {'b': 'hello'}}

    """
    if lookup is None or lookup in ("", []):
        return source

    value = source
    if isinstance(lookup, str):
        keys = lookup.split(".")
    elif isinstance(lookup, list):
        keys = lookup
    else:
        raise TypeError("lookup must be string or list")

    if parent:
        keys = keys[:-1]

    for key in keys:
        if isinstance(value, list):
            key = int(key)
        value = value[key]
    return value


def are_different(first, second, tolerance, absolute_tolerance=None):
    """Check if 2 values are different.

    In case of numerical values, the tolerance is used to check if the values
    are different.
    In all other cases, the difference is straight forward.
    """

    def _strip_string(value: str) -> str:
        # Remove cr
        value = value.replace("\n", " ")
        # make multiple spaces, 1 space
        value = " ".join(value.split())
        # trim start and end spaces
        return value.strip()

    if first == second:
        # values are same - simple case
        return False

    if isinstance(first, str) and isinstance(second, str):
        stripped_first = _strip_string(first)
        stripped_second = _strip_string(second)
        if stripped_first == stripped_second:
            return False

    first_is_nan, second_is_nan = bool(first != first), bool(second != second)  # noqa: PLR0124

    if first_is_nan or second_is_nan:
        # two 'NaN' values are not different (see issue #114)
        return not (first_is_nan and second_is_nan)
    if isinstance(first, num_types) and isinstance(second, num_types):
        # two numerical values are compared with tolerance
        return not math.isclose(
            first,
            second,
            rel_tol=tolerance or 0,
            abs_tol=absolute_tolerance or 0,
        )
    # we got different values
    return True
