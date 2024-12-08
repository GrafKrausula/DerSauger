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
    else:
        file_name, file_ext = os.path.splitext(os.path.basename(input_file))
        if file_ext.lower() != ".png":
            raise ValueError(f"{input_file} is not a PNG file")

    sizes = [16, 32, 48, 64, 128, 256]
    ico_images = []
    try:
        with Image.open(input_file) as img:
            for size in sizes:
                # Resize the image
                resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
                
                # Save the resized image
                output_file = os.path.join(output_folder, f"{file_name}_{size}.png")
                resized_img.save(output_file)
                print(f"Saved: {output_file}")
                
                # Add the resized image to the .ico list
                if size in [16, 32, 48, 64]:  # Include only standard sizes for .ico
                    ico_images.append(resized_img)
            
            # Create an .ico file
            ico_path = os.path.join(output_folder, f"icon.ico")
            ico_images[0].save(ico_path, format='ICO', sizes=[(size, size) for size in [16, 32, 48, 64]])
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
