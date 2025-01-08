import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Data from the images
data_chinese = pd.DataFrame({
    "<time>": [0.12, 0.24, 0.21, 0.24, 0.28, 0.16, 0.18, 0.23],
    "<place>": [0.43, 0.15, 0.27, 0.24, 0.29, 0.18, 0.17, 0.24],
    "<manner>": [0.39, 0.54, 0.44, 0.39, 0.3, 0.45, 0.5, 0.37],
    "<cause>": [0.01, 0.01, 0.01, 0.02, 0.02, 0.03, 0.0, 0.01],
    "<effect>": [0.03, 0.02, 0.03, 0.05, 0.03, 0.11, 0.09, 0.03],
    "<condition>": [0.01, 0.01, 0.01, 0.0, 0.03, 0.01, 0.01, 0.05],
    "<purpose>": [0.01, 0.01, 0.02, 0.03, 0.03, 0.05, 0.0, 0.01],
    "<concession>": [0.01, 0.02, 0.02, 0.03, 0.03, 0.01, 0.01, 0.06]
}, index=["<time>", "<place>", "<manner>", "<cause>", "<effect>", "<condition>", "<purpose>", "<concession>"])

data_english = pd.DataFrame({
    "<time>": [0.09, 0.28, 0.15, 0.19, 0.24, 0.06, 0.26, 0.13],
    "<place>": [0.26, 0.12, 0.22, 0.17, 0.15, 0.14, 0.15, 0.18],
    "<manner>": [0.1, 0.11, 0.05, 0.13, 0.08, 0.12, 0.09, 0.09],
    "<cause>": [0.13, 0.1, 0.05, 0.02, 0.15, 0.05, 0.0, 0.04],
    "<effect>": [0.17, 0.17, 0.18, 0.28, 0.15, 0.33, 0.15, 0.23],
    "<condition>": [0.01, 0.02, 0.04, 0.02, 0.03, 0.03, 0.05, 0.03],
    "<purpose>": [0.16, 0.15, 0.22, 0.11, 0.09, 0.15, 0.0, 0.13],
    "<concession>": [0.07, 0.05, 0.07, 0.07, 0.1, 0.03, 0.1, 0.17]
}, index=["<time>", "<place>", "<manner>", "<cause>", "<effect>", "<condition>", "<purpose>", "<concession>"])

# Plot heatmaps
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.title("Chinese Functional Block Transition Matrix")
plt.imshow(data_chinese, cmap="YlGnBu", interpolation="nearest")
plt.colorbar()
plt.xticks(ticks=np.arange(len(data_chinese.columns)), labels=data_chinese.columns, rotation=45)
plt.yticks(ticks=np.arange(len(data_chinese.index)), labels=data_chinese.index)

plt.subplot(1, 2, 2)
plt.title("English Functional Block Transition Matrix")
plt.imshow(data_english, cmap="YlGnBu", interpolation="nearest")
plt.colorbar()
plt.xticks(ticks=np.arange(len(data_english.columns)), labels=data_english.columns, rotation=45)
plt.yticks(ticks=np.arange(len(data_english.index)), labels=data_english.index)

plt.tight_layout()
plt.savefig("/mnt/data/functional_block_transition_matrices.png")
plt.show()