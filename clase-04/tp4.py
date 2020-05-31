import numpy as np
import imageio
import pickle


FN = 'imageio:camera.png'
NAME = 'camera'
MAG_FILE_NAME = f'{NAME}_mag.bmp'
PHASE_FILE_NAME = f'{NAME}_phase.pkl'


def ft_mag_phase(im):
    """Compute magnitude and phase from an image

    Arguments:
        im (numpy.array): Image

    Returns:
        Magnitude and phase of `im`
        """

    # Obtain transform
    transform = np.fft.fft2(im)

    # shift to center
    fshift = np.fft.fftshift(transform)

    # Obtain magnitud
    magnitude = np.log(np.abs(fshift))

    # Calculate phase
    phase = np.angle(fshift)

    return magnitude, phase


def ift_mag_phase(mag, phase):
    """Reconstruct image from magnitude and phase

    Arguments:
        mag (numpy.array): Magnitude
        phase (numpy.array): Phase

    Returns:
        Reconstructed image from `magnitude` and `phase`
        """

    # Reconstruct the spectrum from the magnitud and phase
    # The exp is used to conterreact the log used before
    recons_shift = np.exp(mag) * (np.cos(phase) + (1j * np.sin(phase)))
    im_rec = np.real(np.fft.ifft2(np.fft.ifftshift(recons_shift)))

    # Interpolate values to obtain a real image with values
    # between 0 and 255
    im = np.interp(im_rec, (im_rec.min(), im_rec.max()), (0, 255))\
        .astype(np.uint8)

    return im


# Guardar Transformada de Fourier dado
# Magnitud, fase y filename
def ftwrite(mag, phase, name):
    """Save a Fourier Transform, given a magnitude and a phase

    Arguments:
        mag (numpy.array): magnitude
        phase (numpy.array): phase
        fn (str): Path to save the transform to

    Returns
        The file names for the save magnitude and phase
    """

    mag_to_write = np.abs(mag)/np.max(mag)

    # Save magnitude
    imageio.imwrite(MAG_FILE_NAME, mag_to_write)

    # Save phase
    pickle.dump(phase, open(PHASE_FILE_NAME, 'wb'))

    return MAG_FILE_NAME, PHASE_FILE_NAME


# Leer Transformada de Fourier
def ftread(name):
    """Read Fourier Transform from a filename.
    Given a name `name` the program will try to read the files:
        - '{name}_mag.png'
        - '{name}_phase.png'

    Arguments:
        name (str): Path to the FT image

    Returns:
        Magnitude and phase of the Fourier Transform
        """

    phase = pickle.load(open(PHASE_FILE_NAME, 'rb'))

    # Return value in [0,1]
    mag = imageio.imread(MAG_FILE_NAME)/255

    return mag, phase


# Remuestreo (resmaple) en espacio fourier
# ftresample(im, new_shape).shape == new_shape
def ftresample(im, new_shape):
    # Qué es el resampling
    pass


def main():
    im = imageio.imread(FN)

    mag, phase = ft_mag_phase(im)

    ftwrite(mag, phase, NAME)

    rmag, rphase = ftread(NAME)

    rim = ift_mag_phase(rmag, rphase)

    imageio.imwrite('m_image.png', rim)


if __name__ == '__main__':
    main()
