from picamera2 import Picamera2
import cv2
import os
from datetime import datetime

# Create the teste directory if it doesn't exist
if not os.path.exists('./teste'):
    os.makedirs('./teste')

# Initialize Picamera2
picam2 = Picamera2()

# Set the capture configuration
capture_config = picam2.create_still_configuration(main={"size": (1640, 1232)})
picam2.configure(capture_config)

# Start the camera
picam2.start()

print("Taking picture...")
# Capture a single frame
frame = picam2.capture_array()

# Generate filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f'./teste/image_{timestamp}.jpg'

# Save the full resolution image
cv2.imwrite(filename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
print(f"Image saved as {filename}")

picam2.stop()