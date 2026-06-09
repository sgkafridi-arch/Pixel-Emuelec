"""
Equalizer/Cores Manifest - Complete list of supported emulator cores
Defines all available cores, their download links, BIOS requirements, and Tensor optimization profiles
"""

CORES_MANIFEST = {
    'Genesis': {
        'id': 'genesis',
        'name': 'Sega Genesis / Megadrive',
        'core_names': ['Genesis-Plus-GX', 'Picodrive'],
        'description': 'Sega Genesis and Megadrive emulator',
        'emulator': 'Picodrive',
        'version': '1.0.0',
        'download_url': 'https://github.com/libretro/picodrive/releases/download/1.0.0/picodrive_libretro.so.zip',
        'file_size_mb': 2.8,
        'bios_required': False,
        'supported_formats': ['.bin', '.gen', '.smd', '.md'],
        'performance_profile': 'Balanced',
        'needs_bios': False,
        'bios_files': [],
        'tensor_optimizations': {
            'G2': 'Balanced',
            'G3': 'Performance',
            'G4': 'Ultra Performance',
        }
    },
    'NES': {
        'id': 'nes',
        'name': 'Nintendo Entertainment System',
        'core_names': ['Nestopia', 'FCEUmm'],
        'description': 'NES emulator with high accuracy',
        'emulator': 'Nestopia',
        'version': '1.51.0',
        'download_url': 'https://github.com/libretro/nestopia/releases/download/1.51.0/nestopia_libretro.so.zip',
        'file_size_mb': 1.2,
        'bios_required': False,
        'supported_formats': ['.nes', '.bin'],
        'performance_profile': 'Balanced',
        'needs_bios': False,
        'bios_files': [],
        'tensor_optimizations': {
            'G2': 'Balanced',
            'G3': 'Performance',
            'G4': 'Ultra Performance',
        }
    },
    'SNES': {
        'id': 'snes',
        'name': 'Super Nintendo Entertainment System',
        'core_names': ['Snes9x', 'bsnes'],
        'description': 'SNES emulator with excellent compatibility',
        'emulator': 'Snes9x',
        'version': '1.62.3',
        'download_url': 'https://github.com/libretro/snes9x/releases/download/1.62.3/snes9x_libretro.so.zip',
        'file_size_mb': 1.8,
        'bios_required': False,
        'supported_formats': ['.smc', '.sfs', '.bin'],
        'performance_profile': 'Balanced',
        'needs_bios': False,
        'bios_files': [],
        'tensor_optimizations': {
            'G2': 'Balanced',
            'G3': 'Performance',
            'G4': 'Ultra Performance',
        }
    },
    'GBA': {
        'id': 'gba',
        'name': 'Game Boy Advance',
        'core_names': ['mGBA', 'VBA-M'],
        'description': 'GBA emulator with excellent accuracy',
        'emulator': 'mGBA',
        'version': '0.10.2',
        'download_url': 'https://github.com/mgba-emu/mgba/releases/download/0.10.2/mgba_libretro.so.zip',
        'file_size_mb': 2.1,
        'bios_required': True,
        'supported_formats': ['.gba', '.bin'],
        'performance_profile': 'Performance',
        'needs_bios': True,
        'bios_files': ['gba_bios.bin'],
        'tensor_optimizations': {
            'G2': 'Performance',
            'G3': 'Ultra Performance',
            'G4': 'Ultra Performance',
        }
    },
    'Dreamcast': {
        'id': 'dreamcast',
        'name': 'Sega Dreamcast',
        'core_names': ['Flycast'],
        'description': 'Dreamcast emulator with high compatibility',
        'emulator': 'Flycast',
        'version': '2.2.0',
        'download_url': 'https://github.com/flyinghead/flycast/releases/download/2.2.0/flycast_libretro.so.zip',
        'file_size_mb': 5.2,
        'bios_required': True,
        'supported_formats': ['.cdi', '.gdi', '.bin'],
        'performance_profile': 'Performance',
        'needs_bios': True,
        'bios_files': ['dc_boot.bin', 'dc_flash.bin'],
        'tensor_optimizations': {
            'G2': 'Performance',
            'G3': 'Ultra Performance',
            'G4': 'Ultra Performance',
        }
    },
    'Naomi': {
        'id': 'naomi',
        'name': 'Sega Naomi / Arcade',
        'core_names': ['Flycast'],
        'description': 'Sega Naomi arcade hardware emulator',
        'emulator': 'Flycast',
        'version': '2.2.0',
        'download_url': 'https://github.com/flyinghead/flycast/releases/download/2.2.0/flycast_libretro.so.zip',
        'file_size_mb': 5.2,
        'bios_required': True,
        'supported_formats': ['.bin', '.zip'],
        'performance_profile': 'Ultra Performance',
        'needs_bios': True,
        'bios_files': ['naomi_boot.bin', 'naomi_flash.bin'],
        'tensor_optimizations': {
            'G2': 'Ultra Performance',
            'G3': 'Ultra Performance',
            'G4': 'Ultra Performance',
        }
    },
    'PSX': {
        'id': 'psx',
        'name': 'Sony PlayStation 1',
        'core_names': ['PCSX ReARMed', 'Mednafen PSX'],
        'description': 'PlayStation 1 emulator',
        'emulator': 'PCSX ReARMed',
        'version': '1.0.0',
        'download_url': 'https://github.com/libretro/pcsx_rearmed/releases/download/1.0.0/pcsx_rearmed_libretro.so.zip',
        'file_size_mb': 3.5,
        'bios_required': True,
        'supported_formats': ['.bin', '.iso', '.cue'],
        'performance_profile': 'Performance',
        'needs_bios': True,
        'bios_files': ['scph1001.bin', 'scph5500.bin', 'scph5501.bin', 'scph5502.bin'],
        'tensor_optimizations': {
            'G2': 'Performance',
            'G3': 'Ultra Performance',
            'G4': 'Ultra Performance',
        }
    },
    'PS2': {
        'id': 'ps2',
        'name': 'Sony PlayStation 2',
        'core_names': ['PCSX2'],
        'description': 'PlayStation 2 emulator',
        'emulator': 'PCSX2',
        'version': '1.7.4',
        'download_url': 'https://github.com/PCSX2/pcsx2/releases/download/v1.7.4/pcsx2-v1.7.4-android-arm64-Release.apk',
        'file_size_mb': 61.8,
        'bios_required': True,
        'supported_formats': ['.bin', '.iso'],
        'performance_profile': 'Ultra Performance',
        'needs_bios': True,
        'bios_files': ['ps2_bios.bin'],
        'tensor_optimizations': {
            'G2': 'Ultra Performance',
            'G3': 'Ultra Performance',
            'G4': 'Ultra Performance',
        }
    },
    'PSP': {
        'id': 'psp',
        'name': 'Sony PlayStation Portable',
        'core_names': ['PPSSPP'],
        'description': 'PSP emulator with excellent performance',
        'emulator': 'PPSSPP',
        'version': '1.15.4',
        'download_url': 'https://github.com/hrydgard/ppsspp/releases/download/v1.15.4/ppsspp-v1.15.4-android-arm64.apk',
        'file_size_mb': 38.7,
        'bios_required': True,
        'supported_formats': ['.iso', '.cso'],
        'performance_profile': 'Performance',
        'needs_bios': True,
        'bios_files': ['EBOOT.PBP'],
        'tensor_optimizations': {
            'G2': 'Performance',
            'G3': 'Ultra Performance',
            'G4': 'Ultra Performance',
        }
    },
    'FBNeo': {
        'id': 'fbneo',
        'name': 'Final Burn Neo - Arcade',
        'core_names': ['FBNeo'],
        'description': 'Multi-arcade emulator with extensive game support',
        'emulator': 'FBNeo',
        'version': '1.0.0',
        'download_url': 'https://github.com/finalburnneo/FBNeo/releases/download/v1.0.0/fbneoarm64.so.zip',
        'file_size_mb': 45.5,
        'bios_required': False,
        'supported_formats': ['.zip', '.bin'],
        'performance_profile': 'Performance',
        'needs_bios': False,
        'bios_files': [],
        'tensor_optimizations': {
            'G2': 'Performance',
            'G3': 'Ultra Performance',
            'G4': 'Ultra Performance',
        }
    },
}

