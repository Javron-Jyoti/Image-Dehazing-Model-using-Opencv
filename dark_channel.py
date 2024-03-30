import cv2
import numpy as np
image = 'fog.jpg'

def compute_dark_channel(image, window_size=15):
    min_channel = np.min(image, axis=2)  # Use np.min() instead of cv2.min()
    return cv2.erode(min_channel, kernel=cv2.getStructuringElement(cv2.MORPH_RECT, (window_size, window_size)))

def estimate_atmospheric_light(image, dark_channel):
    flat_dark_channel = dark_channel.flatten()
    sorted_indices = flat_dark_channel.argsort()[::-1]
    top_indices = sorted_indices[:int(len(sorted_indices) * 0.001)]  # Consider top 0.1% brightest pixels
    atmospheric_light = [max(image.flatten()[i]) for i in top_indices]
    return atmospheric_light

def compute_transmission_map(dark_channel, atmospheric_light, omega=0.95):
    transmission_map = 1 - omega * dark_channel / atmospheric_light
    return transmission_map

def dehaze(image, transmission_map, atmospheric_light, t0=0.1):
    t_clipped = cv2.max(transmission_map, t0)  # Clip transmission to avoid division issues
    dehazed_image = (image - atmospheric_light) / t_clipped[:, :, None] + atmospheric_light
    dehazed_image = cv2.normalize(dehazed_image, None, 0, 255, cv2.NORM_MINMAX)  # Normalize to [0, 255]
    dehazed_image = dehazed_image.astype('uint8')
    return dehazed_image

# Load the image
image_path = 'fog.jpg'
hazy_image = cv2.imread(image_path)

# Check if the image is loaded successfully
if hazy_image is None:
    print(f"Error: Unable to load the image from {image_path}")
    exit()

# Check the dimensions of the loaded image
if len(hazy_image.shape) < 3:
    print("Error: The loaded image does not have the expected number of dimensions.")
    print(f"Image shape: {hazy_image.shape}")
    exit()

# Compute dark channel
dark_channel = compute_dark_channel(hazy_image)

# Estimate atmospheric light
atmospheric_light = estimate_atmospheric_light(hazy_image, dark_channel)

# Compute transmission map
transmission_map = compute_transmission_map(dark_channel, atmospheric_light)

# Dehaze the image
dehazed_image = dehaze(hazy_image, transmission_map, atmospheric_light)

# Save the dehazed image
cv2.imwrite('dehazed_image.jpg', dehazed_image)
