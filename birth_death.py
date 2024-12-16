import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('birth_death_rates.csv')

# Display the first few rows of the dataset
print(data.head())

# Check the columns to ensure they are named correctly
print(data.columns)

# Convert the year column to datetime (if it's not already in datetime format)
data['Year'] = pd.to_datetime(data['Year'], format='%Y')

# Group by year and calculate average birth and death rates
annual_data = data.groupby(data['Year'].dt.year).mean()

# Plotting the trends as a bar chart
plt.figure(figsize=(12, 6))

# Set the bar width
bar_width = 0.35

# Set the positions of the bars on the x-axis
r1 = annual_data.index
r2 = [x + bar_width for x in r1]

# Create bars for Birth Rate and Death Rate
plt.bar(r1, annual_data['Birth Rate'], width=bar_width, label='Birth Rate', color='blue')
plt.bar(r2, annual_data['Death Rate'], width=bar_width, label='Death Rate', color='red')

# Adding titles and labels
plt.title('Birth and Death Rate Trends Over Time', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Rate per 1000 People', fontsize=14)
plt.xticks([r + bar_width / 2 for r in r1], annual_data.index, rotation=45)  # Center the x-ticks
plt.legend()
plt.grid(axis='y')

# Show the plot
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()
