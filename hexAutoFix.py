#code for file carving automation jpg dan png berhasil, gif masih failed (final code).
import os

def carve_files(input_files, output_directory):
    combined_data = bytearray()
    file_counter = 1  # Untuk memberikan nama unik kepada setiap file

    # Iterate over the input files
    for input_file in input_files:
        with open(input_file, 'rb') as file:
            # Read the entire content of the file and append to the combined data
            combined_data += file.read()

    file_info = {
        'jpg': {
            'signature': b'\xFF\xD8\xFF\xE0',
            'end_marker': b'\xFF\xD9'
        },
        'png': {
            'signature': b'\x89\x50\x4E\x47',
            'end_marker': b'IEND\xAE\x42\x60\x82'
        },
        'gif': {
            'signature': b'\x47\x49\x46\x38',
            'end_marker': b'\x3B'
        },
        # Add more file types as needed
    }

    # Iterate over the file signatures
    for extension, info in file_info.items():
        start_index = combined_data.find(info['signature'])

        # Continue searching until the signature is not found
        while start_index != -1:
            end_index = combined_data.find(info['end_marker'], start_index)

            # Check if the ending index is found
            if end_index != -1:
                # Carve the file data between the start and end indices
                file_data = combined_data[start_index:end_index + len(info['end_marker'])]

                # Create the output file path with a unique name
                output_file = os.path.join(output_directory, f'carved_file_{file_counter:03d}.{extension}')

                # Write the carved file data to the output file
                with open(output_file, 'wb') as output_file:
                    output_file.write(file_data)

                # Print information about the extracted file
                print(f'File {output_file} extracted successfully.')

                # Update the start index to continue searching
                start_index = combined_data.find(info['signature'], end_index + len(info['end_marker']))

                # Increment the file counter for the next unique name
                file_counter += 1
            else:
                # Signature is found but ending index is not found, break the loop
                break

# Usage example with multiple input files
input_files = [
    r'C:\FIleCarving\USB-TOSHIBA01-002-12-2023.001.dd',
    r'C:\FIleCarving\USB-TOSHIBA01-002-12-2023.002.dd'
    # Add more input files as needed
]
output_directory = r'C:\Users\Lenovo\Desktop\Skripsi\Percobaan Ketiga Otomatis 300 File Gambar\TESHASIL'
carve_files(input_files, output_directory)
