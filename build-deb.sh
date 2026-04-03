#!/bin/bash
# Build script for Scrcpy GUI DEB package

echo "=== Scrcpy GUI DEB Package Builder ==="
echo ""

# Get the absolute path to the current directory
BUILD_DIR="$(cd "$(dirname "$0")" && pwd)"
PACKAGE_NAME="scrcpy-gui"

# Try to get version from git tag, fallback to default
PACKAGE_VERSION="1.3"
if command -v git &> /dev/null && git rev-parse --git-dir > /dev/null 2>&1; then
    GIT_DESCRIBE=$(git describe --tags --abbrev=0 2>/dev/null)
    if [ $? -eq 0 ] && [ -n "$GIT_DESCRIBE" ]; then
        # Remove 'v' prefix if present
        PACKAGE_VERSION="${GIT_DESCRIBE#v}"
        echo "Using version from git tag: $PACKAGE_VERSION"
    else
        echo "No git tags found, using default version: $PACKAGE_VERSION"
    fi
else
    echo "Git not available or not a git repository, using default version: $PACKAGE_VERSION"
fi

# Clean previous builds
rm -rf ${PACKAGE_NAME}_${PACKAGE_VERSION}_all.deb

# Create the package directory structure
echo "Setting up package structure..."
rm -rf debian_package
mkdir -p debian_package/DEBIAN
mkdir -p debian_package/opt/${PACKAGE_NAME}

# Copy control file
cp ${BUILD_DIR}/debian/DEBIAN/control debian_package/DEBIAN/control

# Copy postinst and postrm scripts
cp ${BUILD_DIR}/debian/DEBIAN/postinst debian_package/DEBIAN/postinst
cp ${BUILD_DIR}/debian/DEBIAN/postrm debian_package/DEBIAN/postrm
chmod +x debian_package/DEBIAN/postinst debian_package/DEBIAN/postrm

# Copy desktop file
cp ${BUILD_DIR}/debian/DEBIAN/scrcpy-gui.desktop debian_package/opt/${PACKAGE_NAME}/

# Copy application files
echo "Copying application files..."
cp ${BUILD_DIR}/scrcpy_gui.py debian_package/opt/${PACKAGE_NAME}/
cp ${BUILD_DIR}/icon.png debian_package/opt/${PACKAGE_NAME}/ 2>/dev/null || true
cp ${BUILD_DIR}/scrcpy debian_package/opt/${PACKAGE_NAME}/ 2>/dev/null || true
cp ${BUILD_DIR}/scrcpy-server debian_package/opt/${PACKAGE_NAME}/ 2>/dev/null || true
cp ${BUILD_DIR}/adb debian_package/opt/${PACKAGE_NAME}/ 2>/dev/null || true

# Set proper permissions
chmod +x debian_package/opt/${PACKAGE_NAME}/scrcpy 2>/dev/null || true
chmod +x debian_package/opt/${PACKAGE_NAME}/scrcpy_gui.py
chmod +x debian_package/opt/${PACKAGE_NAME}/adb 2>/dev/null || true

# Build the package
echo "Building DEB package..."
dpkg-deb --build debian_package ${PACKAGE_NAME}_${PACKAGE_VERSION}_all.deb

# Clean up
rm -rf debian_package

echo ""
echo "=== Build Complete ==="
echo "DEB package created: ${PACKAGE_NAME}_${PACKAGE_VERSION}_all.deb"
echo ""
echo "To install:"
echo "  sudo dpkg -i ${PACKAGE_NAME}_${PACKAGE_VERSION}_all.deb"
echo ""
echo "To remove:"
echo "  sudo dpkg -r ${PACKAGE_NAME}"
echo ""
echo "After installation, run 'scrcpy-gui' to start the application."
echo "Or find it in your applications menu."
