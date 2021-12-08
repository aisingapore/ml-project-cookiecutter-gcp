# Add your metric update functions here.
# Parameters should only have `value` and `old_value`.
# Return value should only be either int or float.

from typing import Union

number = Union[int, float]

def model_latency_seconds(value: number, old_value: number = 0) -> number:
    # Overwrite old value
    return value

def model_accuracy_rate(value: number, old_value: number = 0) -> number:
    # Overwrite old value
    return value

