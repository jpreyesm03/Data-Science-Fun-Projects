import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Step 1: Load your CSV file
df = pd.read_csv(r"C:\Users\jprey\OneDrive\Escritorio\JP\KUL\5th Semester (Polimi)\MIT IDSS\Practice Projects\Top 5 Leagues\top_5_leagues_25_countries_cumulative.csv")

# Step 2: Reshape your data from wide to long format
# This will make it easier to handle seasons and their values
df_long = df.melt(id_vars='Countries', var_name='Season', value_name='Value')

# Step 3: Create an empty dataframe to hold cumulative values per country
df_cumulative = df.copy()

# Initialize the cumulative columns to zero (except for "Countries")
for col in df_cumulative.columns[1:]:
    df_cumulative[col] = 0

# Step 4: Prepare the figure and axis
fig, ax = plt.subplots()

# Set up your histogram
def update_hist(season_idx):
    ax.clear()  # Clear previous histogram

    # Accumulate values up to the current season
    season_columns = df.columns[1:season_idx+2]  # From first to current season
    df_cumulative['Cumulative Value'] = df[season_columns].sum(axis=1)  # Summing across the seasons
    
    # Plot the histogram
    ax.hist(df_cumulative['Cumulative Value'], bins=10, color='green', alpha=0.7)  # Adjust bins as needed
    ax.set_title(f'Accumulated Histogram for seasons up to {df.columns[season_idx+1]}')
    ax.set_xlabel('Accumulated Values')
    ax.set_ylabel('Frequency')

# Step 5: Create an animation function
def animate(i):
    update_hist(i)

# Step 6: Define number of frames (equal to the number of seasons)
num_frames = len(df.columns) - 1  # Exclude "Countries" column

# Step 7: Create the animation
ani = FuncAnimation(fig, animate, frames=num_frames, interval=1000)

# Step 8: Save or display the animation
ani.save('histogram_accumulated.gif', writer='imagemagick')  # Save as GIF
# Or use plt.show() to just display it
plt.show()

