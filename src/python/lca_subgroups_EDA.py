import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

df = pd.read_csv('../../data/subgroups.csv')

class_mapping = {1: 4, 2: 3, 3: 5, 4: 6, 5: 1, 7: 2}

# Replace values in the 'reassigned_classes' column
df['reassigned_classes'] = df['reassigned_classes'].replace(class_mapping)

os.makedirs("../../res/_lca_eda", exist_ok=True)
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Box plot for SOFA score
sns.boxplot(data=df, x='reassigned_classes', y='sofa', ax=axes[0], palette="Set2")
axes[0].set_title("SOFA Score by Subgroup")
axes[0].set_xlabel("Subgroup")
axes[0].set_ylabel("SOFA Score")

# Box plot for OASIS score
sns.boxplot(data=df, x='reassigned_classes', y='oasis', ax=axes[1], palette="Set3")
axes[1].set_title("OASIS Score by Subgroup")
axes[1].set_xlabel("Subgroup")
axes[1].set_ylabel("OASIS Score")

plt.savefig(f"../../res/_lca_eda/sofa_and_oasis.png")
plt.close()


# Calculate percent prevalence for each class
class_counts = df.groupby('reassigned_classes').agg(
    sepsis_percent=('sepsis', lambda x: (x.sum() / len(x)) * 100),
    organ_failure_percent=('organ_failure', lambda x: (x.sum() / len(x)) * 100)
).reset_index()

# Calculate percent mortality for sepsis-positive and organ-failure-positive cases
mortality_counts = df[df['hospital_expire_flag'] == 1].groupby('reassigned_classes').agg(
    sepsis_mortality_percent=('sepsis', lambda x: (x.sum() / len(df[df['sepsis'] == 1])) * 100),
    organ_failure_mortality_percent=('organ_failure', lambda x: (x.sum() / len(df[df['organ_failure'] == 1])) * 100)
).reset_index()

# --- Plot 1: Percent Prevalence ---
# Melt the prevalence DataFrame
prevalence_melted = class_counts.melt(
    id_vars='reassigned_classes',
    value_vars=['sepsis_percent', 'organ_failure_percent'],
    var_name='condition',
    value_name='prevalence'
)


# Create the prevalence bar plot
plt.figure(figsize=(10, 6))
sns.barplot(
    x='reassigned_classes',
    y='prevalence',
    hue='condition',
    data=prevalence_melted,
    palette="Set2"
)

# Customize the plot
plt.title("Percent Prevalence of Sepsis and Organ Failure by Subgroup")
plt.xlabel("Reassigned Class")
plt.ylabel("Percent Prevalence (%)")
plt.legend(title="Condition", loc="upper right")
plt.tight_layout()

plt.savefig(f"../../res/_lca_eda/sepsis_organfailure_prevalance.png")
plt.close()


# --- Plot 2: Percent Mortality ---
# Melt the mortality DataFrame
mortality_melted = mortality_counts.melt(
    id_vars='reassigned_classes',
    value_vars=['sepsis_mortality_percent', 'organ_failure_mortality_percent'],
    var_name='condition',
    value_name='mortality_percent'
)

# Create the mortality bar plot
plt.figure(figsize=(10, 6))
sns.barplot(
    x='reassigned_classes',
    y='mortality_percent',
    hue='condition',
    data=mortality_melted,
    palette="coolwarm"
)

# Customize the plot
plt.title("Percent Mortality for Sepsis-Positive and Organ-Failure-Positive Cases")
plt.xlabel("Reassigned Class")
plt.ylabel("Percent Mortality (%)")
plt.legend(title="Condition", loc="upper right")
plt.tight_layout()

plt.savefig(f"../../res/_lca_eda/sepsis_organfailure_mortality.png")
plt.close()

new_com = df.columns[21:-2]

subgroup_comorbidity_counts2 = df.groupby('reassigned_classes')[new_com].sum()


# Calculate the global maximum value across all subgroups
global_max = subgroup_comorbidity_counts2.max().max()

# Iterate through each subgroup
for subgroup, counts in subgroup_comorbidity_counts2.iterrows():
    labels = counts.index  # Preserve the original order
    values = counts.values

    # Normalize values using the global maximum
    values_normalized = values / global_max  # Scale the values to [0, 1]

    # Define angles for the bars (evenly spaced)
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)

    # Wrap the values and angles for circular plotting
    values_normalized = np.append(values_normalized, values_normalized[0])  # Closing the loop
    angles = np.append(angles, angles[0])  # Closing the loop

    # Define the top 5 comorbidities for labeling
    top_5_indices = np.argsort(values[:-1])[-5:]  # Indices of the top 5 (before normalization)
    top_5_labels = [labels[i] for i in top_5_indices]

    # Plot settings
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"projection": "polar"})
    sns.set(style="whitegrid")

    # Plot all bars with normalized values
    bars = ax.bar(
        angles[:-1], values_normalized[:-1], width=0.4, align="center",
        color=sns.color_palette("Set2", len(labels)),
        edgecolor="black", alpha=0.8
    )

    # Add labels for top 5
    for angle, value, label in zip(angles[:-1], values_normalized[:-1], labels):
        if label in top_5_labels:
            # Dynamic offset based on the normalized value to avoid overlap
            y_offset = 0.05  # Adjust the offset slightly to prevent overlap with the bar
            ax.text(
                angle, value + y_offset, label,
                horizontalalignment="center", verticalalignment="center",
                fontsize=10, rotation=0  # Keep labels horizontal
            )

    # Style adjustments
    ax.set_xticks([])  # Remove angular ticks
    ax.set_yticks([])  # Remove radial ticks
    ax.spines['polar'].set_visible(False)  # Hide border circle
    ax.set_ylim(0, 1)  # Set y-axis (radial axis) limit from 0 to 1
    ax.set_title(f"Subgroup {subgroup}", va="bottom", fontsize=14)

    # Show plot
    plt.tight_layout()
    plt.savefig(f"../../res/_lca_eda/subgroup_{subgroup}_comorbidities.png")
    plt.close()


# Sort groups by reassigned_classes
sorted_groups = sorted(df['reassigned_classes'].unique())  # Ensure classes are sorted from 1 to 6
grouped_data = [df[df['reassigned_classes'] == group]['age_years'].dropna() for group in sorted_groups]

# Create a single plot
plt.figure(figsize=(10, 6))
plt.boxplot(grouped_data, vert=True, patch_artist=True, 
            boxprops=dict(facecolor='skyblue', color='black'), 
            medianprops=dict(color='red'))

# Add titles and labels
plt.title('Age Distribution Across Groups (Ordered 1 to 6)')
plt.xlabel('Group')
plt.ylabel('Age (years)')
plt.xticks(ticks=range(1, len(sorted_groups) + 1), labels=sorted_groups, rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show plot
plt.tight_layout()
plt.savefig(f"../../res/_lca_eda/subgroup_age_distribution.png")






