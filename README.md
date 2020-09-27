# Adaptive Otsu thresholding

Python implementation of an adaptive variation of the standard Otsu thresholding method.
In this variation for each pixel of the input image a different threshold value is chosen regarding the neighbourhood (window) around that pixel.

To run the code type: python3 adaptive_otsu.py <input_image_path> <output_image_path> <window_size>

For the example run "python3 adaptive_otsu.py input_image.png output_image.png 30" , the following image transformation is performed.

# Input image
![Image of Yaktocat]https://github.com/Daphne-Skiado/Adaptive-Otsu/blob/master/input_image.png)

# Output image
![Image of Yaktocat]https://github.com/Daphne-Skiado/Adaptive-Otsu/blob/master/output_image.png)
