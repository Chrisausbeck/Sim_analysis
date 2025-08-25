# src/formatting.py
import pandas as pd
from src.utils import concat_dfs

def df_format(df, residue, my_format):
    if my_format:
        residue_A = f"A{residue}_mean"
        residue_B = f"C{residue}_mean"
    else:
        residue_A = f"A{residue}"
        residue_B = f"C{residue}"

    df_filtered_A = df[['Seq']].copy()
    df_filtered_A['Condition'] = df['Condition'] + '_Chain_A'
    df_filtered_A['DCI'] = df[residue_A]

    df_filtered_B = df[['Seq']].copy()
    df_filtered_B['Condition'] = df['Condition'] + '_Chain_B'
    df_filtered_B['DCI'] = df[residue_B]

    return concat_dfs(df_filtered_A, df_filtered_B)

def save_to_csv(df, my_format, residue, title, output_dir):
    if my_format:
        residue_A = f"A{residue}_mean"
        residue_B = f"C{residue}_mean"
    else:
        residue_A = f"A{residue}"
        residue_B = f"C{residue}"

    result_df = df[['Seq']].copy()
    result_df['Chain A'] = df[residue_A]
    result_df['Chain B'] = df[residue_B]

    result_df.to_csv(output_dir + title, index=False)
    print(f"Data saved to: {output_dir + title}")