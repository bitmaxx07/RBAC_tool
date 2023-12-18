"""
Could be useful for the discussion chapter
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta
import pandas as pd

data = pd.read_csv("random_items.csv")

success_A = (data['Item'] == 'A').sum()
fail_A = (data['Item'] != 'A').sum()

print("A in sample selected:", success_A, "/", success_A + fail_A)

alpha_A = 1 + success_A
beta_A = 1 + fail_A

sample_A = beta.rvs(alpha_A, beta_A, size=1000)

plt.figure(figsize=(10, 8))
plt.hist(sample_A)
plt.title('Distribution for A')
plt.xlabel('Prob of selected')
plt.ylabel('Frequency')
plt.show()

mean_prob_A = np.mean(sample_A)
sd_A = np.std(sample_A)

print("mean prob of A selected:", mean_prob_A)
print("SD:", sd_A)


def thompson(item):
    if item not in data['Item'].values:
        return f"{item} not in given file!"
    else:
        success = (data['Item'] == item).sum()
        failure = (data['Item'] != item).sum()

        alpha_item = 1 + success
        beta_item = 1 + failure

        samples = beta.rvs(alpha_item, beta_item, size=1000)

        return {
            'mean_prob': np.mean(samples),
            'SD': np.std(samples),
            'sample': samples
        }


print(thompson("B"))
