"""
Core Manager - Handles core download, installation, and management
"""

import os
import requests
import zipfile
import subprocess
from pathlib import Path
from core.cores_manifest import CORES_MANIFEST, get_bios_info
from core.models import DownloadedCore
from sqlalchemy.orm.session import Session


class CoreManager:
    """
    Manages emulator core downloads and installation
    """
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.cores_dir = os.path.join(
            os.path.expanduser('~'),
            '.pixel_edition',
            'cores'
        )
        self.roms_dir = os.path.join(
            os.path.expanduser('~'),
            '.pixel_edition',
            'roms'
        )
        self.bios_dir = os.path.join(
            os.path.expanduser('~'),
            '.pixel_edition',
            'bios'
        )
        
        # Create directories if they don't exist
        os.makedirs(self.cores_dir, exist_ok=True)
        os.makedirs(self.roms_dir, exist_ok=True)
        os.makedirs(self.bios_dir, exist_ok=True)
    
    def download_core(self, console_name, progress_callback=None):
        """
        Download emulator core for a console
        progress_callback: function(downloaded_bytes, total_bytes) for progress tracking
        """
        if console_name not in CORES_MANIFEST:
            return {'success': False, 'error': f'Console {console_name} not found'}
        
        console_info = CORES_MANIFEST[console_name]
        download_url = console_info['download_url']
        file_size_mb = console_info['file_size_mb']
        
        try:
            # Check if already downloaded
            existing = self.db_session.query(DownloadedCore).filter_by(
                core_name=console_name
            ).first()
            
            if existing:
                return {'success': True, 'message': 'Core already downloaded'}
            
            # Download core
            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            # Save to cores directory
            core_filename = f"{console_name.lower()}_core.zip"
            core_path = os.path.join(self.cores_dir, core_filename)
            
            with open(core_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size:
                            progress_callback(downloaded, total_size)
            
            # Extract if zip
            if core_path.endswith('.zip'):
                with zipfile.ZipFile(core_path, 'r') as zip_ref:
                    zip_ref.extractall(self.cores_dir)
                os.remove(core_path)
            
            # Store in database
            downloaded_core = DownloadedCore(
                core_name=console_name,
                core_version=console_info.get('version', '1.0.0'),
                file_path=os.path.join(self.cores_dir, console_name.lower()),
                file_size_mb=file_size_mb,
                download_url=download_url,
                is_active=True
            )
            self.db_session.add(downloaded_core)
            self.db_session.commit()
            
            return {'success': True, 'message': f'Core {console_name} downloaded successfully'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_console_rom_directory(self, console_name):
        """
        Create ROM directory for a console with optional BIOS subfolder
        """
        rom_path = os.path.join(self.roms_dir, console_name.lower())
        os.makedirs(rom_path, exist_ok=True)
        
        # Create BIOS folder if console needs it
        if console_name in CORES_MANIFEST:
            console_info = CORES_MANIFEST[console_name]
            if console_info.get('needs_bios'):
                bios_path = os.path.join(rom_path, 'bios')
                os.makedirs(bios_path, exist_ok=True)
                
                # Create instruction file
                bios_info = get_bios_info(console_name)
                if bios_info:
                    instruction_file = os.path.join(
                        bios_path,
                        'README_BIOS.txt'
                    )
                    with open(instruction_file, 'w') as f:
                        f.write(f"BIOS Files Required for {console_name}\n")
                        f.write(f"========================================\n\n")
                        f.write(f"Required Files: {', '.join(bios_info['required_files'])}\n\n")
                        f.write(f"Description: {bios_info['description']}\n\n")
                        f.write(f"Source: {bios_info['source']}\n\n")
                        f.write(f"Place BIOS files in this 'bios' folder.\n")
        
        return rom_path
    
    def get_console_directory(self, console_name):
        """
        Get ROM directory path for a console
        """
        return os.path.join(self.roms_dir, console_name.lower())
    
    def get_bios_directory(self, console_name):
        """
        Get BIOS directory path for a console
        """
        if console_name in CORES_MANIFEST:
            console_info = CORES_MANIFEST[console_name]
            if console_info.get('needs_bios'):
                return os.path.join(self.roms_dir, console_name.lower(), 'bios')
        return None
    
    def verify_bios_files(self, console_name):
        """
        Check if all required BIOS files are present
        Returns: {'complete': bool, 'missing': list, 'found': list}
        """
        if console_name not in CORES_MANIFEST:
            return {'complete': False, 'missing': [], 'found': []}
        
        console_info = CORES_MANIFEST[console_name]
        if not console_info.get('needs_bios'):
            return {'complete': True, 'missing': [], 'found': []}
        
        bios_info = get_bios_info(console_name)
        if not bios_info:
            return {'complete': True, 'missing': [], 'found': []}
        
        bios_dir = self.get_bios_directory(console_name)
        required_files = bios_info['required_files']
        
        found = []
        missing = []
        
        if bios_dir and os.path.exists(bios_dir):
            for bios_file in required_files:
                bios_path = os.path.join(bios_dir, bios_file)
                if os.path.exists(bios_path):
                    found.append(bios_file)
                else:
                    missing.append(bios_file)
        else:
            missing = required_files
        
        return {
            'complete': len(missing) == 0,
            'missing': missing,
            'found': found
        }
    
    def get_downloaded_cores(self):
        """
        Get list of all downloaded cores
        """
        return self.db_session.query(DownloadedCore).filter_by(
            is_active=True
        ).all()
    
    def is_core_downloaded(self, console_name):
        """
        Check if a core is already downloaded
        """
        core = self.db_session.query(DownloadedCore).filter_by(
            core_name=console_name,
            is_active=True
        ).first()
        return core is not None
