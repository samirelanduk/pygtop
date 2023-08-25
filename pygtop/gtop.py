"""Functions for interacting with the Guide to PHARMACOLOGY web services."""

import json
import requests

ROOT_URL = "https://www.guidetopharmacology.org/services/"

def get_json_from_gtop(query, attempts=5):
    """Issues a query to the GtoP web services, and returns the resulting JSON.

    If it does not get a valid response, it will try again, and if it still
    doesn't get JSON back, it will return None.

    :param str query: The query to append to the base URL.
    :param int attempts: The number of attempts to make before giving up \
    (default is 5).
    :return: JSON object or None"""

    if not isinstance(attempts, int):
        raise TypeError(
         "attempts must be an integer greater than zero, not %s", str(attempts)
        )
    if attempts < 1:
        raise ValueError(
         "attempts must be an integer greater than zero, not %s", str(attempts)
        )

    try_count = 0
    while try_count < attempts:
        response = requests.get("%s%s" % (ROOT_URL, query))
        try:
            if response.status_code == 200 and len(response.text) > 1:
                return json.loads(response.text)
            else:
                raise ValueError
        except ValueError:
            try_count += 1
    return None
