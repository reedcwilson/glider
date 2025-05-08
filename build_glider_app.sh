#!/bin/bash

# Build script for Glider.app
# This script builds a macOS .app bundle for the Glider application

# Exit on error
set -e

echo "=== Building Glider.app ==="

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/Glider dist/Glider.app dist/Glider dist/Glider.dmg

# Build the app using PyInstaller
echo "Building app with PyInstaller..."
pyinstaller Glider.spec

# Verify the app was built
if [ ! -d "dist/Glider.app" ]; then
    echo "Error: App build failed. dist/Glider.app not found."
    exit 1
fi

# Fix permissions
echo "Fixing permissions..."
chmod -R +x dist/Glider.app

# Create a wrapper script to ensure proper environment
echo "Creating wrapper script..."
cat > dist/Glider.app/Contents/MacOS/GliderLauncher << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
export PYTHONHOME="$(dirname "$(dirname "$0")")/Frameworks/Python.framework/Versions/Current"
export DYLD_LIBRARY_PATH="$(dirname "$(dirname "$0")")/Frameworks:$DYLD_LIBRARY_PATH"
export QT_PLUGIN_PATH="$(dirname "$(dirname "$0")")/Frameworks/PyQt6/Qt6/plugins"
export QT_QPA_PLATFORM_PLUGIN_PATH="$(dirname "$(dirname "$0")")/Frameworks/PyQt6/Qt6/plugins/platforms"
./Glider.bin "$@"
EOF

chmod +x dist/Glider.app/Contents/MacOS/GliderLauncher

# Rename the original executable and make the wrapper the main executable
mv dist/Glider.app/Contents/MacOS/Glider dist/Glider.app/Contents/MacOS/Glider.bin
mv dist/Glider.app/Contents/MacOS/GliderLauncher dist/Glider.app/Contents/MacOS/Glider

# Update Info.plist to ensure proper app behavior
echo "Updating Info.plist..."
/usr/libexec/PlistBuddy -c "Add :NSHighResolutionCapable bool true" dist/Glider.app/Contents/Info.plist 2>/dev/null || true
/usr/libexec/PlistBuddy -c "Add :NSSupportsAutomaticGraphicsSwitching bool true" dist/Glider.app/Contents/Info.plist 2>/dev/null || true
/usr/libexec/PlistBuddy -c "Add :NSRequiresAquaSystemAppearance bool false" dist/Glider.app/Contents/Info.plist 2>/dev/null || true

echo "App built successfully at dist/Glider.app"

# Create a DMG (optional)
echo "Creating DMG installer..."

# Create a folder for DMG preparation
mkdir -p dist/dmg
rm -rf dist/dmg/*

# Copy the app bundle to the dmg folder
cp -r "dist/Glider.app" dist/dmg

# Remove any existing DMG
test -f "dist/Glider.dmg" && rm "dist/Glider.dmg"

# Check if create-dmg is installed
if command -v create-dmg &> /dev/null; then
    create-dmg \
      --volname "Glider" \
      --volicon "glider.icns" \
      --window-pos 200 120 \
      --window-size 600 300 \
      --icon-size 100 \
      --icon "Glider.app" 175 120 \
      --hide-extension "Glider.app" \
      --app-drop-link 425 120 \
      "dist/Glider.dmg" \
      "dist/dmg/"
    
    echo "DMG created at dist/Glider.dmg"
else
    echo "Warning: create-dmg not found. DMG creation skipped."
    echo "To install create-dmg: brew install create-dmg"
    
    # Create a simple zip file instead
    echo "Creating zip archive instead..."
    cd dist
    zip -r Glider.zip Glider.app
    cd ..
    echo "Zip archive created at dist/Glider.zip"
fi

echo "=== Build completed successfully ==="
