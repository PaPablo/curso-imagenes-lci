"""
Implementar:
    1. Kernel Promedio - En estos casos el cierre no se hace, poner en negro:
        a. 3x3
        b. 5x5
        c. 7x7
        2. Kernel pasabajos y pasaaltos:
            a. Pasabajos
            - Bartlett 3x3
            - Bartlett 5x5
            - Bartlett 7x7
            - Gaussiano 5x5
            - Gaussiano 7x7
            b. Detectores de bordes:
                - Laplaciano v4
                - Laplaciano v8
                - Sobel N
                - Sobel E
                - Sobel S
                - Sobel O
                """
import imageio
import ipdb
import numpy as np


def extend_image(image, x=0, y=0):
    """Extend the image in x and x pixels"""
    return np.pad(image, (x, y), mode='edge')


def apply_kernel_pixel(image, row, col, kernel):

    kernel_w, kernel_h = kernel.shape

    x_off = kernel_w // 2
    y_off = kernel_w // 2

    x_start = row-x_off
    y_start = col-y_off
    x_end = row+x_off+1
    y_end = col+y_off+1

    crop_image = image[
        x_start: x_end,  # The +1 is because of how python slices
        y_start: y_end  # arrays
    ]

    result = 0

    for x, kernel_row in enumerate(kernel):
        for y, value in enumerate(kernel_row):
            result += crop_image[x, y]*value

    return result


def apply_kernel(image, kernel, shape=None):

    kernel_w, kernel_h = kernel.shape

    x_off = kernel_w // 2
    y_off = kernel_w // 2

    if shape is None:
        img_w, img_h = image.shape
    else:
        img_w, img_h = shape

    resized_image = extend_image(image, x_off, y_off)

    out_img = image[:, :]

    for row in range(img_h):
        for col in range(img_w):
            out_pixel = apply_kernel_pixel(
                resized_image,
                row+x_off,
                col+y_off,
                kernel)
            out_img[row, col] = out_pixel

    return out_img


def conv_avg(image, width=3, height=3):

    kernel = np.ones((width, height))
    kernel /= sum(kernel)

    out_img = apply_kernel(image, kernel)

    return out_img


def generate_bartlett_vector(length):
    half = length // 2

    head = np.arange(1, half+1)

    result = head
    result = np.append(result, [half+1])
    result = np.append(result, head[::-1])

    return result.flatten()


def conv_bartlett(image, length=3):

    vector = generate_bartlett_vector(length)

    kernel = np.outer(vector, vector)

    kernel = kernel/np.sum(kernel)

    out = apply_kernel(image, kernel, image.shape)

    return out


def pascal_row(length=1):
    if length == 1:
        return [1]
    else:
        previous_row = pascal_row(length-1)
        row = []
        row.append(previous_row[0])
        for i in range(len(previous_row) - 1):
            row.append(previous_row[i] + previous_row[i+1])
        row.append(previous_row[-1])
        return row


def conv_gaussian(image, length=5):
    vector = pascal_row(length)

    kernel = np.outer(vector, vector)

    kernel = kernel/np.sum(kernel)

    out = apply_kernel(image, kernel, image.shape)

    return out

def save_image(name, image):
    out = (image * 255).astype(np.uint8)

    imageio.imwrite(name, out)


def main():
    # For use with the other filters
    camera = imageio.imread('imageio:camera.png')/255

    imageio.imwrite('camera.png', (camera*255).astype(np.uint8))
    # For the sobel filters
    page = imageio.imread('imageio:page.png')/255
    imageio.imwrite('page.png', (page*255).astype(np.uint8))

    # Promedio 3x3
    # c_avg_3_3 = (conv_avg(camera, 3, 3) * 255).astype(np.uint8)
    # imageio.imwrite('c_avg_3_3.png', c_avg_3_3)
    # Promedio 5x5
    # c_avg_5_5 = (conv_avg(camera, 5, 5) * 255).astype(np.uint8)
    # imageio.imwrite('c_avg_5_5.png', c_avg_5_5)
    # Promedio 7x7
    # c_avg_7_7 = (conv_avg(camera, 7, 7) * 255).astype(np.uint8)
    # imageio.imwrite('c_avg_7_7.png', c_avg_7_7)
    # Bartlett 3x3
    # bartlett_3_3 = conv_bartlett(camera, 3)
    # save_image('bartlett_3_3.png', bartlett_3_3)
    # Bartlett 5x5
    # bartlett_5_5 = conv_bartlett(camera, 5)
    # save_image('bartlett_5_5.png', bartlett_5_5)
    # Bartlett 7x7
    # bartlett_7_7 = conv_bartlett(camera, 7)
    # save_image('bartlett_7_7.png', bartlett_7_7)
    # Gaussiano 5x5
    gaussian_5_5 = conv_gaussian(camera, 5)
    save_image('gaussian_5_5.png', gaussian_5_5)
    # Gaussiano 7x7
    gaussian_7_7 = conv_gaussian(camera, 7)
    save_image('gaussian_7_7.png', gaussian_7_7)
    # Laplaciano v4
    # Laplaciano v8
    # Sobel N
    # Sobel E
    # Sobel S
    # Sobel O


if __name__ == "__main__":
    main()
