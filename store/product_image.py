import os
from PIL import Image
import requests

directory_path = "media/media_file/"  # Path to the media folder

api_endpoint = "http://localhost:8000/api/update-productImage/"  # API endpoint to upload the files

# Get the absolute path to the media folder
absolute_directory_path = os.path.abspath(directory_path)

# Check if the given path is a directory
if os.path.isdir(absolute_directory_path):
    # List all files in the directory
    file_list = os.listdir(absolute_directory_path)

    # Iterate over each file in the directory
    for file_name in file_list:
        # Get the absolute path of the file
        file_path = os.path.join(absolute_directory_path, file_name)

        # Check if the path is a file
        if os.path.isfile(file_path):
            # Check if the file is an image
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                # Open the image using PIL's Image module
                image = Image.open(file_path)

                # Print the file name
                # print(f"Image File Name: {file_name}")

                # Perform operations on the image as needed
                # For example, you can access image properties like size, format, etc.
                image_size = image.size
                image_format = image.format
                 # Create a dictionary for the file data to be sent as multipart form-data
                files = {'media_file': (file_name, open(file_path, 'rb'), f'image/{image_format.lower()}')}

                try:
                    # Send a POST request to the API endpoint with the file data
                    response = requests.post(api_endpoint, files=files)

                    # Check the response status code
                    if response.status_code == 200:
                        print(f"Successfully uploaded {file_name}")
                    else:
                        print(f"Failed to upload {file_name}")
                except requests.exceptions.RequestException as e:
                    print(f"Error occurred while uploading {file_name}: {e}")

                # print(f"Image Size: {image_size}")
                # print(f"Image Format: {image_format}")
                # print("---------------------------------")
else:
    print("Invalid directory path.")
