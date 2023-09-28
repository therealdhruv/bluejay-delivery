import pandas as pd

# Load the data from the Excel file
df = pd.read_excel('Assignment_Timecard.xlsx')

# Convert 'Time' and 'Time Out' to datetime
df['Time'] = pd.to_datetime(df['Time'])
df['Time Out'] = pd.to_datetime(df['Time Out'])

# Calculate shift duration in hours
df['Shift Duration'] = (df['Time Out'] - df['Time']).dt.total_seconds() / 3600

# Sort by 'Employee Name' and 'Time'
df.sort_values(['Employee Name', 'Time'], inplace=True)

# Calculate time difference between shifts for each employee
df['Time Diff'] = df.groupby('Employee Name')['Time'].diff().dt.total_seconds() / 3600

# Identify employees who have worked for 7 consecutive days
df['Consecutive Days'] = (df.groupby('Employee Name')['Pay Cycle Start Date'].diff().dt.days == 1).cumsum()
employees_7_days = df[df.groupby('Employee Name')['Consecutive Days'].transform('size') >= 7]['Employee Name'].unique()

# Identify employees who have less than 10 hours and more than 1 hour of time between shifts
employees_time_diff = df[(df['Time Diff'] > 1) & (df['Time Diff'] < 10)]['Employee Name'].unique()

# Identify employees who have worked for more than 14 hours in a single shift
employees_long_shift = df[df['Shift Duration'] > 14]['Employee Name'].unique()

print("\n\nEmployees who have worked for 7 consecutive days: \n")
print(employees_7_days)
print("\nEmployees who have less than 10 hours and more than 1 hour of time between shifts: \n")
print(employees_time_diff)
print("\nEmployees who have worked for more than 14 hours in a single shift: \n")
print(employees_long_shift)
