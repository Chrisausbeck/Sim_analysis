import os
import yaml
import numpy as np
import matplotlib.pyplot as plt
from src.load_data import load_and_prepare
from src.analysis import get_chains
from src.plotting import plot_density

# YAML Parameters
with open("configs/LACI_dfi_density.yaml", 'r') as f:
    config = yaml.safe_load(f)

#set datasets to YAML file
datasets = config['datasets']
cfg_all = config['all']
all_output = cfg_all['all_output']
all_title = cfg_all['all_title']
os.makedirs(all_output, exist_ok=True)

density_dir = cfg_all['density_dir']
os.makedirs(density_dir, exist_ok=True)

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
    score = dataset_args['score']
    bound = dataset_args['bound']

    # Create output directory if needed
    os.makedirs(output, exist_ok=True)

    # Load and prepare data
    df = load_and_prepare(**data_to_load)

    # Run analysis (modify this as needed)
    chain_df = get_chains(df, score)
    # Select points within the given bounds
    if bound == tuple:
        lower, upper = bound # assuming bound is a tuple (lower, upper)
        chain_df = chain_df[(chain_df['ResI'] >= lower) & (chain_df['ResI'] <= upper)]

    #plot single density protein
    plt.figure(figsize=(10, 6))
    plot_density(chain_df, 'difference', color, bound)
    # Optional: Add vertical line at 0
    plt.axvline(0, color='gray', linestyle='--', linewidth=1)

    plt.title(title + ' Density Difference')
    plt.xlabel("DFI Density", fontsize=14)
    plt.ylabel("Density", fontsize=14)
    plt.savefig(os.path.join(density_dir, title + ' Density'), dpi=300)
    plt.xlim(-0.0015,0.0015)
    plt.title(title + ' Density Difference Zoomed in')
    plt.savefig(os.path.join(density_dir, title + ' Density Zoomed'), dpi=300)
    plt.close()


    #Add to density dfi difference plot
    plt.figure(1)
    plot_density(chain_df, 'difference', color, bound)

plt.figure(1)

# Optional: Add vertical line at 0
plt.axvline(0, color='gray', linestyle='--', linewidth=1)

plt.title(all_title + ' Density Difference')
plt.xlabel("DFI Density", fontsize=14)
plt.ylabel("Density", fontsize=14)
plt.legend()
plt.savefig(os.path.join(density_dir, all_title + ' Density'), dpi=300)
plt.xlim(-0.0015,0.0015)
plt.title(all_title + ' Density Difference Zoomed')
plt.savefig(os.path.join(density_dir, all_title + ' Density Zoomed'), dpi=300)
plt.close()