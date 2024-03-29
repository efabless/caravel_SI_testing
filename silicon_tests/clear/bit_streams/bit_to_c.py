import os

# Directory containing the .bit files
bit_streams_dir = '/home/marwan/blizzard_SI_testing/caravel_board/firmware_vex/blizzard/bit_streams/'

def file_to_c_array(input_file, output_file):
    try:
        # Read the binary file
        with open(input_file, 'rb') as f:
            content = f.read()

        # Convert each byte to its hexadecimal representation
        c_array = ', '.join('0x{:02x}'.format(byte) for byte in content)

        # Write the C array to the output file
        with open(output_file, 'w') as f:
            array_name = os.path.splitext(os.path.basename(output_file))[0]
            f.write(f'#ifndef {array_name.upper()}_H\n')
            f.write(f'#define {array_name.upper()}_H\n\n')
            f.write(f'const unsigned char {array_name}[] = {{\n')
            f.write('    ' + c_array)
            f.write('\n};\n')
            f.write(f'const unsigned int {array_name}_size = sizeof({array_name});\n\n')
            f.write(f'#endif // {array_name.upper()}_H\n')

    except IOError as e:
        print("An error occurred:", e)

# Iterate over all .bit files in the specified directory and convert them
for file_name in os.listdir(bit_streams_dir):
    if file_name.endswith('.bit'):
        input_file_path = os.path.join(bit_streams_dir, file_name)
        output_file_name = os.path.splitext(file_name)[0] + '.h'
        output_file_path = os.path.join(bit_streams_dir, output_file_name)
        file_to_c_array(input_file_path, output_file_path)
        print(f"Converted {file_name} to {output_file_name}")