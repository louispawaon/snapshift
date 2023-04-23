import os
import pyheif
from PIL import Image

input_folder = input("Enter the path to input folder: ") #Change path folder
output_folder = "path/to/your/output/folder" #Change path folder

for filename in os.listdir(input_folder):
    if filename.endswith(".heic"):
        # Load the HEIC file
        heif_file = pyheif.read(os.path.join(input_folder, filename))

        # Convert the image data to a PIL Image object
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )

        # Save the PIL Image object as a JPG file in the output folder
        output_filename = os.path.splitext(filename)[0] + ".jpg"
        output_path = os.path.join(output_folder, output_filename)
        image.save(output_path)

        print(f"Converted {filename} to {output_filename}")