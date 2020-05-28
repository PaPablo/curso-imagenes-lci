import math
import numpy as np
import imageio
from image_manip import (
    normalize,
    map_pixels,
    rgb_to_yiq,
    yiq_to_rgb,
    denormalize,
    apply_yiq_transformation
)
import matplotlib.pyplot as plt


def generate_luminance_histogram(image, fig_path, n_intervals=[10]):
    # Generate Y values for image

    def reduce(pixel):
        r, g, b = pixel
        return .299*r + .587*g + .114*b

    def get_y_values(image):
        """Return y values from an image

        Returns an array, where each value is the
        Y value for each pixel, where the Y value
        for the (i,j) pixel is in the position
        w*i + j with w equal to the width of the image
        """
        normalized_image = normalize(image)
        return map_pixels(function=reduce, image=normalized_image).flat

    def plot_histogram(image, values, n_intervals):

        fig, ax = \
            plt.subplots(nrows=1, ncols=len(n_intervals)+1, figsize=(30, 8))

        for index, interval in enumerate(n_intervals):
            heights, bins = np.histogram(values, bins=interval, range=(0, 1))
            percent = [(h/number_of_pixels)*100 for h in heights]
            i = index+1

            ax[i].bar(
                bins[:-1],
                percent,
                width=1/interval,
                align="edge",
                edgecolor="black"
            )

            ax[i].set_ylabel("Porcentaje de Píxeles (%)")
            ax[i].set_xlabel("Valor de luminancia")
            ax[i].set_ylim(0, 1)
            ax[i].set_xlim(0, 1)
            ax[i].set_yticks(np.arange(0, 110, step=10))
            ax[i].grid(axis='y')

        ax[0].imshow(image)
        plt.savefig(fig_path)

    y_values = get_y_values(image)
    number_of_pixels = len(y_values)

    plot_histogram(image, y_values, n_intervals)


def generate_luminance_histogram_from_path(image_path, n_intervals):
    generate_luminance_histogram(imageio.imread(image_path), n_intervals)


def apply_y_function_transformation(image, function=lambda pixel: pixel):
    """Applies a transformation to an image according to alpha and beta"""
    # Normalize the given image
    norm_img = normalize(image)

    # Convert to YIQ
    yiq_image = np.apply_along_axis(
        func1d=rgb_to_yiq,
        axis=2,
        arr=norm_img
    )

    # Apply transformation
    yiq_prime_image = np.apply_along_axis(
        func1d=function,
        axis=2,
        arr=yiq_image
    )

    # Deconvert to RGB
    rgb_prime_image = np.apply_along_axis(
        func1d=yiq_to_rgb,
        axis=2,
        arr=yiq_prime_image
    )

    # Return denormalized image
    return denormalize(rgb_prime_image)


# In[17]:


def apply_sqrt(pixel):
    y, i, q = pixel

    y = math.pow(y, 1/2)

    if y > 1:
        y = 1

    return [y, i, q]


def apply_square(pixel):
    y, i, q = pixel

    y = math.pow(y, 2)

    if y > 1:
        y = 1

    return [y, i, q]


def linear_function_from_two_points(p1, p2):
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
            return linear_function_from_two_points((lower, 0), (upper, 1))(y)

    return _apply


def apply_lineal_by_parts_to_pixel(lower, upper):
    def _apply(pixel):
        y, i, q = pixel
        return [apply_lineal_by_parts(lower, upper)(y), i, q]
    return _apply


def main():

    # Cargamos imagen
    img = imageio.imread('imageio:astronaut.png')
    # Guardamos el histograma
    generate_luminance_histogram(img, '01-imagen_normal_hist.png', [40])
    # Manipulamos
    img_manip = apply_yiq_transformation(img, alpha=.3, beta=.3)
    # Histograma
    generate_luminance_histogram(img_manip, '02-imagen_manip_hist.png', [40])
    # Multiplicamos
    mult_img = apply_y_function_transformation(img, lambda pixel: pixel*2)
    # Histograma
    generate_luminance_histogram(mult_img, '03-imagen_mult_hist.png', [40])
    # Sqrt
    sqrt_img = apply_y_function_transformation(img, function=apply_sqrt)
    # Histograma
    generate_luminance_histogram(sqrt_img, '04-sqrt-img.png', [40])
    # Square
    square_img = apply_y_function_transformation(img, function=apply_square)
    # Histograma
    generate_luminance_histogram(square_img, '05-square-img.png', [40])
    # By parts
    by_parts = apply_y_function_transformation(
        img, function=apply_lineal_by_parts_to_pixel(.3, .7))
    # Histograma
    generate_luminance_histogram(by_parts, '06-byparts-img.png', [40])


if __name__ == '__main__':
    main()
