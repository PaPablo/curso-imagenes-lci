import numpy as np
import imageio

def main():
    # Cargamos imagen
    astronaut = imageio.imread('imageio:astronaut.png')

    # Flip image
    imageio.imwrite('flip_ud_astronaut.png', np.flipud(astronaut))
    imageio.imwrite('flip_lr_astronaut.png', np.fliplr(astronaut))

    # Crop image
    alt_astronaut = astronaut[200:300, 200:300]
    imageio.imwrite('alt_astronaut.png', alt_astronaut)


print(__name__)
if __name__ == "__main__":
    print('hola')
    main()
