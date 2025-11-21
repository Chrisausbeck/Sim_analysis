import os
import yaml
import numpy as np
import matplotlib.pyplot as plt
from src.load_data import load_and_prepare
from src.plotting import plot_chains
from src.analysis import get_chains
from src.plotting import plot_chain_difference

# YAML Parameters
with open("configs/Sars_Cov_2_dfi.yaml", 'r') as f:
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
    score = dataset_args['score']

    # Create output directory if needed
    os.makedirs(output, exist_ok=True)

    # Load and prepare data
    df = load_and_prepare(**data_to_load)

    # Run analysis (modify this as needed)
    chain_df = get_chains(df, score)

    #plot chain A and B on same plot
    plt.figure(figsize=(10, 6))
    plot_chains(chain_df, color)
    plt.title(title)
    plt.ylabel('DFI')
    plt.xlabel('ResI')
    plt.savefig(os.path.join(output, title), dpi=300)
    #plt.xlim(50, 350)
    #plt.ylim(0, 0.003)
    #plt.savefig(os.path.join(output, title + ' zoomed'), dpi=300)
    plt.close()

    # 2. Add to combined "all datasets" plot
    plt.figure(1)
    plot_chains(chain_df, color)

    # 3. Add to difference plot
    plt.figure(2)
    plot_chain_difference(chain_df, 'difference', color)

# --- Save the combined plots
plt.figure(1)
plt.title(all_title)
plt.ylabel('DFI')
plt.xlabel('ResI')
plt.savefig(os.path.join(all_output, all_title), dpi=300)
#plt.xlim(50, 350)
#plt.ylim(0, 0.003)
#plt.savefig(os.path.join(all_output, all_title + ' zoomed'), dpi=300)
plt.close()

plt.figure(2)
plt.title(all_title + ' Difference')
plt.ylabel('DFI')
plt.xlabel('ResI')
plt.savefig(os.path.join(all_output, all_title + ' Difference'), dpi=300)
plt.close()