import json
import numpy as np

def load_matches(path, n_lines=-1, verbose=False, func=lambda item, args: True, args=None):
    """
    Walks through a JSON file and returns lines matching a function. This
    is an optimization over other json-parsing APIs, because this saves
    memory by preemptively filtering out non-matching lines.
    
    @param n_lines: Lines of the file to walk through. Default is -1 for all.
    @param verbose: Whether to print feedback. If n_lines is -1, then the
        progress bar shows a '*' for every 100,000 lines read. Otherwise,
        the progress bar shows a '=' for every 5% of lines read.
    @param func: Lambda function for matching lines. Default is to match all.
    @param args: Arguments to the lambda function.
    @return: List of JSON objects.
    """
    data = []
    n_unprocessable = 0
    if verbose:
        print("Now loading", path)
        print("[", end='')
    with open(path, "rb") as f:
        # https://stackoverflow.com/a/26128151
        for i, line in enumerate(f):
            if i == n_lines:
                break
            byte_to_str = line.decode('utf8')
            item = json.loads(byte_to_str)
            try:
                if func(item, args):
                    data.append(item)
            except:
                n_unprocessable += 1

            if verbose:
                if n_lines == -1:
                    if i % 100000 == 0:
                        print("*", end='')
                else:
                    m = max(n_lines // 20, 1)  # to prevent mod by 0
                    if i % m == 0:
                        print("=", end='')
    if verbose:
        print(f"] Loaded {len(data)}/{i} entries ({n_unprocessable} unprocessable)")
    return data

"""
Variety of matching functions.

@param item: The JSON object to match against.
@param args: Varies.
@return: Whether there was a match.

Examples with load_matches:
load_matches(PATH_BUSINESS, func=fn_eq, args=("state", "CA"))
load_matches(PATH_BUSINESS, func=fn_has, args=("name", "fish"))
load_matches(PATH_BUSINESS, func=fn_distance, args=(COORD_PHILADELPHIA, 2))
    # in which COORD_PHILADELPHIA = (39.9526, -75.1652)
load_matches(PATH_REVIEW, func=fn_gt, args=("date", "2018-10"))
load_matches(PATH_REVIEW, func=fn_lt, args=("date", "2005-12"))
"""

def fn_distance(item, args):
    center, radius = args
    point = (item["latitude"], item["longitude"])
    distance = coord_distance(center, point)
    return distance < radius

def fn_eq(item, args):
    field, target = args
    return item[field] == target

def fn_lt(item, args):
    field, target = args
    return item[field] < target

def fn_gt(item, args):
    field, target = args
    return item[field] > target

def fn_substring(item, args):
    field, substring = args
    return substring.lower() in item[field].lower()

def fn_in(item, args):
    field, collection = args
    return item[field] in collection

def fn_none(item, args):
    return False

"""
More advanced matching functions, allowing for multiple conditions.

Example:
load_matches(PATH_BUSINESS,
             verbose=True,
             func=fn_all,
             args=[(fn_gt, "stars", 3.9),
                   (fn_eq, "is_open", 1),
                   (fn_gt, "review_count", 1000)])
"""

def fn_any(item, args):
    for fn, *arg in args:
        if fn(item, arg):
            return True
    return False

def fn_all(item, args):
    for fn, *arg in args:
        if not fn(item, arg):
            return False
    return True

"""
Other helper functions.
"""

def coord_distance(coord_a, coord_b):
    """
    Calculates the distance between two points using the haversine formula.

    @param: Tuple of longitude, latitude as floats.
    @return: Distance, in miles.
    """
    lat_a, lon_a = np.deg2rad(coord_a)
    lat_b, lon_b = np.deg2rad(coord_b)
    d_lon = lon_b - lon_a
    d_lat = lat_b - lat_a
    a = np.sin(d_lat / 2)**2 + np.cos(lat_a)*np.cos(lat_b)*np.sin(d_lon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 3956  # miles
    return c * r
