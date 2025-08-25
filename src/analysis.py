# src/analysis.py
import pandas as pd
import numpy as np

def find_max(df, cols, name):
    df_filtered = df[cols].copy()
    df_filtered['max'] = df_filtered.max(axis=1)
    df_filtered['name'] = name
    df_filtered['Seq'] = df['Seq']
    return df_filtered

def get_con_non_con_values(df_1, conserved_A, conserved_B, non_conserved_A, non_conserved_B):
    A_con = find_max(df_1, conserved_A, 'Conserved_Chain_A')
    A_non_con = find_max(df_1, non_conserved_A, 'non_Conserved_Chain_A')
    B_con = find_max(df_1, conserved_B, 'Conserved_Chain_B')
    B_non_con = find_max(df_1, non_conserved_B, 'non_Conserved_Chain_B')
    return A_con, A_non_con, B_con, B_non_con

def find_dci_max_diff(df_1, con_non_con_frames):
    A_con, A_non_con, B_con, B_non_con = con_non_con_frames
    A_con_diff = pd.DataFrame({
        'Seq': df_1['Seq'],
        'DCI_diff': A_con['max'].values - A_non_con['max'].values,
        'Condition': df_1['Condition'] + '_Chain_A',
    })

    B_con_diff = pd.DataFrame({
        'Seq': df_1['Seq'],
        'DCI_diff': B_con['max'].values - B_non_con['max'].values,
        'Condition': df_1['Condition'] + '_Chain_B',
    })
    return A_con_diff, B_con_diff

def normalize_dci(WT_dataframe, MUT_dataframe):
    #get diagonal elements
    WT_diagonal = np.diag(WT_dataframe.values)
    MUT_diagonal = np.diag(MUT_dataframe.values)
    print(WT_diagonal)
    #get average of diagonal elements
    WT_ave = np.average(WT_diagonal)
    MUT_ave = np.average(MUT_diagonal)
    #get coefficient
    normalize_coeff = WT_ave/MUT_ave
    #normalize MUT dataframe
    float_cols = MUT_dataframe.select_dtypes(include='float').columns
    MUT_dataframe.loc[:, float_cols] *= normalize_coeff
    #create subtraction dataframe
    subtracted_dataframe = MUT_dataframe.copy()
    subtracted_dataframe.loc[:, float_cols] = MUT_dataframe.loc[:, float_cols] - WT_dataframe.loc[:, float_cols]

    return MUT_dataframe, subtracted_dataframe

def get_chains(dataframe, score):
    dfi_array = dataframe[score]
    mid = int(len(dfi_array) / 2)

    chain_A = dfi_array[0:mid].reset_index(drop=True)
    chain_B = dfi_array[mid:].reset_index(drop=True)

    if len(chain_A) != (len(chain_B)):
        print('WARNING: uneven dataframe length, is your protein a heterodimer?')

    ResI = dataframe.index[0:mid]

    chain_data = {'chain_A' : chain_A, 'chain_B': chain_B}
    df = pd.DataFrame(chain_data)
    
    df.index = ResI
    df['Condition'] = dataframe['Condition'].iloc[0:mid]

    df['difference'] = df['chain_A'] - df['chain_B']

    return df
