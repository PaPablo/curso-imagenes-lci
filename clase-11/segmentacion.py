import matplotlib.pyplot as plt
import numpy as np
import imageio

from queue import Queue
from borders import border, circle
from filters import apply_kernel, get_laplace_kernel


def binarize(image, threshold=.5):
    copy = np.copy(image)

    copy[image >= threshold] = 1
    copy[image < threshold] = 0

    return copy


def binarize_mode(img):

    # ## Encontrar dos modas “clara” y “oscura” y binarizar por distancia mínima.

    hist, bin_edges = np.histogram(img, bins=50)

    # Bit rudimentary, but kinda works
    (_, dark_mode), (_, bright_mode) = sorted([(n, bin_edge) for n, bin_edge in zip(
        hist, bin_edges)], key=lambda x: x[0], reverse=True)[:2]

    mid_point = abs(dark_mode-bright_mode)/2

    return binarize(img, threshold=mid_point)


# Otsu https://en.wikipedia.org/wiki/Otsu%27s_method
def otsu(image, bins=256):

    otsus = []
    # minimizar F.var(F) + B.var(B)
    for t in range(bins):
        threshold = t/255
        foreground = image[image >= threshold]
        background = image[image < threshold]
        if len(foreground) == 0 or len(background) == 0:
            continue
        varF = np.var(foreground)
        varB = np.var(background)
        value = np.sum(foreground) * varF + np.sum(background) * varB

        otsus.append((threshold,  value))

    return min(otsus, key=lambda x: x[1])[0]


# ### Marching Squares


def get_marching_segmentation(case):
    if case == 0:
        return np.array([[0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0]])
    elif case == 1:
        return np.array([[0, 0, 0],
                         [1, 0, 0],
                         [0, 1, 0]])
    elif case == 2:
        return np.array([[0, 0, 0],
                         [0, 0, 1],
                         [0, 1, 0]])
    elif case == 3:
        return np.array([[0, 0, 0],
                         [1, 1, 1],
                         [0, 0, 0]])
    elif case == 4:
        return np.array([[0, 1, 0],
                         [0, 0, 1],
                         [0, 0, 0]])
    elif case == 5:
        return np.array([[0, 1, 0],
                         [1, 0, 1],
                         [0, 1, 0]])
    elif case == 6:
        return np.array([[0, 1, 0],
                         [0, 1, 0],
                         [0, 1, 0]])
    elif case == 7:
        return np.array([[0, 1, 0],
                         [1, 0, 0],
                         [0, 0, 0]])
    elif case == 8:
        return np.array([[0, 1, 0],
                         [1, 0, 0],
                         [0, 0, 0]])
    elif case == 9:
        return np.array([[0, 1, 0],
                         [0, 1, 0],
                         [0, 1, 0]])
    elif case == 10:
        return np.array([[0, 1, 0],
                         [1, 0, 1],
                         [0, 1, 0]])
    elif case == 11:
        return np.array([[0, 1, 0],
                         [0, 0, 1],
                         [0, 0, 0]])
    elif case == 12:
        return np.array([[0, 0, 0],
                         [1, 1, 1],
                         [0, 0, 0]])
    elif case == 13:
        return np.array([[0, 0, 0],
                         [0, 0, 1],
                         [0, 1, 0]])
    elif case == 14:
        return np.array([[0, 0, 0],
                         [1, 0, 0],
                         [0, 1, 0]])
    elif case == 15:
        return np.array([[0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0]])


def marching_case(portion):
    [[a, b, d, c]] = portion.reshape((1, 4))

    return d + c*2 + b*4 + a*8


def marchig_square_cases(img):
    h, w = img.shape

    cases = []
    for y in range(h-1):
        row = []
        for x in range(w-1):
            row.append(marching_case(img[y:y+2, x:x+2]))
        cases.append(row)

    return np.array(cases).astype(np.uint8)


def marching_square_contour(cases):

    return np.vstack(
        [
            np.hstack([get_marching_segmentation(col) for col in row])
            for row in cases]
    )


def marching_squares(img, threshold=.5, order=0):
    binarized_img = binarize(img, threshold)

    cases = marchig_square_cases(binarized_img)

    return marching_square_contour(cases)


def get_neighbors(img_shape, pos):
    y, x = pos

    h, w = img_shape

    north = (y+1, x)
    south = (y-1, x)
    west = (y, x-1)
    east = (y, x+1)

    return sorted(filter(lambda point:
                         point[0] >= 0 and point[0] < h and
                         point[1] >= 0 and point[1] < w,
                         [north, south, east, west]))


def color_fill(img, pos, target_color):

    img = np.copy(img)

    color = img[pos]
    print(color)

    # Seen pixels
    seen = np.zeros(img.shape)

    queue = Queue()

    queue.put(pos)

    while not queue.empty():
        pos = queue.get_nowait()

        img[pos] = target_color

        neighbors = get_neighbors(img.shape, pos)

        for n in neighbors:
            if seen[n] == 0 and img[n] == color:
                seen[n] = 1
                queue.put(n)

    return img


def main():
    img_a = (imageio.imread('data/img_a.png') / 255)[:, :, 0]
    img_b = (imageio.imread('data/img_b.png') / 255)[:, :, 0]

    # Binarización

    # Umbral en .6
    binarizacion_a_06 = binarize(img_a, threshold=.6)
    imageio.imsave('binarizacion_a_06.png', binarizacion_a_06)

    # Umbral en .4
    binarizacion_a_04 = binarize(img_a, threshold=.4)
    imageio.imsave('binarizacion_a_04.png', binarizacion_a_04)

    # Por modas
    binarizarion_por_moda = binarize_mode(img_b)
    imageio.imsave('binarizarion_por_moda.png', binarizarion_por_moda)

    # Otsu
    binarizarion_otzu = binarize(img_a, threshold=otsu(img_b))
    imageio.imsave('binarizarion_otzu.png', binarizarion_otzu)

    # Laplaciano
    laplace_img = apply_kernel(img_a, get_laplace_kernel(8))
    imageio.imsave('laplace_img.png', laplace_img)

    # Borde morfológico
    morph_border_img = border(img_a, circle(1))
    imageio.imsave('morph_border_img.png', morph_border_img)

    marching_squares_img_a = marching_squares(img_a)
    imageio.imsave('marching_squares_img_a.png', marching_squares_img_a)

    magic_wand = color_fill(img_b, (1, 1), .3)
    imageio.imsave('magic_wand.png', magic_wand)


if __name__ == "__main__":
    main()
