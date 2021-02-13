#!/usr/bin/env python3

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_heatmap(data):
    mask = np.triu(np.ones_like(data, dtype=bool))

    heat_map = sns.heatmap(data, mask=mask, annot=True)
    heat_map.set(title='Cosine Similarity Matrix')

    heat_map.set_yticklabels(heat_map.get_ymajorticklabels(), fontsize = 6, rotation=30)
    heat_map.set_xticklabels(heat_map.get_xmajorticklabels(), fontsize = 6, rotation=30)

    plt.show()
