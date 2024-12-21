import argparse
from PIL import Image
import os

def scale_png_to_sizes(input_file, output_folder):
    """
    Scales a PNG image to multiple sizes, saves them as output files, and creates an .ico file.
    
    Args:
        input_file (str): Path to the input PNG file.
        output_folder (str): Path to the folder where output files will be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"{input_file} is not a file")
    
    file_name, file_ext = os.path.splitext(os.path.basename(input_file))
    if file_ext.lower() != ".png":
        raise ValueError(f"{input_file} is not a PNG file")

    sizes = [16, 32, 48, 256]  # Standard sizes for ICO files
    ico_images = {}
    
    try:
        with Image.open(input_file) as img:
            img = img.convert("RGBA")  # Ensure the image has an alpha channel
            
            for size in sizes:
                # Resize the image to the required size
                resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
                
                # Save the resized image to the output folder
                output_file = os.path.join(output_folder, f"{file_name}_{size}.png")
                resized_img.save(output_file)
                print(f"Saved: {output_file}")
                
                # Add the resized image to the dictionary for ICO creation
                ico_images[size] = resized_img

            # Ensure all required sizes are available
            required_sizes = set(sizes)
            available_sizes = set(ico_images.keys())
            if not required_sizes.issubset(available_sizes):
                missing_sizes = required_sizes - available_sizes
                raise ValueError(f"Missing required sizes for ICO file: {missing_sizes}")
            
            # Define the path for the .ico file
            ico_path = os.path.join(output_folder, "icon.ico")
            
            # Delete existing file if necessary
            if os.path.exists(ico_path):
                os.remove(ico_path)

            # Save the .ico file, using the largest size as the base
            largest_image = ico_images[256]  # Use the 256x256 image as the base
            largest_image.save(
                ico_path,
                format="ICO",
                sizes=[(size, size) for size in sizes]
            )
            print(f"Saved: {ico_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Scale a PNG image to multiple sizes and create an .ico file.")
    parser.add_argument("input_file", type=str, help="Path to the input PNG file.")
    parser.add_argument("output_folder", type=str, help="Path to the output folder.")

    args = parser.parse_args()

    try:
        scale_png_to_sizes(args.input_file, args.output_folder)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
