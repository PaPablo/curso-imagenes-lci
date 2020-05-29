import numpy as np
import imageio
from image_manip import rgb_to_yiq, yiq_to_rgb

import matplotlib.pyplot as plt

def rgb_clamp_addition(img1, img2):
    addition = img1.astype(int)+ img2.astype(int)
    return np.clip(addition, 0, 255)


def rgb_avg_addition(img1, img2):
    addition = (img1.astype(int)+ img2.astype(int))/2
    return np.clip(addition.astype(int), 0, 255)


def rgb_clamp_subtraction(img1, img2):
    addition = img1.astype(int)- img2.astype(int)
    return np.clip(addition, 0, 255)


def rgb_avg_subtraction(img1, img2):
    addition = (img1.astype(int)- img2.astype(int))/2
    return np.clip(addition.astype(int), 0, 255)


def yiq_clamp_add(img1, img2):
    # Convert to yiq
    img1_yiq = rgb_to_yiq(img1)
    img2_yiq = rgb_to_yiq(img2)

    def generate_new_yiq(p1, p2):
        y1, i1, q1 = p1
        y2, i2, q2 = p2

        # Suma clampeada
        y3 = np.clip(y1 + y2, 0,1)

        # Interpolación
        i3 = (y1 * i1 + y2 * i2)/(y1 + y2)
        q3 = (y1 * q1 + y2 * q2)/(y1 + y2)

        return [y3, i3, q3]

    img3_yiq = np.array([generate_new_yiq(p1,p2) for p1, p2 in zip(img1_yiq.reshape((-1, 3)), img2_yiq.reshape((-1, 3)))]).reshape(img1.shape)

    return yiq_to_rgb(img3_yiq)


def yiq_clamp_sub(img1, img2):
    # Convert to yiq
    img1_yiq = rgb_to_yiq(img1)
    img2_yiq = rgb_to_yiq(img2)

    def generate_new_yiq(p1, p2):
        y1, i1, q1 = p1
        y2, i2, q2 = p2

        # Suma clampeada
        y3 = np.clip(y1 - y2, 0,1)

        # Interpolación
        i3 = (y1 * i1 + y2 * i2)/(y1 + y2)
        q3 = (y1 * q1 + y2 * q2)/(y1 + y2)

        return [y3, i3, q3]

    img3_yiq = np.array([generate_new_yiq(p1,p2) for p1, p2 in zip(img1_yiq.reshape((-1, 3)), img2_yiq.reshape((-1, 3)))]).reshape(img1.shape)

    return yiq_to_rgb(img3_yiq)


def if_lighter(img1, img2):
    # Convert to yiq
    img1_yiq = rgb_to_yiq(img1)
    img2_yiq = rgb_to_yiq(img2)

    def generate_if_lighter(p1, p2):
        y1, _, _ = p1
        y2, _, _ = p2

        if y1 > y2:
            return p1
        else:
            return p2

    img3_yiq = np.array([generate_if_lighter(p1,p2) for p1, p2 in zip(img1_yiq.reshape((-1, 3)), img2_yiq.reshape((-1, 3)))]).reshape(img1.shape)

    return yiq_to_rgb(img3_yiq)


def if_darker(img1, img2):
    # Convert to yiq
    img1_yiq = rgb_to_yiq(img1)
    img2_yiq = rgb_to_yiq(img2)

    def generate_if_lighter(p1, p2):
        y1, _, _ = p1
        y2, _, _ = p2

        if y1 < y2:
            return p1
        else:
            return p2

    img3_yiq = np.array([generate_if_lighter(p1,p2) for p1, p2 in zip(img1_yiq.reshape((-1, 3)), img2_yiq.reshape((-1, 3)))]).reshape(img1.shape)

    return yiq_to_rgb(img3_yiq)

def main():
    astronaut = imageio.imread('imageio:astronaut.png')
    wikkie = imageio.imread('imageio:wikkie.png')

    plt.imshow(rgb_clamp_addition(astronaut, wikkie))
    plt.savefig('01-rgb-clamp-add.png')

    plt.imshow(rgb_avg_addition(astronaut, wikkie))
    plt.savefig('02-rgb-avg-add.png')

    plt.imshow(rgb_clamp_subtraction(astronaut, wikkie))
    plt.savefig('03-rgb-clamp-sub.png')

    plt.imshow(rgb_avg_subtraction(astronaut, wikkie))
    plt.savefig('04-rgb-avg-sub.png')

    plt.imshow(yiq_clamp_sub(astronaut, wikkie))
    plt.savefig('05-yiq-clamp-add.png')

    plt.imshow(rgb_clamp_addition(astronaut, wikkie))
    plt.savefig('06-yiq-clamp-sub.png')

    plt.imshow(if_lighter(astronaut, wikkie))
    plt.savefig('07-if-darker.png')

    plt.imshow(if_darker(astronaut, wikkie))
    plt.savefig('08-if-lighter.png')


if __name__ == '__main__':
    main()
