import math
import numpy as np
import logging

from image_manip import (
        transform_to_yiq,
        transform_to_rgb,
        normalize,
        denormalize,
        apply_yiq_transformation)

from scipy import ndimage
import imageio
import matplotlib.pyplot as plt

def generate_luminance_histogram(image, n_intervals=[10]):
    """Plot the luminance histogram for the given image  - Image should be normalized"""

    def plot_histogram(image, values, n_intervals):
        
        fig, ax = plt.subplots(nrows=1, ncols=len(n_intervals)+1, figsize=(30,8))
    
        for index, interval in enumerate(n_intervals):
            heights, bins = np.histogram(values, bins=interval, range=(0,1))
            percent = [(h/sum(heights)*100) for h in heights]
            i = index+1

            ax[i].bar(bins[:-1], percent,width=1/interval, align="edge", edgecolor="black")
            
            ax[i].set_ylabel("Porcentaje de Píxeles (%)")
            ax[i].set_xlabel("Valor de luminancia")
            ax[i].set_ylim(0,1)
            ax[i].set_xlim(0,1)
            ax[i].set_yticks(np.arange(0,110, step=10))
            ax[i].grid(axis='y')
        
        ax[0].imshow(image, cmap='gray')
        plt.show()

        
    plot_histogram(image, image, n_intervals)
    
def generate_luminance_histogram_from_path(image_path, n_intervals):
    generate_luminance_histogram(np.array(imageio.imread(image_path)), n_intervals)

def apply_y_function_transformation(image, function=lambda pixel: pixel):
    """Applies a transformation to an image according to alpha and beta"""
    # Normalize the given image
    norm_img = normalize(image)
    
    # Convert to YIQ
    yiq_image = np.apply_along_axis(
        func1d=transform_to_yiq,
        axis=2,
        arr=norm_img
    )
    
    # Apply transformation
    yiq_prime_image = np.apply_along_axis(
        func1d=function
        ,axis=2,
        arr=yiq_image
    )
    
    # Deconvert to RGB
    rgb_prime_image = np.apply_along_axis(
        func1d=transform_to_rgb,
        axis=2,
        arr=yiq_prime_image
    )
    
    # Return denormalized image
    return denormalize(rgb_prime_image)


def apply_sqrt(pixel):
    y, i,q = pixel
    
    y = math.sqrt(y)
    
    if y > 1:
        y=1
        
    return [y,i,q]

def apply_square(pixel):
    y, i,q = pixel
    
    y = math.pow(y, 2)
    
    if y > 1:
        y=1
        
    return [y,i,q]

def linear_function_from_two_points(p1, p2):
    logging.debug(p1, p2)
    x1, y1 = p1
    x2, y2 = p2
    
    m = (y2-y1) / (x2-x1)
    b = y1 - (m * x1)
    
    def f(x):
        return (m * x) + b
    return f
    
def apply_lineal_by_parts(lower, upper):
    
    positive = lower <= upper
    
    points = []
    if positive:
        points += [(lower, 0), (upper, 1)]
    else:
        points += [(lower, 1), (upper, 0)]
        
    def _apply(y):
        if positive and y > upper:
            return 1
        elif positive and y < lower:
            return 0
        elif not positive and y > upper:
            return 0
        elif not positive and y < lower:
            return 1
        else:
            return linear_function_from_two_points((lower, 0), (upper,1))(y)

    return _apply

def apply_lineal_by_parts_to_pixel(lower, upper):
    def _apply(pixel):
        y,i,q = pixel
        return [apply_lineal_by_parts(lower, upper)(y),i,q]
    return _apply



