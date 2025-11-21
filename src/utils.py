import re
import pandas as pd

def swap_prefix(col):
    if col.startswith('A'):
        return 'C' + col[1:]
    elif col.startswith('C'):
        return 'A' + col[1:]
    return col

def increment_columns_or_index(col, start):
    match = re.match(r"([A-Z])(\d+)", col)
    if match:
        letter, num = match.groups()
        new_num = int(num) + start
        return f"{letter}{new_num}"
    return col


def concat_dfs(*dfs, axis=0, ignore_index=True):
    return pd.concat(dfs, axis=axis, ignore_index=ignore_index)