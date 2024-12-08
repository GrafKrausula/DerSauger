from generate_extension_icons import scale_png_to_sizes
import os

icon_base = "Sauger.png"
output_folder = r"..\DerSauger\Sauger Chrome Extension\images"
input_file = os.path.join(output_folder, icon_base)

scale_png_to_sizes(input_file, output_folder)
