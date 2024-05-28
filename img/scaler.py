from PIL import Image
import os

def resize_images(source_folder, scale_factor=0.1, target_folder=None):
    # If no target folder is provided, create a subfolder 'resized' within the source folder
    if target_folder is None:
        target_folder = os.path.join(source_folder, "resized")
        os.makedirs(target_folder, exist_ok=True)

    # List all files in the source folder
    files = os.listdir(source_folder)

    # Process each file
    for file in files:
        # Construct file path
        file_path = os.path.join(source_folder, file)
        
        # Open the image
        with Image.open(file_path) as img:
            # Calculate new dimensions
            new_width = int(img.width * scale_factor)
            new_height = int(img.height * scale_factor)

            # Resize the image
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)


            # Construct the target file path
            target_file_path = os.path.join(target_folder, file)

            # Save the resized image
            resized_img.save(target_file_path)

    print(f"Images resized and saved in {target_folder}")

# Example usage (commented out):
resize_images(".\sluring", 0.08, ".\sluring_small")

# The above function call is commented out to prevent execution in the PCI. Uncomment it for local testing or final deployment.
