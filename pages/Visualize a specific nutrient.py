# Re-importing necessary libraries and reloading the dataset due to environment reset
import pandas as pd
import matplotlib.pyplot as plt

# Load the uploaded cleaned food data
cleaned_file_path = 'data/cleaned_food_data.csv'
food_data = pd.read_csv(cleaned_file_path)

# Variables available for visualization
variables = [
    'energy_kcal', 'protein', 'total_fat', 'dietary_fiber',
    'carbohydrate', 'iron_(fe)', 'calcium_(ca)', 'zinc_(zn)',
    'magnesium_(mg)', 'phosphorus_(p)', 'potassium_(k)', 'sodium_(na)'
]

# Function to visualize nutrient distribution based on selected variable
def visualize_distribution(data, variable):
    plt.figure(figsize=(10, 6))
    data.groupby('food_group')[variable].mean().sort_values().plot(
        kind='bar',
        title=f'Average {variable.replace("_", " ").capitalize()} by Food Group'
    )
    plt.ylabel(f'Average {variable.replace("_", " ").capitalize()}')
    plt.xlabel('Food Group')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Example: Visualize distribution for 'energy_kcal' and 'protein'
visualize_distribution(food_data, 'energy_kcal')
visualize_distribution(food_data, 'protein')
