!pip install -q "pydicom>=2.4" "pylibjpeg>=2.0" "pylibjpeg-libjpeg>=2.1" "pylibjpeg-openjpeg"


from google.colab import drive
drive.mount('/content/drive')


import os
import math
import numpy as np
import pydicom
from pydicom.pixel_data_handlers.util import apply_voi_lut
import matplotlib.pyplot as plt

def display_dicom_slices(series_dir, num_images=4):
    """
    Function to read and display a specified number of DICOM files from a folder.

    Inputs:
    - series_dir: Path to the folder containing DICOM files (str)
    - num_images: Maximum number of images to display (int, default is 4)

    Output: Displays a grid of images with titles as file names without .dcm
    """
    # Read DICOM files and store in slices list along with file names
    slices = []
    file_names = []
    for root, _, files in os.walk(series_dir):
        for fn in files:
            if fn.lower().endswith(".dcm"):
                ds = pydicom.dcmread(os.path.join(root, fn), force=True)
                slices.append(ds)
                file_names.append(os.path.splitext(fn)[0])  # Remove .dcm extension

    # Check if any files were found
    if len(slices) == 0:
        print("No DICOM files found.")
        return

    # Set the number of images to display (up to num_images)
    num_to_display = min(len(slices), num_images)

    # Set up grid for display
    rows = math.ceil(math.sqrt(num_to_display))
    cols = math.ceil(num_to_display / rows)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))

    # Flatten axes array for easier iteration
    axes = np.array(axes).flatten()

    # Process and display each image
    for i in range(num_to_display):
        ds = slices[i]
        try:
            img = apply_voi_lut(ds.pixel_array, ds)  # Apply Window/Level adjustment
            if ds.get("PhotometricInterpretation") == "MONOCHROME1":
                img = img.max() - img  # Invert for MONOCHROME1

            axes[i].imshow(img, cmap='gray')
            axes[i].axis('off')  # Hide axes
            axes[i].set_title(file_names[i], fontsize=8)  # Display file name without .dcm
        except Exception as e:
            print(f"Error processing slice {file_names[i]}: {e}")
            axes[i].axis('off')
            continue

    # Disable extra axes if fewer images than grid slots
    for i in range(num_to_display, len(axes)):
        axes[i].axis('off')

    plt.tight_layout()  # Adjust spacing between images
    plt.show()
    
########Test

series_dir = "/content/drive/MyDrive/medical/data/project/Abdomal_aurt/KIYANIYAN^MOHAMAD/CT/Series 0-"
display_dicom_slices(series_dir, num_images=4)