# BIOS Requirements Summary
BIOS_REQUIREMENTS = {
    'GBA': {
        'required_files': ['gba_bios.bin'],
        'description': 'GBA System BIOS',
        'source': 'GBA cartridge dump',
    },
    'Dreamcast': {
        'required_files': ['dc_boot.bin', 'dc_flash.bin'],
        'description': 'Dreamcast BIOS files',
        'source': 'Dreamcast system dump',
    },
    'Naomi': {
        'required_files': ['naomi_boot.bin', 'naomi_flash.bin'],
        'description': 'Naomi arcade system BIOS',
        'source': 'Naomi arcade board dump',
    },
    'PSX': {
        'required_files': ['scph1001.bin', 'scph5500.bin', 'scph5501.bin', 'scph5502.bin'],
        'description': 'PlayStation 1 region-specific BIOS files',
        'source': 'PSX console dump',
    },
    'PS2': {
        'required_files': ['ps2_bios.bin'],
        'description': 'PlayStation 2 BIOS',
        'source': 'PS2 console dump',
    },
    'PSP': {
        'required_files': ['EBOOT.PBP'],
        'description': 'PSP system firmware',
        'source': 'PSP system dump',
    },
}

# Console Categories
CONSOLE_CATEGORIES = {
    '2D_Consoles': {
        'name': '2D Consoles',
        'description': 'Classic 2D gaming systems',
        'consoles': ['Genesis', 'NES', 'SNES'],
    },
    'Handheld': {
        'name': 'Handheld',
        'description': 'Portable gaming devices',
        'consoles': ['GBA', 'PSP'],
    },
    '3D_Consoles': {
        'name': '3D Consoles',
        'description': 'Advanced 3D gaming systems',
        'consoles': ['PSX', 'PS2', 'Dreamcast', 'Naomi'],
    },
    'Arcade': {
        'name': 'Arcade',
        'description': 'Arcade and multi-game systems',
        'consoles': ['FBNeo'],
    },
}

def get_console_info(console_id):
    """
    Get information about a specific console
    """
    for console_name, info in CORES_MANIFEST.items():
        if info.get('id') == console_id:
            return info
    return None

def get_bios_info(console_name):
    """
    Get BIOS requirements for a console
    """
    return BIOS_REQUIREMENTS.get(console_name, None)

def get_all_consoles():
    """
    Get list of all available consoles
    """
    return list(CORES_MANIFEST.keys())

def needs_bios(console_name):
    """
    Check if console needs BIOS files
    """
    console = CORES_MANIFEST.get(console_name, {})
    return console.get('needs_bios', False)

def get_tensor_profile(console_name, tensor_generation='G4'):
    """
    Get optimal Tensor performance profile for a console
    """
    console = CORES_MANIFEST.get(console_name, {})
    optimizations = console.get('tensor_optimizations', {})
    return optimizations.get(tensor_generation, 'Balanced')
