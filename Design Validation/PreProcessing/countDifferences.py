import pandas as pd

# Load the first CSV file
df1 = pd.read_csv("tableData195/C_m01_s01.csv", header=None)

# Load the second CSV file
df2 = pd.read_csv("tableData195/C_m01_s01_smooth.csv", header=None)

# Compare the two DataFrames element-wise and count the differences
num_diff = (df1 != df2).sum().sum()

print("Number of different values between the two CSV files:", num_diff)
