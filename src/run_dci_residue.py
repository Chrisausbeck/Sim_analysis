import os
import yaml
import numpy as np
import matplotlib.pyplot as plt
from src.load_data import load_and_prepare
from src.analysis import normalize_dci
from src.plotting import plot_residue

# YAML Parameters
with open("configs/EGFR.yaml", 'r') as f:
    config = yaml.safe_load(f)

#separate out YAML file
datasets = config['datasets']

output_dirs = config['outputs']
residues = config['residues']
residue_dir = 'output/EGFR/residue/'
titles = config['titles']
colors = config['colors']


#Load and prepare WT dataframe for subtraction
df_WT = load_and_prepare(**datasets['WT'])

# Loop through each dataset in the config
for resI in residues:
    for label, dataset_args in list(datasets.items())[:3]:
        print(f"Processing dataset: {label}")

        # Create output directory if needed
        os.makedirs(output_dirs[label], exist_ok=True)

        # Load and prepare data
        df = load_and_prepare(**dataset_args)

        # Run analysis (modify this as needed)
        normalized_df, subtracted_df = normalize_dci(df_WT, df)  # placeholder – apply analysis if needed

        plot_residue(normalized_df, resI, colors[label])

    plt.title('DCI of ' + str(resI))
    plt.legend()
    plt.savefig(os.path.join(residue_dir, str(resI)), dpi=300)
    plt.close()