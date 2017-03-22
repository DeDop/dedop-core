"""
Basic data models for representing the altimeter L1A, L1B, and L1B-S products in memory.
"""
from .surface_data import SurfaceData, SurfaceType
from .l1a_processing_data import L1AProcessingData, PacketPid
from .processor import BaseProcessor

__author__ = 'DeDop Development Team'

__all__ = [
    'BaseProcessor',
    'L1AProcessingData',
    'PacketPid',
    'SurfaceData',
    'SurfaceType'
]

