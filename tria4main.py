import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
data = pd.read_csv(r"C:\Users\adity\OneDrive\Documents\dc_project\data_raw.csv")
print(data.shape)
# Extract the time and current data for each sensor
sensor1_time = data["s1"]
sensor1_current = data["µA1"]

sensor2_time = data["s2"]
sensor2_current = data["µA2"]

sensor3_time = data["s3"]
sensor3_current = data["µA3"]

sensor4_time = data["s4"]
sensor4_current = data["µA4"]



# Plot Sensor 1
plt.figure(figsize=(10, 6))
plt.plot(sensor1_time, sensor1_current, color='blue')
plt.xlabel('Time')
plt.ylabel('Current (µA)')
plt.title('Sensor 1 Data')
plt.show()

# Plot Sensor 2
plt.figure(figsize=(10, 6))
plt.plot(sensor2_time, sensor2_current, color='red')
plt.xlabel('Time')
plt.ylabel('Current (µA)')
plt.title('Sensor 2 Data')
plt.show()

# Plot Sensor 3
plt.figure(figsize=(10, 6))
plt.plot(sensor3_time, sensor3_current, color='green')
plt.xlabel('Time')
plt.ylabel('Current (µA)')
plt.title('Sensor 3 Data')
plt.show()

# Plot Sensor 4
plt.figure(figsize=(10, 6))
plt.plot(sensor4_time, sensor4_current, color='orange')
plt.xlabel('Time')
plt.ylabel('Current (µA)')
plt.title('Sensor 4 Data')
plt.show()

# Calculate the range of time values for each sensor
sensor1_time_range = sensor1_time.max() - sensor1_time.min()
sensor2_time_range = sensor2_time.max() - sensor2_time.min()
sensor3_time_range = sensor3_time.max() - sensor3_time.min()
sensor4_time_range = sensor4_time.max() - sensor4_time.min()

# Calculate the segment size for each sensor
sensor1_segment_size = sensor1_time_range / 10
sensor2_segment_size = sensor2_time_range / 10
sensor3_segment_size = sensor3_time_range / 10
sensor4_segment_size = sensor4_time_range / 10

# Initialize the segment boundaries for each sensor
sensor1_segment_boundaries = [sensor1_time.min() + i * sensor1_segment_size for i in range(11)]
sensor2_segment_boundaries = [sensor2_time.min() + i * sensor2_segment_size for i in range(11)]
sensor3_segment_boundaries = [sensor3_time.min() + i * sensor3_segment_size for i in range(11)]
sensor4_segment_boundaries = [sensor4_time.min() + i * sensor4_segment_size for i in range(11)]

# Create a DataFrame to store the results
results = pd.DataFrame(columns=["Sensor", "Segment", "Min Value", "Max Value", "deltaR", "abs_deltaR"])

# Calculate the minimum and maximum values for each segment for each sensor
for sensor_name, time_column, current_column, segment_boundaries in zip(
    ["Sensor 1", "Sensor 2", "Sensor 3", "Sensor 4"],
    [sensor1_time, sensor2_time, sensor3_time, sensor4_time],
    [sensor1_current, sensor2_current, sensor3_current, sensor4_current],
    [sensor1_segment_boundaries, sensor2_segment_boundaries, sensor3_segment_boundaries, sensor4_segment_boundaries]
):
    for i in range(10):
        start = segment_boundaries[i]
        end = segment_boundaries[i + 1]  # Include the next segment's starting point
        if start <= 10:
            start = 11  # Ignore values in the range 0-10
        segment_current = current_column[(time_column >= start) & (time_column < end)]
        min_value = segment_current.min()
        max_value = segment_current.max()
        deltaR = max_value - min_value
        abs_deltaR = (max_value - min_value) / min_value
        new_row = pd.Series([sensor_name, i + 1, min_value, max_value, deltaR, abs_deltaR], index=results.columns)
        results = pd.concat([results, new_row.to_frame().T], ignore_index=True)

    # Save the results to a CSV file
    results.to_csv(r"C:\Users\adity\OneDrive\Documents\dc_project\result_2features.csv", index=False)



#.....................................................

#.................................................
# Define the alpha values
alpha_values = [0.1, 0.01, 0.001]

# Calculate y(s) for each alpha value for each sensor
for alpha in alpha_values:
    # Create new columns for y(s) at the current alpha value for each sensor
    sensor1_y = [(1 - alpha) * sensor1_current[i - 1] + alpha * (sensor1_current[i] - sensor1_current[i - 1])
                 if i > 0 else 0 for i in range(len(sensor1_current))]
    sensor2_y = [(1 - alpha) * sensor2_current[i - 1] + alpha * (sensor2_current[i] - sensor2_current[i - 1])
                 if i > 0 else 0 for i in range(len(sensor2_current))]
    sensor3_y = [(1 - alpha) * sensor3_current[i - 1] + alpha * (sensor3_current[i] - sensor3_current[i - 1])
                 if i > 0 else 0 for i in range(len(sensor3_current))]
    sensor4_y = [(1 - alpha) * sensor4_current[i - 1] + alpha * (sensor4_current[i] - sensor4_current[i - 1])
                 if i > 0 else 0 for i in range(len(sensor4_current))]

    # Add the new columns to the DataFrame
    data[f"Sensor 1 y({alpha})"] = sensor1_y
    data[f"Sensor 2 y({alpha})"] = sensor2_y
    data[f"Sensor 3 y({alpha})"] = sensor3_y
    data[f"Sensor 4 y({alpha})"] = sensor4_y


# Save the modified data to a new CSV file
data.to_csv(r"C:\Users\adity\OneDrive\Documents\dc_project\data_raw_with_y(k).csv", index=False)

#......................................................

# Read the CSV file with y(s) values
data_with_y = pd.read_csv(r"C:\Users\adity\OneDrive\Documents\dc_project\data_raw_with_y(k).csv")

# Define the alpha values
alpha_values = [0.1, 0.01, 0.001]

# Create a DataFrame to store the results for y(s) segments
y_segment_results = pd.DataFrame(columns=["Sensor", "Segment", "Alpha", "Min Value", "Max Value"])

# Generate graphs for each y(s) value and calculate segment min/max
for sensor_num in range(1, 5):
    for alpha in alpha_values:
        sensor_name = f"Sensor {sensor_num}"
        y_column_name = f"{sensor_name} y({alpha})"

        # Plot the y(s) value for the current alpha value
        plt.figure(figsize=(10, 6))
        plt.plot(data_with_y[y_column_name])
        plt.xlabel('Time')
        plt.ylabel(f'y({alpha})')
        plt.title(f'{sensor_name} y({alpha})')
        plt.show()

        # Calculate the minimum and maximum values for each segment for the current alpha value
        for segment_num in range(10):
            segment_start = segment_num * 10
            segment_end = (segment_num + 1) * 10
            segment_values = data_with_y[y_column_name][segment_start:segment_end]
            min_value = segment_values.min()
            max_value = segment_values.max()
            new_row = pd.Series([sensor_name, segment_num + 1, alpha, min_value, max_value], index=y_segment_results.columns)
            y_segment_results = pd.concat([y_segment_results, new_row.to_frame().T], ignore_index=True)

# Save the results for y(s) segments to the CSV file
y_segment_results.to_csv(r"C:\Users\adity\OneDrive\Documents\dc_project\result_next_6features.csv", index=False)