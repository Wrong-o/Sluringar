from PIL import Image

def transform_image(image_path, x_scale, y_scale, output_path):
    """
    Transforms an image's dimensions by scaling its width and height independently.
    
    Args:
    image_path (str): The path to the input image file.
    x_scale (float): The scaling factor for the width.
    y_scale (float): The scaling factor for the height.
    output_path (str): The path to save the transformed image.
    """
    # Load the image
    img = Image.open(image_path)
    
    # Calculate new dimensions
    new_width = int(img.width * x_scale)
    new_height = int(img.height * y_scale)
    
    try:
        # Try using the newer resampling method
        transformed_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    except AttributeError:
        # Fallback to older method if Resampling is not available
        transformed_img = img.resize((new_width, new_height), Image.ANTIALIAS)
    
    # Save the transformed image
    transformed_img.save(output_path)

# Example usage (uncommented for testing)
transform_image('sluring1.png', 1.22, 0.73, 'sluring9.png')

