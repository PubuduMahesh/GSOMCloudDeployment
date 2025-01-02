import os
import numpy as np
import pandas as pd
import gsom

# Construct the absolute path to the data file
data_filename = os.path.join(os.path.dirname(__file__), "data", "zoo.txt")

# Define the output directory
output_dir = os.path.join(os.path.dirname(__file__), "../output")
os.makedirs(output_dir, exist_ok=True)

if __name__ == '__main__':
    np.random.seed(1)
    df = pd.read_csv(data_filename)
    print(df.shape)
    data_training = df.iloc[:, 1:17]

    # Train the GSOM map
    gsom_map = gsom.GSOM(.83, 16, max_radius=4)
    gsom_map.fit(data_training.to_numpy(), 100, 50)

    # Drop unnecessary columns and predict
    df = df.drop(columns=["label"])
    map_points = gsom_map.predict(df, "Name")

    # Change the working directory to the output directory
    current_dir = os.getcwd()
    os.chdir(output_dir)
    
    # Plot the GSOM map (output will be saved to the output directory)
    gsom.plot(map_points, "Name", gsom_map=gsom_map)

    # Restore the original working directory
    os.chdir(current_dir)

    # Save the GSOM output to the output directory
    csv_output_path = os.path.join(output_dir, "gsom.csv")
    map_points.to_csv(csv_output_path, index=False)

    print(f"CSV file saved to {csv_output_path}")
    print(f"PDF (if generated) saved to {output_dir}")
    print("Complete")
