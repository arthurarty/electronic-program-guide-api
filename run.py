import subprocess

# Define the path to your bash script
script_path = '.wg++/run.sh'

# Start the bash script using subprocess
process = subprocess.Popen(['bash', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for the script to finish and capture the output
stdout, stderr = process.communicate()

# Print the output
print("Standard Output:\n", stdout.decode())
print("Standard Error:\n", stderr.decode())


# TODO: Store the result of the log.
