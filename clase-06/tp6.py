import imageio
import numpy as np


def extend_image(image, x=0, y=0):
    """Extend the image in x and x pixels"""
    return np.pad(image, (x, y), mode='edge')


def apply_operation_pixel(image, se, row, col, operation):

    window_w, window_h = se.shape

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

    return operation(se, crop_image)


def apply_operation(im, se, operation):
    image = np.copy(im)
    window_w, window_h = se.shape

    x_off = window_w // 2
    y_off = window_h // 2

    img_h, img_w = image.shape

    resized_image = extend_image(image, x_off, y_off)

    out_img = image[:, :]

    for row in range(img_h):
        for col in range(img_w):

            out_pixel = apply_operation_pixel(
                resized_image,
                se,
                row+x_off,
                col+y_off,
                operation)
            out_img[row, col] = out_pixel

    return out_img.clip(0, 1)


def save_image(name, image):
    out = (image * 255).astype(np.uint8)

    imageio.imwrite(name, out)


def erode(se, crop_image):
    return crop_image[se].min()


def dilate(se, crop_image):
    return crop_image[se].max()


def median(se, crop_image):
    elements = crop_image[se].flatten()
    middle = len(elements) // 2 + 1
    return sorted(elements)[middle]


def invert(image):
    return (image * (-1))+1


def binarize(image, threshold=.5):
    copy = np.copy(image)

    copy[image >= threshold] = 1
    copy[image < threshold] = 0

    return copy


def opening(image, se):
    """Apertura de la imagen
        erosion -> dilatacion
    """

    erosion = apply_operation(
        image,
        se,
        erode
    )

    return apply_operation(
        erosion,
        se,
        dilate
    )


def closing(image, se):
    """Cierre de la imagen
        dilatacion -> erosion
    """

    dilation = apply_operation(
        image,
        se,
        dilate
    )

    return apply_operation(
        dilation,
        se,
        erode
    )


def border(image, se, inner=True):
    """Borde interior o exterior
        interior: original - erosion
        exterior: dilatacion - original
    """
    if inner:
        erosion = apply_operation(image, se, erode)
        return np.clip(image - erosion, 0, 1)
    else:
        dilation = apply_operation(image, se, dilate)
        return np.clip(dilation-image, 0, 1)


def tophat(image, se):
    """Tophat
        imagen - apertura
    """
    opened = opening(image, se)

    return np.clip(image - opened, 0, 1)


def bottomhat(image, se):
    pass


def box(r):
    return np.ones((r*2+1, r*2+1), dtype=np.bool)


def circle(r):
    vec = np.linspace(0, r*2, r*2+1)-r
    [x, y] = np.meshgrid(vec, vec)
    dist = (x**2+y**2)**0.5
    se = box(r)
    se[dist > (r+0.3)] = False
    return se


def main():
    # text = imageio.imread('imageio:page.png') / 255

    # text = invert(text)

    # level_0 = [dilate, erode, median]
    # level_1 = [opening, closing, tophat]

    # for op in level_0:
    # manip = apply_operation(
    # text,
    # op
    # )

    # save_image(f'{op.__name__}.png', manip)

    # for op in level_1:
    # manip = op(text)
    # save_image(f'{op.__name__}.png', manip)

    particles = imageio.imread('particles_in.png')/255

    particles_out = opening(particles, circle(4))

    iris = imageio.imread('./iris.bmp') / 255

    iris_out = tophat(iris, circle(5))

    save_image('iris_out.png', iris_out)

    save_image('particles_out.png', particles_out)


if __name__ == "__main__":
    main()
