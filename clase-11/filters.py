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


avg_3_3_kernel = np.ones((3, 3))/9
avg_5_5_kernel = np.ones((5, 5))/25
avg_7_7_kernel = np.ones((7, 7))/49


def generate_bartlett_vector(length):
    half = length // 2

    head = np.arange(1, half+1)

    result = head
    result = np.append(result, [half+1])
    result = np.append(result, head[::-1])

    return result.flatten()


def get_bartlett_kernel(length=3):

    vector = generate_bartlett_vector(length)

    kernel = np.outer(vector, vector)

    kernel = kernel/np.sum(kernel)

    return kernel


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


def get_gaussian_kernel(length=5):
    vector = pascal_row(length)

    kernel = np.outer(vector, vector)

    kernel = kernel/np.sum(kernel)

    return kernel


def get_laplace_kernel(neighbors=4):
    if neighbors == 4:
        return np.array([
            [0, -1, 0],
            [-1, 4, -1],
            [0, -1, 0],
        ])
    else:
        return np.array([
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1],
        ])


def get_sobel_kernel(orientation='s'):
    k = np.array([
        [+1, +2, +1],
        [0, 0, 0],
        [-1, -2, -1],
    ])
    if orientation == 's':
        return k
    elif orientation == 'w':
        return np.rot90(k, k=3)
    elif orientation == 'n':
        return np.rot90(k, k=2)
    elif orientation == 'e':
        return np.rot90(k)


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

    try:

        for x, kernel_row in enumerate(kernel):
            for y, value in enumerate(kernel_row):
                result += crop_image[x, y]*value
    except:
        # ipdb.set_trace()
        pass

    return result


def apply_kernel(im, kernel, shape=None):

    image = np.copy(im)
    kernel_w, kernel_h = kernel.shape

    x_off = kernel_w // 2
    y_off = kernel_w // 2

    if shape is None:
        img_h, img_w = image.shape
    else:
        img_h, img_w = shape

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

    return out_img.clip(0, 1)


def conv_avg(image, width=3, height=3):

    kernel = np.ones((width, height))
    kernel /= sum(kernel)

    out_img = apply_kernel(image, kernel)

    return out_img


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

    laplace_percent = .5

    # Promedio 3x3
    print("Avg 3x3")
    c_avg_3_3 = apply_kernel(
        camera,
        avg_3_3_kernel
    )
    save_image('c_avg_3_3.png', c_avg_3_3)
    # Promedio 5x5
    print("Avg 5x5")
    c_avg_5_5 = apply_kernel(
        camera,
        avg_5_5_kernel
    )
    save_image('c_avg_5_5.png', c_avg_5_5)
    # Promedio 7x7
    print("Avg 7x7")
    c_avg_7_7 = apply_kernel(
        camera,
        avg_7_7_kernel
    )
    save_image('c_avg_7_7.png', c_avg_7_7)
    # Bartlett 3x3
    print("Bartlett 3x3")
    bartlett_3_3 = apply_kernel(
        camera,
        get_bartlett_kernel(3)
    )
    save_image('bartlett_3_3.png', bartlett_3_3)
    # Bartlett 5x5
    print("Bartlett 5x5")
    bartlett_5_5 = apply_kernel(
        camera,
        get_bartlett_kernel(5)
    )
    save_image('bartlett_5_5.png', bartlett_5_5)
    # Bartlett 7x7
    print("Bartlett 7x7")
    bartlett_7_7 = apply_kernel(
        camera,
        get_bartlett_kernel(7)
    )
    save_image('bartlett_7_7.png', bartlett_7_7)
    # Gaussiano 5x5
    print("Gaussian 5x5")
    gaussian_5_5 = apply_kernel(
        camera,
        get_gaussian_kernel(length=5),
        camera.shape)
    save_image('gaussian_5_5.png', gaussian_5_5)
    # Gaussiano 7x7
    print("Gaussian 7x7")
    gaussian_7_7 = apply_kernel(
        camera,
        get_gaussian_kernel(length=7),
        camera.shape)
    save_image('gaussian_7_7.png', gaussian_7_7)
    # Laplaciano v4
    print(f"laplace v4 {laplace_percent}")
    laplace_v4 = apply_kernel(
        camera,
        get_laplace_kernel(4)
    )
    save_image(
        'laplace_v4.png',
        (camera + (laplace_v4*laplace_percent)).clip(0, 1)
    )
    # Laplaciano v8
    print(f"laplace v8 {laplace_percent}")
    laplace_v8 = apply_kernel(
        camera,
        get_laplace_kernel(8)
    )
    save_image(
        'laplace_v8.png',
        (camera+(laplace_v8*laplace_percent)).clip(0, 1)
    )
    # Sobel N
    print('sobel N')
    sobel_n = apply_kernel(
        page,
        get_sobel_kernel(orientation='n')
    )
    save_image('sobel_n.png', sobel_n)
    # Sobel E
    print('sobel E')
    sobel_e = apply_kernel(
        page,
        get_sobel_kernel(orientation='e')
    )
    save_image('sobel_e.png', sobel_e)
    # Sobel S
    print('sobel S')
    sobel_s = apply_kernel(
        page,
        get_sobel_kernel(orientation='s')
    )
    save_image('sobel_s.png', sobel_s)
    # Sobel W
    print('sobel W')
    sobel_w = apply_kernel(
        page,
        get_sobel_kernel(orientation='w')
    )
    save_image('sobel_w.png', sobel_w)


if __name__ == "__main__":
    main()
