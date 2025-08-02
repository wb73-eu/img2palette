from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import colorsys

def convert_hsv_to_rgb(hsv_color):
    """Converts a single HSV color (0-255 scale) to RGB (0-255 scale)."""
    h_norm = hsv_color[0] / 255.0
    s_norm = hsv_color[1] / 255.0
    v_norm = hsv_color[2] / 255.0

    r_norm, g_norm, b_norm = colorsys.hsv_to_rgb(h_norm, s_norm, v_norm)

    return (int(r_norm * 255), int(g_norm * 255), int(b_norm * 255))

def get_palette(image_path, num_colors, color_space='rgb'):
    """
    Extracts a palette of colors from an image using K-Means clustering.

    Args:
        image_path (str): The path to the image file.
        num_colors (int): The number of colors to find.
        color_space (str): The color space to use ('rgb' or 'hsv').

    Returns:
        list: A list of the dominant colors as tuples.
    """

    # Import image
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return []
    
    # Convert image to HSV if chosen
    if color_space == 'hsv':
        image = image.convert('HSV')

    # Convert image to array
    image_array = np.array(image)
    # Flatten array into list of pixels
    pixels = image_array.reshape(-1, image_array.shape[-1])

    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=num_colors, random_state=0, n_init=10)
    kmeans.fit(pixels)

    # Get cluster centers as palette colors
    palette = kmeans.cluster_centers_

    # Convert the palette to integers
    int_palette = palette.astype(int).tolist()

    if color_space == 'hsv':
        rgb_palette = [convert_hsv_to_rgb(color) for color in int_palette]
        return rgb_palette
    else:
        return int_palette

if __name__ == "__main__":
    image_file = "test_image.jpg"
    number_of_colors = 5

    # Get the palette using RGB clustering
    rgb_palette = get_palette(image_file, number_of_colors, color_space='rgb')
    print(f"Dominant Colors (RGB, clustered with RGB):")
    for color in rgb_palette:
        print(f" - {tuple(color)}")

    print("-" * 20)

    # Get the palette using HSV clustering
    hsv_clustered_palette = get_palette(image_file, number_of_colors, color_space='hsv')
    print(f"Dominant Colors (RGB, clustered with HSV):")
    for color in hsv_clustered_palette:
        print(f" - {tuple(color)}")