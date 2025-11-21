# src/load.py
import pandas as pd
from src.utils import increment_columns_or_index, swap_prefix
import itertools as iter
import numpy as np

def format(df, format_type):
    if format_type:
        df = df.drop(df.filter(regex='_sem$').columns, axis=1)
    return df

def shift_dci_values(df, start):
    df.columns = [increment_columns_or_index(col, start - 1) for col in df.columns]
    df.index = [increment_columns_or_index(row, start - 1) for row in df.index]
    return df

def swap_chains(df):
    chain_length = len(df) // 2
    chain_A = df.iloc[:chain_length].copy()
    chain_B = df.iloc[chain_length:].copy()
    df = pd.concat([chain_B, chain_A], ignore_index=True)
    df.columns = [swap_prefix(col) for col in df.columns]
    return df

def load_and_prepare(file_path, condition, swap, start, myformat, delimiter = ',', index_col = 0, create_resI=False, shift_dci=False):
    df = pd.read_csv(file_path, delimiter=delimiter, index_col = index_col)

    if myformat:
        df = df.drop(df.filter(regex='_sem$').columns, axis=1)
        #if shift != 0:
        #    df.columns = [increment_column(col, shift) for col in df.columns]

    if 'ResI' in df.columns:
        print('checking if correct starting alignment based on start value in .yaml confid')
        if df['ResI'].iloc[0] == start:
            print('correct starting alignment')
        else:
            print('incorrect starting alignment, fixing using inputted start value in .yaml config')
            shift = start - df['ResI'].iloc[0]
            df['ResI'] = df['ResI'] + shift
        df.set_index('ResI', inplace=True)
    
    #setting ResI as the index
    if create_resI == True:
        print('create ResI set to true, creating ResI values using dataframe length and start value in .yaml config')
        resI = np.arange(start, int(len(df) / 2) + start)
        resI = np.concatenate([resI, resI])
        print(len(resI) == len(df))
        df['ResI'] = resI
        df.set_index('ResI', inplace=True)
    
    if shift_dci == True:
        print('shifting DCI values by start value to account for missing residues in structure')
        df = shift_dci_values(df, start)

    if swap:
        df = swap_chains(df)

    df['Condition'] = condition
    print(df.head())
    return df

def align_dfs(*dfs):
    import functools as func
    common_residues = func.reduce(
        lambda acc, df: acc & set(df['ResI']),
        dfs[1:],
        set(dfs[0]['ResI'])
    )
    return [df[df['ResI'].isin(common_residues)].copy() for df in dfs]