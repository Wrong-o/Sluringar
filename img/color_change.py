from PIL import Image
import os

def swap_green_blue(image_path, output_path):
    """
    Swap the green and blue values in the pixels of the image.
    
    :param image_path: Path to the input image
    :param output_path: Path to save the output image
    """
    with Image.open(image_path) as img:
        img = img.convert("RGBA")  # Ensure the image has an alpha channel
        datas = img.getdata()

        newData = []
        for item in datas:
            new_pixel = (item[0], item[2], item[1], item[3])  # Swap green and blue
            newData.append(new_pixel)

        img.putdata(newData)
        img.save(output_path, "PNG")

# Specify your image path and output path
image_path = '/mnt/data/sluring1.png'
output_path = '/mnt/data/output_image_swapped.png'

# Call the function to swap green and blue
swap_green_blue(image_path, output_path)

print(f"The image with swapped green and blue values has been saved to {output_path}")
