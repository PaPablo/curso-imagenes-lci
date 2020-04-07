import numpy as np

def normalize(image):
    """normlize image"""
    return np.clip(image/255, 0,1)

def denormalize(normalized_image):
    """denormalized values from a normlized image"""
    
    denorm = (normalized_image*255).astype(int)
    return np.clip(denorm, 0, 255)