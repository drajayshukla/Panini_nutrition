import pandas as pd
import matplotlib.pyplot as plt
#Load the dataset
file_path = 'data/cleaned_food_data.csv'
food_data = pd.read_csv(file_path)

# Ensure correct data types for numerical columns
numerical_columns = food_data.select_dtypes(include=['float64', 'int64']).columns

# Visualizations
import matplotlib.pyplot as plt

# 1. Distribution of Energy by Food Group
plt.figure(figsize=(10, 6))
food_data.groupby('food_group')['energy_kcal'].mean().sort_values().plot(kind='bar', title='Average Energy (kcal) by Food Group')
plt.ylabel('Average Energy (kcal)')
plt.xlabel('Food Group')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 2. Nutrient Comparison Across Food Groups (Radar Chart)
from math import pi
import numpy as np

# Radar chart for the top 3 food groups
top_food_groups = food_data['food_group'].value_counts().index[:3]
group_data = food_data[food_data['food_group'].isin(top_food_groups)].groupby('food_group')[numerical_columns].mean()

# Prepare data for the radar chart
categories = numerical_columns.tolist()
num_vars = len(categories)
angles = np.linspace(0, 2 * pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # Repeat the first angle to close the chart

plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)
for group in top_food_groups:
    values = group_data.loc[group].values.flatten().tolist()
    values += values[:1]  # Repeat the first value to close the chart
    ax.plot(angles, values, label=group)
    ax.fill(angles, values, alpha=0.25)

ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)
plt.xticks(angles[:-1], categories, fontsize=10)
plt.title('Nutrient Distribution in Top Food Groups', fontsize=12)
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
plt.tight_layout()
plt.show()

# 3. Correlation Heatmap
import seaborn as sns

plt.figure(figsize=(12, 8))
correlation = food_data[numerical_columns].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap of Nutrients', fontsize=14)
plt.tight_layout()
plt.show()

# 4. Boxplot of Protein Content Across Food Groups
plt.figure(figsize=(12, 6))
sns.boxplot(data=food_data, x='food_group', y='protein')
plt.xticks(rotation=45, ha='right')
plt.title('Protein Content Distribution by Food Group')
plt.tight_layout()
plt.show()
