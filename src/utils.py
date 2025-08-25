import re
import pandas as pd

def swap_prefix(col):
    if col.startswith('A'):
        return 'C' + col[1:]
    elif col.startswith('C'):
        return 'A' + col[1:]
    return col

def increment_column(col, shift):
    match = re.match(r"([A-Z])(\d+)(_mean)", col)
    if match:
        letter, num, suffix = match.groups()
        new_num = int(num) + shift
        return f"{letter}{new_num}{suffix}"
    return col


def concat_dfs(*dfs, axis=0, ignore_index=True):
    return pd.concat(dfs, axis=axis, ignore_index=ignore_index)