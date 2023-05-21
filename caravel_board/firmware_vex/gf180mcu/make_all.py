import os
import logging

# Get the current working directory
cwd = os.getcwd()

# Create a logger object
logger = logging.getLogger("make_logger")
logger.setLevel(logging.INFO)

# Create a file handler and add it to the logger
file_handler = logging.FileHandler("make_all.log")
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

# Loop through all directories in the current working directory
for root, dirs, files in os.walk(cwd):
    # Get the directory name using os.path.basename
    dir_name = os.path.basename(root)
    # Check if there is a Makefile in the current directory
    if "Makefile" in files:
        # Print the directory name and run the make command
        logger.info(f"Running make in {dir_name}")
        os.chdir(root)
        make_output = os.popen("make clean").read()
        logger.info(make_output)
        os.chdir(cwd)
