import numpy as np
import imageio


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
    recons_transform = np.exp(mag) * (np.cos(phase) + 1j * np.sin(phase))

    im_rec = np.fft.ifft2(np.fft.ifftshift(recons_transform))\
        .astype(np.float64)

    # Interpolate values to obtain a real image with values
    # between 0 and 255
    img = np.interp(im_rec, (im_rec.min(), im_rec.max()), (0, 255))\
        .astype(np.uint8)

    return img


# Guardar Transformada de Fourier dado
# Magnitud, fase y filename
def ftwrite(mag, phase, fn):
    """Save a Fourier Transform, given a magnitude and a phase

    Arguments:
        mag (numpy.array): magnitude
        phase (numpy.array): phase
        fn (str): Path to save the transform to

    Returns
    None
    """
    # Acaso la magnitud y la fase requieren ser guardadas como un pkl
    pass


# Leer Transformada de Fourier
def ftread(fn):
    """Read Fourier Transform from a filename

    Arguments:
        fn (str): Path to the FT image

    Returns:
        Magnitude and phase of the Fourier Transform
        """
    pass


# Remuestreo (resmaple) en espacio fourier
# ftresample(im, new_shape).shape == new_shape
def ftresample(im, new_shape):
    # Qué es el resampling
    pass
