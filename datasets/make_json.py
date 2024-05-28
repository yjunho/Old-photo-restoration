# import json
# import os
# import io
# import numpy as np


# # For DIV2K, Set5, Set14, BSD100, Urban100, Manga109
# file = io.open('DIV2K.json','w',encoding='utf-8')
# samples = []

# root = './DIV2K/DIV2K_train_HR_sub'
# sample_list = sorted(os.listdir(root))
# sample = [sample_list[i][:-4] for i in range(len(sample_list))]
# sample_sub = []
# for sam in sample:
#     if not sam == ".DS_S":
#         sample_sub.append(sam)
# l = {'name': 'DIV2K', 'phase': 'train','sample': sample_sub}

# samples.append(l)

# js = json.dump(samples, file, sort_keys=True, indent=4)

import json
import os
import io

# For DIV2K, Set5, Set14, BSD100, Urban100, Manga109
file_path = 'DIV2K.json'

# Ensure the directory structure is correct and contains files
root = './DIV2K/DIV2K_train_HR_sub'
if not os.path.exists(root):
    raise FileNotFoundError(f"Root directory not found: {root}")

# Create the list of samples
samples = []
sample_list = sorted(os.listdir(root))
sample_sub = [sample[:-4] for sample in sample_list if sample.endswith('.png') and sample != ".DS_Store"]

# Check the generated sample list
if not sample_sub:
    raise ValueError("No valid samples found in the directory.")

# Create the JSON structure
l = {'name': 'DIV2K', 'phase': 'train', 'sample': sample_sub}
samples.append(l)

# Write to JSON file
with io.open(file_path, 'w', encoding='utf-8') as file:
    json.dump(samples, file, sort_keys=True, indent=4)

print(f"JSON file created at {file_path} with {len(sample_sub)} samples.")

