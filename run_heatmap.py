import os
import yaml
import numpy as np
from src.load_data import load_and_prepare
from src.analysis import normalize_dci
from src.plotting import heatmap

# YAML Parameters
with open("configs/EGFR_non_average_dci.yaml", 'r') as f:
    config = yaml.safe_load(f)

#separate out YAML file
datasets = config['datasets']
cfg_all = config['all']
heatmap_dir = cfg_all['heatmap_dir']
os.makedirs(heatmap_dir, exist_ok=True)
titles = cfg_all['all_title']

WT_data = datasets['WT']
#Load and prepare WT dataframe for subtraction
df_WT = load_and_prepare(**WT_data['data_to_load'])

# Loop through each dataset in the config
for label, dataset_args in datasets.items():
    print(f"Processing dataset: {label}")
    data_to_load = dataset_args['data_to_load']
    output = dataset_args['output']

    os.makedirs(output, exist_ok=True)

    # Load and prepare data
    df = load_and_prepare(**data_to_load)

    # Run analysis (modify this as needed)
    normalized_df, subtracted_df = normalize_dci(df_WT, df)



    # Plot raw data heatmap and save it in respective mutation folder and heatmap folder
    heatmap(df, 0, 3.0, dataset_args['output'], heatmap_dir, dataset_args['title'] + ' Heatmap', 'plasma')
    # Plot analysed data heatmap and save it in respective mutation folder and heatmap folder
    heatmap(normalized_df, 0, 3.0, dataset_args['output'], heatmap_dir, dataset_args['title'] + ' Normalized Heatmap', 'plasma')
    # Plot subtracted data heatmap and save it in respective mutation folder and heatmap folder
    heatmap(subtracted_df, -1.5, 1.5, dataset_args['output'], heatmap_dir, dataset_args['title'] + ' Subtracted Heatmap', 'coolwarm')