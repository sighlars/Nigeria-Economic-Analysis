import pandas as pd 
import matplotlib.pyplot as plt  
from scipy.stats import linregress
import seaborn as sns

# Load the dataset from a CSV file
data = pd.read_csv("nigeria_population.csv")  # Reads the CSV file into a DataFrame called `data`
# Representation: data is now a table with rows and columns like a spreadsheet.

# Filter the rows to only include GDP growth data
GDP_data = data[data["Series Name"] == "GDP growth (annual %)"]  
# Representation: GDP_data contains only the rows where "Series Name" is "GDP growth (annual %)".

# Reshape the dataset to make year columns into rows
GDP_data_long = GDP_data.melt(
    id_vars=["Country Name", "Series Name"],  # Keep these columns as is
    value_vars=[col for col in GDP_data.columns if "YR" in col],  # Select year columns (e.g., "YR1990", "YR2000")
    var_name="Year",  # New column name for years
    value_name="GDP Rate"  # New column name for GDP rates
)
# Representation: GDP_data_long is now "long" format with three main columns: "Year", "Country Name", and "GDP Rate".

# Extract numeric years (e.g., "YR1990" becomes "1990")
GDP_data_long["Year"] = GDP_data_long["Year"].str.extract(r"(\d+)").astype(int)
# Representation: "Year" column now contains plain numbers like 1990, 2000.

# Convert "GDP Rate" values to numbers and handle any invalid values
GDP_data_long["GDP Rate"] = pd.to_numeric(GDP_data_long["GDP Rate"], errors="coerce")
# Representation: Invalid values in "GDP Rate" (e.g., text or missing values) are replaced with NaN.

# Remove rows with missing values (NaN)
GDP_data_long = GDP_data_long.dropna()
# Representation: Rows where "GDP Rate" or "Year" is missing are removed.

# Create a plot of GDP rates over time
plt.figure(figsize=(10, 6))  # Set the figure size
plt.plot(GDP_data_long["Year"], GDP_data_long["GDP Rate"], label="GDP Rate", color="red")  # Line plot
plt.xlabel("Year")  # Label for x-axis
plt.ylabel("GDP Rate (%)")  # Label for y-axis
plt.title("GDP in Nigeria Over Time")  # Title of the plot
plt.grid(True, linestyle="--", alpha=0.6)  # Add gridlines to the plot
plt.legend()
plt.savefig("GDP_Rate.png", dpi=300, bbox_inches="tight")# Add a legend
plt.show()  # Display the plot

# Debugging: Print the first few rows of cleaned data
print(f'Years: {GDP_data_long["Year"].head()}, GDP Rates: {GDP_data_long["GDP Rate"].head()}')

# Check unique values in "Series Name" to ensure correct filtering
print(data["Series Name"].unique())  # Prints all unique entries in "Series Name" for verification

# Filter rows for Population data
Population_data = data[data["Series Name"] == "Population growth (annual %)"]

# Reshape the data from wide to long format
Population_data_long = Population_data.melt(
    id_vars=["Country Name", "Series Name"],
    value_vars=[col for col in Population_data.columns if "YR" in col],  # Select year columns
    var_name="Year",
    value_name="Population growth"
)

# Clean the Year column (remove "[YRYYYY]")
Population_data_long["Year"] = Population_data_long["Year"].str.extract(r"(\d+)").astype(int)

# Convert Population growth to numeric (handle non-numeric values)
Population_data_long["Population growth"] = pd.to_numeric(Population_data_long["Population growth"], errors="coerce")

# Drop rows with missing values
Population_data_long = Population_data_long.dropna()

# Merge GDP and Population data
merged_data = pd.merge(GDP_data_long, Population_data_long, on=["Country Name", "Year"])


# Plot GDP vs. Population
plt.figure(figsize=(10, 6))
plt.scatter(merged_data["Population growth"], merged_data["GDP Rate"], color="blue")
plt.xlabel("Population growth (%)")
plt.ylabel("GDP Rate (%)")
plt.title("GDP vs. Population in Nigeria")
plt.savefig("Population_against_gdp.png", dpi=300, bbox_inches="tight")
plt.show()

