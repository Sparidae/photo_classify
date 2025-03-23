"""
Core functionality for photo classification
"""

from .vision_api import query_vision_model
from .image_utils import convert_image_to_webp_base64

__all__ = ['query_vision_model', 'convert_image_to_webp_base64'] 