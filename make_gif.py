from PIL import Image
import os
from year_by_year_png import make_impact_by_year_png
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

def make_gif():

    make_impact_by_year_png()

    # Input folder containing PNG images
    input_folder = "meteorite_impacts_by_year"

    # Output GIF filename
    output_gif = "gif_files\impacts.gif"

    # Create a list to store image objects
    frames = []

    # List all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            img = Image.open(os.path.join(input_folder, filename))
            frames.append(img)

    # Save the frames as a GIF
    frames[0].save(
        output_gif,
        save_all=True,
        append_images=frames[1:],
        duration=100,  # Set the frame duration in milliseconds
        loop=0,  # Set loop to 0 for infinite loop, or you can specify the number of loops
    )

    print(f"GIF saved as {output_gif}")

if __name__ == "__main__":
    make_gif()
