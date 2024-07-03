import os

def create_dummy_images(prefix, start_index, end_index, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(start_index, end_index + 1):
        # Generate file name
        filename = f"{prefix}_{i:04d}.png"
        filepath = os.path.join(output_dir, filename)
        
        # Generate dummy content (just an example, you can modify as needed)
        dummy_content = f"This is dummy image {i}."
        
        # Write content to file
        with open(filepath, 'w') as f:
            f.write(dummy_content)

if __name__ == "__main__":
    # Define parameters
    prefix = "foo_test"
    start_index = 1
    end_index = 2000
    output_directory = "./dummy_images"
    
    # Call function to create dummy images
    create_dummy_images(prefix, start_index, end_index, output_directory)