import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random as random

def ez_diffusion_model_v2(accuracy, rt_mean, rt_variance, scaling_param=0.1):
    """
    Calculate the drift rate (v) and boundary separation (a) for the EZ-diffusion model.

    Parameters:
    - accuracy: Probability of correct responses (P_c).
    - rt_mean: Mean reaction time for correct responses.
    - rt_variance: Variance of reaction times for correct responses.
    - scaling_param: Scaling parameter (s), default is 0.1.

    Returns:
    - drift_rate (v)
    - boundary_separation (a)
    - non_decision_time (Ter)
    """
    
    if accuracy <= 0 or accuracy >= 1:
        raise ValueError("Accuracy must be between 0 and 1 (exclusive).")
    if rt_variance <= 0:
        raise ValueError("RT variance must be positive.")

    logit_pc = np.log(accuracy / (1 - accuracy))

    # Drift rate (v)
    drift_rate = (
        np.sign(accuracy - 0.5)
        * scaling_param
        * np.sqrt(
            (logit_pc * (accuracy**2 * logit_pc - accuracy * logit_pc + accuracy - 0.5)) / rt_variance
        )
    )

    # Boundary separation (a)
    boundary_separation = (scaling_param**2 * logit_pc) / drift_rate

    # Non-decision time (Ter)
    non_decision_time = rt_mean - (boundary_separation / (2 * drift_rate))

    return drift_rate, boundary_separation, non_decision_time


def wagen_ez_diffusion(mean_rt, rt_variance, accuracy):
    s = 0.1  # Standard deviation of drift rate

    if accuracy >= 1.0:
        accuracy = 0.999
    elif accuracy <= 0.0:
        accuracy = 0.001

    L = np.log(accuracy / (1 - accuracy))
    x = ((L * (L * accuracy * (1 - accuracy) - rt_variance * s**2))**0.5) / (rt_variance * s**2)
    drift_rate = x * s
    boundary_separation = L / drift_rate
    non_decision_time = mean_rt - (boundary_separation / (2 * drift_rate))
    return drift_rate, boundary_separation, non_decision_time

def plot_RT(data):
    plt.plot(data["TN"], data["Reaction Time"])
    plt.title("Variation of Reaction Time vs Trial Number")
    plt.xlabel("Trial No.")
    plt.ylabel("Reaction Time (s)")
    plt.show()

data = pd.read_csv("posnerData_S1.txt", sep="\t")
print(data.head())
print(data.shape)
print(data.info())
print(data.describe())
print(data["Correct"].unique())

# plot_RT(data)
# Filter correct responses
correct_cue_data = data[data['Correct'] == 'T']

# Summarize statistics for valid and invalid cues
summary = correct_cue_data.groupby('Valid').agg(
    mean_rt=('Reaction Time', 'mean'),
    rt_variance=('Reaction Time', 'var'),
    accuracy=('Correct', 'count')  # Proportion correct needs all trials
).reset_index()

print(type(summary))
print(summary.head())

total_trials = data.groupby('Valid')['TN'].count().reset_index() #.rename(columns={'TN': 'total_trials'})
summary = summary.merge(total_trials, on='Valid')
summary['accuracy'] = summary['accuracy'] / summary['TN']

# Apply EZ-diffusion model for each condition
# for _, row in summary.iterrows():
#     v, a, Ter = wagen_ez_diffusion(row['mean_rt'], row['rt_variance'], row['accuracy'])
#     print(f"Condition: {'Valid' if row['Valid'] == 'T' else 'Invalid'}")
#     print(f"  Drift Rate (v): {v:.4f}")
#     print(f"  Boundary Separation (a): {a:.4f}")
#     print(f"  Non-Decision Time (Ter): {Ter:.4f} seconds\n")

# Apply EZ-diffusion model for each condition using ez_diffusion_model_v2
for _, row in summary.iterrows():
    v, a, Ter = ez_diffusion_model_v2(row['accuracy'], row['mean_rt'], row['rt_variance'])  # Updated function call
    print(f"Condition: {'Valid' if row['Valid'] == 'T' else 'Invalid'}")
    print(f"  Drift Rate (v): {v:.4f}")
    print(f"  Boundary Separation (a): {a:.4f}")
    print(f"  Non-Decision Time (Ter): {Ter:.4f} seconds\n")