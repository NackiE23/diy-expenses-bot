import re
from typing import Tuple, Any


def input_validation(input_string: str):
    pattern = re.compile(r'^(\d+(\.\d+)?)\s*(?:-d (.*?))?\s*(?:-dt (.*?))?$')
    match = pattern.match(input_string)

    if match:
        sum_value = match.group(1)
        description = match.group(3)  # Group 3 corresponds to the -d description
        datetime_value = match.group(4)  # Group 4 corresponds to the -dt datetime

        return {
            'sum': float(sum_value),
            'description': description,
            'datetime': datetime_value
        }
    else:
        return None
