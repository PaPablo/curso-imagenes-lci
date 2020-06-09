import imageio
import numpy as np


def extend_image(image, x=0, y=0):
    """Extend the image in x and x pixels"""
    return np.pad(image, (x, y), mode='edge')


def apply_operation_pixel(image, row, col, operation=lambda crop: 0):

    window_w, window_h = (3, 3)

    x_off = window_w // 2
    y_off = window_h // 2

    x_start = row-x_off
    y_start = col-y_off
    x_end = row+x_off+1
    y_end = col+y_off+1

    crop_image = image[
        x_start: x_end,  # The +1 is because of how python slices
        y_start: y_end  # arrays
    ]

    return operation(crop_image)


def apply_operation(im, operation=lambda crop: 0):
    image = np.copy(im)
    window_w, window_h = (3, 3)

    x_off = window_w // 2
    y_off = window_h // 2

    img_h, img_w = image.shape

    resized_image = extend_image(image, x_off, y_off)

    out_img = image[:, :]

    for row in range(img_h):
        for col in range(img_w):

            out_pixel = apply_operation_pixel(
                resized_image,
                row+x_off,
                col+y_off,
                operation)
            out_img[row, col] = out_pixel

    return out_img.clip(0, 1)


def save_image(name, image):
    out = (image * 255).astype(np.uint8)

    imageio.imwrite(name, out)


def erode(crop_image):
    return crop_image.min()


def dilate(crop_image):
    return crop_image.max()


def median(crop_image):
    w, h = crop_image.shape
    middle = ((w*h)//2) + 1
    return sorted(crop_image.flatten())[middle]


def invert(image):
    return (image * (-1))+1


def binarize(image, threshold=.5):
    copy = np.copy(image)

    copy[image >= threshold] = 1
    copy[image < threshold] = 0

    return copy

def main():
    text = imageio.imread('imageio:page.png') / 255
    text = invert(text)


    e_text = apply_operation(
        text,
        median
    )

    save_image('h.png', e_text)


if __name__ == "__main__":
    main()
