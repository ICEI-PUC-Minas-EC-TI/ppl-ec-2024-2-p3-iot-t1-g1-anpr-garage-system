import os
from PIL import Image
import hashlib
from pathlib import Path

def get_image_hash(image_path):
    """Calculate image hash using MD5 on the image data."""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if image is in RGBA format
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # Get the raw image data
            img_data = img.tobytes()
            
            # Calculate hash
            return hashlib.md5(img_data).hexdigest()
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None

def find_and_remove_duplicates(directory):
    """Find and remove duplicate images in the specified directory."""
    # Dictionary to store image hashes
    image_hashes = {}
    
    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    
    # Convert directory to Path object
    dir_path = Path(directory)
    
    # Counter for statistics
    stats = {
        'total_images': 0,
        'duplicates_found': 0,
        'errors': 0
    }
    
    print(f"Scanning directory: {directory}")
    
    # Iterate through all files in directory
    for file_path in dir_path.glob('*'):
        if file_path.suffix.lower() in image_extensions:
            stats['total_images'] += 1
            
            # Calculate hash
            img_hash = get_image_hash(file_path)
            
            if img_hash is None:
                stats['errors'] += 1
                continue
                
            if img_hash in image_hashes:
                # Found a duplicate
                stats['duplicates_found'] += 1
                print(f"Found duplicate: {file_path}")
                print(f"Original: {image_hashes[img_hash]}")
                
                # Remove the duplicate
                try:
                    file_path.unlink()
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {str(e)}")
                    stats['errors'] += 1
            else:
                # New image
                image_hashes[img_hash] = file_path
    
    # Print statistics
    print("\nSummary:")
    print(f"Total images processed: {stats['total_images']}")
    print(f"Duplicates found and removed: {stats['duplicates_found']}")
    print(f"Errors encountered: {stats['errors']}")

if __name__ == "__main__":
    # Get directory path from user
    directory = input("Enter the directory path to check for duplicate images: ")
    
    # Verify directory exists
    if not os.path.isdir(directory):
        print("Error: Invalid directory path")
        exit(1)
    
    # Process the directory
    find_and_remove_duplicates(directory)