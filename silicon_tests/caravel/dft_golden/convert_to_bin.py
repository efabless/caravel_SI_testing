
def convert_to_binary(input_file, output_file):
    with open(input_file, 'r') as f:
        # Skip the first 7 header lines
        for _ in range(7):
            next(f)
        
        # Read the rest of the file and convert the 0's and 1's lines to binary
        binary_data = bytearray()
        
        for line in f:
            # Strip newline characters and any unwanted spaces
            line = line.strip()
            
            # Convert the line of '0' and '1' to binary (as bytes)
            binary_data.extend(int(line, 2).to_bytes((len(line) + 7) // 8, byteorder='big'))
        
    # Write the binary data to the output file
    with open(output_file, 'wb') as out_file:
        out_file.write(binary_data)

    print(f"Binary file '{output_file}' created successfully.")

def create_mask(input_file, output_file):
    # Open the input file for reading and the output file for writing
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for _ in range(7):
            next(infile)
        # Read the file line by line
        for line in infile:
            # Replace 'X' with '1' and '0' or '1' with '0'
            masked_line = ''.join('0' if char == 'x' else '1' for char in line.strip())
            
            # Write the processed line to the output file
            outfile.write(masked_line + '\n')
    
    print(f"Mask file '{output_file}' created successfully!")


def find_zero_ranges_in_first_line(file_path):
    with open(file_path, 'r') as f:
        # Read the first line from the file
        first_line = f.readline().strip()  # Strip to remove any trailing newline or spaces
        
        zero_ranges = []  # To store ranges of 0s
        start_index = None  # To track the start of a zero sequence
        length = len(first_line)  # Length of the line

        # Iterate over the characters in the first line in reverse order (from right to left)
        for index in range(length - 1, -1, -1):  # Start from the last character
            char = first_line[index]
            
            # Calculate the right-to-left index (starting from 0 for the rightmost character)
            right_to_left_index = length - 1 - index

            if char == '0':
                # If this is the first zero or part of an ongoing zero sequence
                if start_index is None:
                    start_index = right_to_left_index  # Mark the start of a zero sequence
            else:
                # If this is a 1, and we were tracking a zero sequence, close it
                if start_index is not None:
                    zero_ranges.append((start_index, right_to_left_index - 1))  # Store range (start, end) for this zero block
                    start_index = None  # Reset for the next sequence

        # If the first line ends with zeros, close the range
        if start_index is not None:
            zero_ranges.append((start_index, right_to_left_index))  # The range ends at the leftmost position (index 0)
        
        # Reverse the ranges to return them in left-to-right order
        return zero_ranges[::-1]



def remove_Xs(input_file, output_file):
    # Open the input file for reading and the output file for writing
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Read the file line by line
        for line in infile:
            # Replace 'X' with '0' and leave '0' or '1' as they are
            modified_line = ''.join('0' if char == 'x' else char for char in line.strip())
            
            # Write the processed line to the output file
            outfile.write(modified_line + '\n')
    
    print(f"Modified file '{output_file}' created successfully!")


# create mask 
input_file = 'mgmt_core_wrapper.out.bin'  # Your input file with 0s, 1s, and Xs
output_file = 'mask.txt'  # The output file to store the mask
create_mask(input_file, output_file)

# Example usage
file_path = 'mask.txt'  # Replace with your text file path
ranges = find_zero_ranges_in_first_line(file_path)
# Output the ranges of zeros
for start, end in ranges:
    print(f"Zeros from index {start} to {end}")


# remove Xs from out vectors 
input_file = 'mgmt_core_wrapper.out.bin'  # Your input file with 0s, 1s, and Xs
output_file = 'out_vectors.txt'  # The output file to store the mask
remove_Xs(input_file, output_file)


# convert input to binary
input_file = 'mgmt_core_wrapper.vec.bin'   # Replace with the path to your input text file
output_file = 'in_vectors.bin'  # Replace with the path where you want the binary file
convert_to_binary(input_file, output_file)

# convert output to binary
input_file = 'out_vectors.txt'   # Replace with the path to your input text file
output_file = 'out_vectors.bin'  # Replace with the path where you want the binary file
convert_to_binary(input_file, output_file)

# convert mask to binary
input_file = 'mask.txt'   # Replace with the path to your input text file
output_file = 'mask.bin'  # Replace with the path where you want the binary file
convert_to_binary(input_file, output_file)

