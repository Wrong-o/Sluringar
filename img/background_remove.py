from PIL import Image
import os

image_path = 'sluring.webp'  # Update this path to the location of your source image
# Check if the file exists
if os.path.exists(image_path):
    print("File found.")
else:
    print("File not found. Check the path.")

os.listdir()
def remove_white_background(image_path, output_path, tolerance=10):
    """Remove the white background from an image and save the new image with transparency."""
    with Image.open(image_path) as img:
        img = img.convert("RGBA")  # Ensure the image has an alpha channel
        datas = img.getdata()

        newData = []
        for item in datas:
            # Change all white (also consider off-white) pixels to transparent
            if item[0] > 255 - tolerance and item[1] > 255 - tolerance and item[2] > 255 - tolerance:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)
        img.save(output_path, "PNG")

# Specify your image path and output path
image_path = 'sluring.webp'  # Update this path to the location of your source image
output_path = 'sluring1.png'

# Call the function
remove_white_background(image_path, output_path)

