import numpy as np

rgb_to_yiq = np.array([
    [0.299 , 0.587 , 0.114],
    [0.595716 , -0.274453 , -0.321263],
    [0.211456 , -0.522591 , 0.311135]
])


yiq_to_rgb = np.array([
    [1, .9663, .6210],
    [1, -.2721, -.6474],
    [1, -1.1070, 1.7046]
])

def normalize(image):
    """normlize image"""
    return np.clip(image/255, 0,1)

def denormalize(normalized_image):
    """denormalized values from a normlized image"""
    
    denorm = (normalized_image*255).astype(int)
    return np.clip(denorm, 0, 255)


def transform_to_yiq(pixel):
    """Transform from RGB representation to YIQ representation"""
    return np.matmul(rgb_to_yiq, pixel)

def transform_to_rgb(pixel):
    """Transform from YIQ representation to RGB representation"""
    return np.matmul(yiq_to_rgb, pixel)

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

def apply_yiq_transformation(image, alpha=1, beta=1):
    """Applies a transformation to an image according to alpha and beta"""
    

    
    def normalize(image):
        return image/255
    
    def denormalize(normalized_image):
        denorm = (normalized_image*255).astype(int)
        # Clip limita los valores
        return np.clip(denorm, 0, 255)
    
    # Normalize the given image
    norm_img = normalize(image)
    
   
    # Convert to YIQ
    yiq_image = np.apply_along_axis(
        func1d=transform_to_yiq,
        axis=2,
        arr=norm_img
    )
    
    # Apply transformation
    yiq_prime_image = np.apply_along_axis(
        func1d=apply_alpha_and_beta(alpha, beta)
        ,axis=2,
        arr=yiq_image
    )
    
    # Deconvert to RGB
    rgb_prime_image = np.apply_along_axis(
        func1d=transform_to_rgb,
        axis=2,
        arr=yiq_prime_image
    )
    
    # Return denormalized image
    return denormalize(rgb_prime_image)