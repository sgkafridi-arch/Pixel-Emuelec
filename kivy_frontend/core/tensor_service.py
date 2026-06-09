"""
Tensor device detection and optimization service
"""

import subprocess
from core.models import TensorDeviceInfo
from core.database import get_db_session


class TensorOptimizationService:
    """
    Detects Tensor chip and optimizes settings
    """
    
    TENSOR_DEVICES = {
        'tensor': 'G2',
        'tensor_2': 'G2',
        'tensor_pro': 'G2',
        'tensor_2nd': 'G3',
        'tensor_3': 'G3',
        'tensor_3rd': 'G4',
        'tensor_4': 'G4',
    }
    
    def __init__(self):
        self.device_info = None
        self.db_session = get_db_session()
    
    def detect_device(self):
        """
        Detect device Tensor chip and capabilities
        """
        try:
            device_name = self._get_device_name()
            tensor_gen = self._detect_tensor_generation()
            ram = self._get_ram_gb()
            refresh_rate = self._get_refresh_rate()
            vulkan_version = self._get_vulkan_version()
            android_version = self._get_android_version()
            
            device_info = TensorDeviceInfo(
                device_name=device_name,
                tensor_generation=tensor_gen,
                ram_gb=ram,
                refresh_rate=refresh_rate,
                vulkan_support=vulkan_version is not None,
                vulkan_version=vulkan_version,
                android_version=android_version
            )
            
            self.db_session.add(device_info)
            self.db_session.commit()
            self.device_info = device_info
            
            print(f"Detected: {device_name} - Tensor {tensor_gen} - {ram}GB RAM")
            
        except Exception as e:
            print(f"Error detecting device: {e}")
            self.device_info = None
    
    def _get_device_name(self):
        """Get device name"""
        try:
            result = subprocess.run(
                ['getprop', 'ro.product.model'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() or 'Unknown Device'
        except:
            return 'Unknown Device'
    
    def _detect_tensor_generation(self):
        """Detect Tensor generation"""
        try:
            result = subprocess.run(
                ['getprop', 'ro.soc.model'],
                capture_output=True,
                text=True,
                timeout=5
            )
            soc_model = result.stdout.strip().lower()
            
            for key, value in self.TENSOR_DEVICES.items():
                if key in soc_model:
                    return value
            
            return 'Unknown'
        except:
            return 'Unknown'
    
    def _get_ram_gb(self):
        """Get available RAM in GB"""
        try:
            result = subprocess.run(
                ['grep', 'MemTotal', '/proc/meminfo'],
                capture_output=True,
                text=True,
                timeout=5
            )
            mem_kb = int(result.stdout.split()[1])
            return mem_kb // (1024 * 1024)
        except:
            return 8
    
    def _get_refresh_rate(self):
        """Get display refresh rate"""
        return 120  # Pixel 7+ typically has 120Hz
    
    def _get_vulkan_version(self):
        """Get Vulkan version"""
        try:
            result = subprocess.run(
                ['getprop', 'ro.hardware.vulkan'],
                capture_output=True,
                text=True,
                timeout=5
            )
            version = result.stdout.strip()
            return version if version else '1.3'
        except:
            return None
    
    def _get_android_version(self):
        """Get Android version"""
        try:
            result = subprocess.run(
                ['getprop', 'ro.build.version.release'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return int(result.stdout.strip().split('.')[0])
        except:
            return 14