# Simulate the impact of population changes on GDP
# Assume a 1% increase in population growth increases GDP by 0.5%
merged_data["Simulated GDP Rate (Population +1%)"] = merged_data["GDP Rate"] + (merged_data["Population growth"] * 0.5)

# Assume a 1% decrease in population growth decreases GDP by 0.5%
merged_data["Simulated GDP Rate (Population -1%)"] = merged_data["GDP Rate"] - (merged_data["Population growth"] * 0.5)

# Plot the results
plt.figure(figsize=(10, 6))
plt.scatter(merged_data["Population growth"], merged_data["GDP Rate"], label="Current GDP Rate", color="blue")
plt.scatter(merged_data["Population growth"], merged_data["Simulated GDP Rate (Population +1%)"], label="Simulated GDP Rate (Population +1%)", color="green")
plt.scatter(merged_data["Population growth"], merged_data["Simulated GDP Rate (Population -1%)"], label="Simulated GDP Rate (Population -1%)", color="red")
plt.xlabel("Population growth (%)")
plt.ylabel("GDP Rate (%)")
plt.title("Impact of Population Changes on GDP in Nigeria")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig("Simulated_Population_Impact_on_GDP.png", dpi=300, bbox_inches="tight")
plt.show()
# Explanation: This creates a scatter plot showing the current GDP rate and the simulated GDP rates after population changes

#check spread of migration vs GDP

migration_data = data[data["Series Name"] == "Net migration"]

# Reshape the data from wide to long format
migration_data_long = migration_data.melt(
    id_vars=["Country Name", "Series Name"],
    value_vars=[col for col in migration_data.columns if "YR" in col],  # Select year columns
    var_name="Year",
    value_name="Net migration"
)

# Clean the Year column (remove "[YRYYYY]")
migration_data_long["Year"] = migration_data_long["Year"].str.extract(r"(\d+)").astype(int)

# Convert Population growth to numeric (handle non-numeric values)
migration_data_long["Net migration"] = pd.to_numeric(migration_data_long["Net migration"], errors="coerce")

# Drop rows with missing values
migration_data_long = migration_data_long.dropna()

# Merge GDP and Population data
merged_data2 = pd.merge(GDP_data_long, migration_data_long, on=["Country Name", "Year"])

# Calculate regression line
slope, intercept, r_value, p_value, std_err = linregress(
    merged_data2["Net migration"], merged_data2["GDP Rate"]
)
line = slope * merged_data2["Net migration"] + intercept

# Plot with regression line
plt.figure(figsize=(10, 6))
plt.scatter(merged_data2["Net migration"], merged_data2["GDP Rate"], color="purple", label="Data")
plt.plot(merged_data2["Net migration"], line, color="black", linestyle="--", 
         label=f"Regression Line (slope={slope:.2f})")
plt.xlabel("Net Migration")
plt.ylabel("GDP Rate (%)")
plt.title("GDP vs. Net Migration in Nigeria (with Regression Line)")
plt.legend()
plt.grid(True)
plt.savefig("Migration_vs_GDP_with_Slope.png", dpi=300, bbox_inches="tight")
plt.show()

# Print correlation metrics
print(f"Correlation Coefficient (r): {r_value:.2f}")
print(f"P-value: {p_value:.4f}")

#Regression Line for Migration vs. GDP (No Simulated Assumptions)
# --------------------------
slope, intercept, r_value, p_value, std_err = linregress(
    merged_data2["Net migration"], merged_data2["GDP Rate"]
)
line = slope * merged_data2["Net migration"] + intercept

plt.figure(figsize=(10, 6))
sns.regplot(x="Net migration", y="GDP Rate", data=merged_data2, 
            scatter_kws={"color": "purple"}, line_kws={"color": "black", "linestyle": "--"})
plt.xlabel("Net Migration")
plt.ylabel("GDP Rate (%)")
plt.title(f"GDP vs. Net Migration in Nigeria (Slope = {slope:.2f})")
plt.grid(True)
plt.savefig("Migration_vs_GDP_with_Slope.png", dpi=300, bbox_inches="tight")
plt.show()


