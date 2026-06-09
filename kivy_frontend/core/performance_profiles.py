"""
Performance profile manager
"""

from core.models import PerformanceProfile
from sqlalchemy.orm.session import Session


class PerformanceProfileManager:
    """
    Manages performance profiles for different use cases
    """
    
    DEFAULT_PROFILES = [
        {
            'name': 'Battery Saver',
            'cpu_governor': 'powersave',
            'gpu_frequency': 300,
            'resolution_scale': 0.75,
            'shader_quality': 'low',
            'texture_cache_mb': 128,
            'frame_pacing': 30,
            'audio_latency_ms': 32,
            'vulkan_enabled': False,
        },
        {
            'name': 'Balanced',
            'cpu_governor': 'schedutil',
            'gpu_frequency': 600,
            'resolution_scale': 0.9,
            'shader_quality': 'medium',
            'texture_cache_mb': 256,
            'frame_pacing': 60,
            'audio_latency_ms': 16,
            'vulkan_enabled': True,
        },
        {
            'name': 'Performance',
            'cpu_governor': 'performance',
            'gpu_frequency': 850,
            'resolution_scale': 1.0,
            'shader_quality': 'high',
            'texture_cache_mb': 512,
            'frame_pacing': 120,
            'audio_latency_ms': 8,
            'vulkan_enabled': True,
        },
        {
            'name': 'Ultra Performance',
            'cpu_governor': 'performance',
            'gpu_frequency': 1000,
            'resolution_scale': 1.1,
            'shader_quality': 'ultra',
            'texture_cache_mb': 1024,
            'frame_pacing': 120,
            'audio_latency_ms': 4,
            'vulkan_enabled': True,
        },
    ]
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self._initialize_default_profiles()
    
    def _initialize_default_profiles(self):
        """
        Initialize default profiles if they don't exist
        """
        for profile_data in self.DEFAULT_PROFILES:
            existing = self.db_session.query(PerformanceProfile).filter_by(
                name=profile_data['name']
            ).first()
            
            if not existing:
                profile = PerformanceProfile(**profile_data)
                self.db_session.add(profile)
        
        self.db_session.commit()
    
    def get_profile(self, name: str) -> PerformanceProfile:
        """Get a profile by name"""
        return self.db_session.query(PerformanceProfile).filter_by(name=name).first()
    
    def get_all_profiles(self):
        """Get all profiles"""
        return self.db_session.query(PerformanceProfile).all()
