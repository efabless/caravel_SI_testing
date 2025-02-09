
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
            
            # Check if the length of the line is divisible by 8
            if len(line) % 8 != 0:
                # Pad the line with 0's at the end to make the length divisible by 8
                padding = 8 - len(line) % 8
                line = line + '0' * padding
            
            # Convert the line of '0' and '1' to binary (as bytes)
            binary_data.extend(int(line, 2).to_bytes(len(line) // 8, byteorder='big'))
        
    # Write the binary data to the output file
    with open(output_file, 'wb') as out_file:
        out_file.write(binary_data)

    print(f"Binary file '{output_file}' created successfully.")




# convert input to binary
input_file = 'caravel_aes_dft.vec.bin'   # Replace with the path to your input text file
output_file = 'aes_in_vectors.bin'  # Replace with the path where you want the binary file
convert_to_binary(input_file, output_file)

# convert output to binary
input_file = 'caravel_aes_dft.out.bin'   # Replace with the path to your input text file
output_file = 'aes_out_vectors.bin'  # Replace with the path where you want the binary file
convert_to_binary(input_file, output_file)

