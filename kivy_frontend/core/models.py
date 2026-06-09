"""
Database models for Pixel Edition
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class TensorDeviceInfo(Base):
    """
    Tensor device information
    """
    __tablename__ = 'tensor_device_info'
    
    id = Column(Integer, primary_key=True)
    device_name = Column(String(255))
    tensor_generation = Column(String(50))  # G2, G3, G4
    ram_gb = Column(Integer)
    refresh_rate = Column(Integer)  # Hz
    vulkan_support = Column(Boolean, default=True)
    vulkan_version = Column(String(10))
    android_version = Column(Integer)
    detected_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'device_name': self.device_name,
            'tensor_generation': self.tensor_generation,
            'ram_gb': self.ram_gb,
            'refresh_rate': self.refresh_rate,
            'vulkan_support': self.vulkan_support,
        }


class PerformanceProfile(Base):
    """
    Performance profile configuration
    """
    __tablename__ = 'performance_profiles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    cpu_governor = Column(String(50))
    gpu_frequency = Column(Integer)
    resolution_scale = Column(Float)
    shader_quality = Column(String(50))
    texture_cache_mb = Column(Integer)
    frame_pacing = Column(Integer)
    audio_latency_ms = Column(Integer)
    vulkan_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class CoreConfiguration(Base):
    """
    Emulator core configuration
    """
    __tablename__ = 'core_configurations'
    
    id = Column(Integer, primary_key=True)
    core_name = Column(String(100), unique=True)
    core_version = Column(String(50))
    graphics_backend = Column(String(50))
    recommended_profile = Column(String(100))
    supports_save_states = Column(Boolean, default=True)
    supports_netplay = Column(Boolean, default=False)
    config_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class DownloadedCore(Base):
    """
    Downloaded emulator core information
    """
    __tablename__ = 'downloaded_cores'
    
    id = Column(Integer, primary_key=True)
    core_name = Column(String(100))
    core_version = Column(String(50))
    file_path = Column(String(255))
    file_size_mb = Column(Float)
    download_url = Column(String(512))
    downloaded_at = Column(DateTime, default=datetime.utcnow)
    checksum = Column(String(255))
    is_active = Column(Boolean, default=True)


class GameLibraryEntry(Base):
    """
    Game library entry
    """
    __tablename__ = 'game_library'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    core_name = Column(String(100))
    rom_path = Column(String(512))
    artwork_path = Column(String(512))
    play_time_minutes = Column(Integer, default=0)
    last_played = Column(DateTime)
    favorite = Column(Boolean, default=False)
    rating = Column(Float, default=0.0)
    added_at = Column(DateTime, default=datetime.utcnow)
