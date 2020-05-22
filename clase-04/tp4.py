import numpy as np
import imageio
import matplotlib.pyplot as plt

# Computar magnitud y fase
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
    phase = angle(fshift)

    return magnitude, phase

def ift_mag_phase(mag,phase):
    """Reconstruct image from magnitude and phase

    Arguments:
        mag (numpy.array): Magnitude
        phase (numpy.array): Phase

    Returns:
        Reconstructed image from `magnitude` and `phase`

    """

    # Reconstrucción del espectro a partir
    # de magnitud y fase
    recons_transform = np.exp(magnitude) * (np.cos(phase) + 1j * np.sin(phase))

    # Aplicar inversa a la transformada
    # obtenida
    im_rec = np.fft.ifft2(np.fft.ifftshift(recons)).astype(np.float64)

    # Interpolar a valores que acepte una imagen
    # de 0 a 255
    img = np.interp(im_rec, (im_rec.min(), im_rec.max()), (0, 255)).astype(np.uint8)

    return img

# Guardar Transformada de Fourier dado 
# Magnitud, fase y filename
def ftwrite(mag, phase, fn):
    pass

# Leer Transformada de Fourier
def ftread(fn):
    pass

# Remuestreo (resmaple) en espacio fourier
# ftresample(im, new_shape).shape == new_shape
def ftresample(im,new_shape)
    pass
