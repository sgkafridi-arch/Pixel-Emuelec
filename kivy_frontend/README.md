# Pixel Edition - Kivy Frontend

**Tensor-optimized emulator frontend for Google Pixel devices**

## 🎮 Features

- Material You design system
- Tensor chip optimization (G2, G3, G4)
- 4 performance profiles (Battery Saver, Balanced, Performance, Ultra)
- Support for 5 emulator cores (FBNeo, Flycast, PPSSPP, YabaSanshiro, PCSX2)
- Vulkan-first graphics architecture
- 60-120 FPS smooth UI
- Game library management
- Save state support

## 🏗️ Architecture

### Core Components
- `main.py` - Main Kivy application
- `core/` - Backend services
  - `database.py` - SQLAlchemy setup
  - `models.py` - Database models
  - `tensor_service.py` - Device detection
  - `performance_profiles.py` - Profile management
- `ui/` - UI layer
  - `theme_engine.py` - Material You theming
  - `screens/` - Application screens

## 🚀 Quick Start

### Desktop Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

### Android Build

```bash
# Install Buildozer
pip install buildozer

# Build debug APK
buildozer android debug

# Install on device
adb install bin/pixeledition-0.1.0-debug.apk
```

## 📱 Supported Devices

**Primary Targets:**
- Google Pixel 7, 7 Pro, 7a
- Google Pixel Fold
- Google Pixel Tablet
- Google Pixel 8, 8 Pro, 8a
- Google Pixel 9, 9 Pro, 9 Pro XL, 9 Pro Fold

## 🎯 Emulator Cores

| Core | Version | Type | Size |
|------|---------|------|------|
| FBNeo | 1.0.0 | Arcade | 45.5 MB |
| Flycast | 2.0 | Dreamcast | 52.3 MB |
| PPSSPP | 1.15.4 | PSP | 38.7 MB |
| YabaSanshiro | 1.5 | Saturn | 35.2 MB |
| PCSX2 | 1.7.4 | PS2 | 61.8 MB |

## 🔧 Database Schema

### Tables
- `tensor_device_info` - Device capabilities
- `performance_profiles` - Performance settings
- `core_configurations` - Emulator core settings
- `downloaded_cores` - Downloaded cores metadata
- `game_library` - Game library entries

## 🎨 UI Screens

1. **Home Screen** - Featured games, recently played
2. **Library Screen** - Game browser with search
3. **Settings Screen** - Configuration options
4. **Downloader Screen** - Core management

## 📊 Performance Profiles

### Battery Saver
- 30 FPS target
- Minimal GPU load
- Lower quality graphics

### Balanced
- 60 FPS target
- Moderate GPU load
- Medium quality graphics

### Performance
- 120 FPS target
- High GPU load
- High quality graphics

### Ultra Performance
- 120+ FPS target
- Maximum GPU load
- Ultra quality graphics

## 🔗 Core Download Links

- **FBNeo**: https://github.com/finalburnneo/FBNeo/releases
- **Flycast**: https://github.com/flyinghead/flycast/releases
- **PPSSPP**: https://github.com/hrydgard/ppsspp/releases
- **YabaSanshiro**: https://github.com/devmiyax/yabaSanshiro/releases
- **PCSX2**: https://github.com/PCSX2/pcsx2/releases

## 📝 License

MIT License
