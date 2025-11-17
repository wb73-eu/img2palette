from PIL import Image
from collections import Counter
import numpy as np
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import colorsys
import argparse

def convert_hsv_to_rgb(hsv_color):
    """Converts a single HSV color (0-255 scale) to RGB (0-255 scale)."""
    h_norm = hsv_color[0] / 255.0
    s_norm = hsv_color[1] / 255.0
    v_norm = hsv_color[2] / 255.0

    r_norm, g_norm, b_norm = colorsys.hsv_to_rgb(h_norm, s_norm, v_norm)

    return (int(r_norm * 255), int(g_norm * 255), int(b_norm * 255))

def get_palette(image_path, num_colors, color_space='rgb', model='kmeans'):
    """
    Extracts a palette of colors from an image using K-Means clustering.

    Args:
        image_path (str): The path to the image file.
        num_colors (int): The number of colors to find.
        color_space (str): The color space to use ('rgb' or 'hsv').
        model (str): The model used for clustering ('kmeans' or 'gmm'z)

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

    if model == 'kmeans':
        # Apply K-Means clustering
        kmeans = KMeans(n_clusters=num_colors, random_state=0)
        kmeans.fit(pixels)
        # Get cluster centers as palette colors
        palette = kmeans.cluster_centers_
        labels = kmeans.labels_
    elif model == 'gmm':
        # Apply Gaussian Mixture Model clustering
        gmm = GaussianMixture(n_components=num_colors, random_state=0)
        gmm.fit(pixels)
        # Ger cluser centers as palette colors
        palette = gmm.means_
        labels = gmm.predict(pixels)

    # Count the number of pixels in each cluster
    cluster_counts = Counter(labels)

    # Get the indices of the clusters in descending order of their size
    sorted_cluster_indices = [item[0] for item in sorted(cluster_counts.items(), key=lambda x: x[1], reverse=True)]

    # Reorder the palette based on the sorted indices
    ordered_palette = [palette[i] for i in sorted_cluster_indices]

    # Convert the ordered palette to integers
    int_palette = [color.astype(int).tolist() for color in ordered_palette]

    if color_space == 'hsv':
        rgb_palette = [convert_hsv_to_rgb(color) for color in int_palette]
        return rgb_palette
    else:
        return int_palette

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extracts a dominant color palette from an image using K-Means clustering."
    )
    parser.add_argument(
        "image_path",
        help="Path to the input image file."
    )

    parser.add_argument(
        "-n", "--num_colors",
        type=int,
        default=5,
        help="Number of colors in the palette (default: 5)."
    )

    parser.add_argument(
        "-c", "--color_space",
        choices=['rgb','hsv'],
        default='rgb',
        help="Color space to use for clustering (default: rgb)."
    )

    parser.add_argument(
        "-m", "--model",
        choices=['kmeans','gmm'],
        default='kmeans',
        help="Model to use for clustering (default: kmeans)"
    )

    args = parser.parse_args()

    # Get the palette using RGB clustering
    palette = get_palette(args.image_path, args.num_colors, args.color_space, args.model)
    
    if palette:
        print(f"Dominant Colors (RGB)")
        for color in palette:
            print(f" - {tuple(color)}")
