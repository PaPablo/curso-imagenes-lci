import numpy as np

rgb_to_yiq_mat = np.array([
    [0.299 , 0.587 , 0.114],
    [0.595716 , -0.274453 , -0.321263],
    [0.211456 , -0.522591 , 0.311135]
    ])


yiq_to_rgb_mat = np.linalg.inv(rgb_to_yiq_mat)

def normalize(image):
    """normlize image"""
    return np.clip(image/255, 0,1)

def denormalize(normalized_image):
    """denormalized values from a normlized image"""

    denorm = (normalized_image*255).astype(int)
    return np.clip(denorm, 0, 255)

def apply_alpha_and_beta(alpha=1,  beta=1):
    """Applies alpha and beta values to a pixel

    Performs the operations needed for transformation.
    It also restricts the output values to those permited
    """
    def _apply(pixel):
        y_prime, i_prime, q_prime = pixel


        y_prime *= alpha

        # Check Y'
        if y_prime > 1:
            y_prime = 1

        i_prime *= beta
        q_prime *= beta
        # Check I'
        if i_prime > .5957:
            i_prime = .5957

        if i_prime < -.5957:
            i_prime = -.5957

        # Check Q'
        if q_prime >.5226:
            q_prime = .5226

        if q_prime < -.5226:
            q_prime = -.5226

        return [y_prime, i_prime, q_prime]

    return _apply

def map_pixels(function, image):
    return np.array([[function(pixel) for pixel in image_rows] for image_rows in image])

def rgb_to_yiq(image):
    norm = normalize(image)
    return (norm.reshape((-1, 3)) @ rgb_to_yiq_mat).reshape(image.shape)

def yiq_to_rgb(data):
    _norm_rgb = (data.reshape((-1,3)) @ yiq_to_rgb_mat).reshape(data.shape)
    return denormalize(_norm_rgb)

def apply_yiq_transformation(image, alpha=1, beta=1):
    """Applies a transformation to an image according to alpha and beta"""

    # Convert to YIQ
    yiq_image =  rgb_to_yiq(image)

    # Apply transformation
    yiq_prime_image = map_pixels(
            function=apply_alpha_and_beta(alpha, beta),
            image=yiq_image
            )

    # Return deconverted to RGB
    return yiq_to_rgb(yiq_prime_image)
