#!/bin/bash

# Define arrays for different flags
flag1_values=(15 30 45 60) # Example values for flag1
flag2_values=(0.08 0.08 0.08) # Example values for flag2
# Add more arrays for additional flags if needed

# Path to the DataCollection directory on the Desktop
data_collection_dir=~/Desktop/DataCollection

# Iterate through combinations of flag values
for val1 in "${flag1_values[@]}"; do
    for val2 in "${flag2_values[@]}"; do
        # Add loops for more flags if needed

        # Generate a unique filename for this combination of flag values
        filename="data_${val1}_${val2}_$(date +%s).dat"

        # Navigate to the DataCollection directory
        cd "$data_collection_dir"

        # GNU Radio flowgraph Python file is named 'Final_Packet_Error_Test_TX_B200.py'
        # Call the first GNU Radio flowgraph with the current combination of flag values
        python3 Final_Packet_Error_Test_TX_B200.py --g "$val1" --m "$val2" # Replace --g and --m with actual flag names depending on the parameters testing*/*

        # Optional: Wait for the flowgraph to process and transmit data
        sleep 4

        # Call your Python XML-RPC script to set file name on the always-running second flowgraph
        python3 AFRL_Control_April_Autodata_Collection.py set_fn "$filename"
        # Optional: Add delay or additional commands if needed
        sleep 4
    done
done
