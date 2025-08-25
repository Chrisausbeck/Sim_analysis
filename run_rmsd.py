import os
import yaml
import numpy as np
import matplotlib.pyplot as plt
from src.load_data import load_and_prepare
from src.plotting import plot_any

# YAML Parameters
with open("configs/EGFR_rmsd.yaml", 'r') as f:
    config = yaml.safe_load(f)

#set datasets to YAML file
datasets = config['datasets']
cfg_all = config['all']
all_output = cfg_all['all_output']
all_title = cfg_all['all_title']
os.makedirs(all_output, exist_ok=True)


# --- Initialize plot for "all" overlay
plt.figure(figsize=(10, 6))

# Store for difference plot as well
plt_diff = plt.figure(figsize=(10, 6))



# Loop through each dataset in the config and plot individually
for label, dataset_args in datasets.items():
    print(f"Processing dataset: {label}")

    data_to_load = dataset_args['data_to_load']
    output = dataset_args['output']
    title = dataset_args['title']
    color = dataset_args['color']
    score_x = dataset_args['score_x']
    score_y = dataset_args['score_y']

    # Create output directory if needed
    os.makedirs(output, exist_ok=True)

    # Load and prepare data
    df = load_and_prepare(**data_to_load)
    df = df.reset_index()

    # Run analysis (modify this as needed)

    #plot chain A and B on same plot
    plt.figure(figsize=(10, 6))
    plot_any(df, score_x, score_y, df['Condition'].iloc[2], color)
    plt.title(title)
    plt.ylabel('RMSD')
    plt.xlabel('Frame')
    plt.savefig(os.path.join(output, title), dpi=300)
    plt.close()

    # 2. Add to combined "all datasets" plot
    plt.figure(1)
    plot_any(df, score_x, score_y, df['Condition'].iloc[2], color)

# --- Save the combined plots
plt.figure(1)
plt.title(all_title)
plt.ylabel('RMSD')
plt.xlabel('Frame')
plt.savefig(os.path.join(all_output, all_title), dpi=300)
plt.close()