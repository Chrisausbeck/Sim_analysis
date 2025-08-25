# src/plotting.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

from src.utils import concat_dfs

def plot_chains(chain_dataframe, color):
    sns.lineplot(data=chain_dataframe, x=chain_dataframe.index, y='chain_A',
                 label = chain_dataframe['Condition'].iloc[0], color = color, linestyle='-', linewidth=0.8,
                 errorbar=None)
    sns.lineplot(data=chain_dataframe, x=chain_dataframe.index, y='chain_B',
                 label = chain_dataframe['Condition'].iloc[0], color = color, linestyle='--', linewidth=0.8,
                 errorbar=None)
    
def plot_chain_difference(chain_dataframe, score, color):
    sns.lineplot(data=chain_dataframe, x=chain_dataframe.index, y=score,
                 label = chain_dataframe['Condition'].iloc[0], color = color, linestyle='-', linewidth=0.8,
                 errorbar=None)
    
def plot_density(dataframe, score, color, bound):
    if bound:
        sns.kdeplot(dataframe[score], label=dataframe['Condition'].iloc[0], color=color, linewidth=2)
    else:
        sns.kdeplot(dataframe[score], label=dataframe['Condition'].iloc[0], color=color, linestyle='--', linewidth=2)

def plot_max(combined_max, chain_bool, title, output_dir):
    plt.figure(figsize=(10, 5))
    if chain_bool:
        plot_chains(combined_max)
    else:
        sns.lineplot(data=combined_max, x='Seq', y='max', errorbar=None, hue='name', linestyle='-', linewidth=0.8)
    plt.title(title)
    plt.xlabel("Residue Index")
    plt.ylabel("DCI")
    plt.ylim(0, 8)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, title + ".png"), dpi=300)
    plt.close()

def plot_max_diff(max_frames, title, output_dir):
    max_A, max_B = max_frames
    combined_max = pd.concat([max_A, max_B])
    sns.lineplot(data=combined_max, x='Seq', y='DCI_diff', errorbar=None, hue='Condition', linestyle='-', linewidth=0.8)
    plt.title(title)
    plt.xlabel("Residue Index")
    plt.ylabel("DCI")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, title + ".png"), dpi=300)
    plt.close()

def plot_un_lig(df_lig1, df_lig2, df_un1, df_un2, residue, output_dir):
    df_diff1 = pd.DataFrame({
        'ResI': df_lig1['ResI'], 'Seq': df_lig1['Seq'],
        'DCI_diff': df_lig1[f'{residue}_mean'] - df_un1[f'{residue}_mean'],
        'Condition': df_lig1['Condition']
    })
    df_diff2 = pd.DataFrame({
        'ResI': df_lig2['ResI'], 'Seq': df_lig2['Seq'],
        'DCI_diff': df_lig2[f'{residue}_mean'] - df_un2[f'{residue}_mean'],
        'Condition': df_lig2['Condition']
    })
    df_plot = pd.concat([df_diff1, df_diff2], ignore_index=True)
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df_plot, x='Seq', y='DCI_diff', hue='Condition', marker='.')
    plt.title(f"DCI Difference {residue} (Ligbound - Unbound)")
    plt.xlabel("Residue Index")
    plt.ylabel("DCI difference")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{residue}__Diff_DCI_lig_un.png"))
    plt.close()

def heatmap(dataframe, min_value, max_value, output_dir, heatmap_dir, title, cmap):
    df = dataframe.drop('Condition', axis=1)
    sns.heatmap(df, vmin=min_value, vmax=max_value, cmap=cmap)
    plt.title(title)
    plt.savefig(os.path.join(output_dir, title), dpi=300)
    plt.savefig(os.path.join(heatmap_dir, title), dpi=300)
    plt.close()

def plot_residue(dataframe, residue, color):
    sns.lineplot(data=dataframe, x=dataframe.index, y=dataframe['A' + str(residue)], label = dataframe['Condition'].iloc[2], color=color, linestyle='-', linewidth=0.5)
    sns.lineplot(data=dataframe, x=dataframe.index, y=dataframe['B' + str(residue)], label = dataframe['Condition'].iloc[2], color=color, linestyle='--', linewidth=0.5)
    plt.xticks(dataframe.index[::100], fontsize=10, rotation=45)
    plt.ylabel('DCI')

def plot_any(dataframe, x_value, y_value, label=None, color='#1f77b4'):
    sns.lineplot(data=dataframe, x=dataframe[x_value], y=dataframe[y_value], label=label, color=color)