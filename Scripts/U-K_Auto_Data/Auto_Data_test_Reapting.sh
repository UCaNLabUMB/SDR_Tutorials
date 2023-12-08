#!/bin/bash

# Check if the number of times to run the script is passed as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <number_of_times_to_run>"
    exit 1
fi

# Assign the first argument to a variable
number_of_runs=$1

# Path to the Python script
python_script="Packet_test_file_in_bash.py"

# Loop to run the Python script the specified number of times
for ((i=1; i<=number_of_runs; i++)); do
    echo "Running the script: ${i}/${number_of_runs}"
    python3 "$python_script" --f "$i"
    
    # Optional: sleep 1 second between runs, can be adjusted as needed
    sleep 1
done

echo "Script execution completed."
