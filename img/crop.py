from PIL import Image

def crop_image(input_path, output_path, top_left, bottom_right):
    """
    Crop an image based on the top-left and bottom-right coordinates.

    Args:
    input_path (str): Path to the input image file.
    output_path (str): Path to save the cropped image.
    top_left (tuple): Tuple (x1, y1) for the top left corner.
    bottom_right (tuple): Tuple (x2, y2) for the bottom right corner.
    """
    # Load the image
    with Image.open(input_path) as img:
        # Define the box for cropping
        crop_box = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])
        # Crop the image
        cropped_img = img.crop(crop_box)
        # Save or display the cropped image
        cropped_img.save(output_path)
        cropped_img.show()

# Example usage
if __name__ == "__main__":
    input_image_path = 'sluring1.png'  # Update with the actual path to your image
    output_image_path = 'cropped_image.png'  # Update with the desired output path
    top_left_coordinates = (250, 200)  # Update these coordinates as needed
    bottom_right_coordinates = (890, 820)  # Update these coordinates as needed

    crop_image(input_image_path, output_image_path, top_left_coordinates, bottom_right_coordinates)

