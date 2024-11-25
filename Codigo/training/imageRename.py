import os
import random
from pathlib import Path
import shutil

def rename_images(input_directory):
    """
    Rename images in a directory with train/test split naming convention.
    
    Args:
        input_directory (str): Path to directory containing images
    """
    # Supported image extensions
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    
    # Get all image files from directory
    image_files = [
        f for f in os.listdir(input_directory)
        if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS
    ]
    
    if not image_files:
        print("No image files found in the specified directory.")
        return
    
    # Calculate split counts
    total_images = len(image_files)
    train_count = int(total_images * 0.8)
    
    # Randomly select files for train set
    train_files = random.sample(image_files, train_count)
    test_files = list(set(image_files) - set(train_files))
    
    # Create counters for train and test
    train_counter = 1
    test_counter = 1
    
    # Process training files
    for file in train_files:
        old_path = os.path.join(input_directory, file)
        extension = os.path.splitext(file)[1]
        new_name = f"lp_train_{train_counter:04d}{extension}"
        new_path = os.path.join(input_directory, new_name)
        
        # Handle case where file already exists
        while os.path.exists(new_path):
            train_counter += 1
            new_name = f"lp_train_{train_counter:04d}{extension}"
            new_path = os.path.join(input_directory, new_name)
        
        os.rename(old_path, new_path)
        train_counter += 1
    
    # Process test files
    for file in test_files:
        old_path = os.path.join(input_directory, file)
        extension = os.path.splitext(file)[1]
        new_name = f"lp_test_{test_counter:04d}{extension}"
        new_path = os.path.join(input_directory, new_name)
        
        # Handle case where file already exists
        while os.path.exists(new_path):
            test_counter += 1
            new_name = f"lp_test_{test_counter:04d}{extension}"
            new_path = os.path.join(input_directory, new_name)
        
        os.rename(old_path, new_path)
        test_counter += 1
    
    print(f"Renamed {len(train_files)} training images and {len(test_files)} test images.")
    print(f"Train/Test split: {len(train_files)/total_images:.1%}/{len(test_files)/total_images:.1%}")

if __name__ == "__main__":
    # Get directory path from user
    directory = input("Enter the directory path containing images: ")
    
    # Validate directory exists
    if not os.path.isdir(directory):
        print("Invalid directory path!")
    else:
        rename_images(directory)