#!/bin/bash
# Flutter Setup Script for WSL2/Linux

echo "📥 Installing Flutter..."

# Check if Flutter SDK directory exists
if [ ! -d "$HOME/flutter" ]; then
    echo "Downloading Flutter SDK..."
    cd $HOME
    git clone https://github.com/flutter/flutter.git -b stable
    echo "✓ Flutter SDK downloaded"
else
    echo "✓ Flutter SDK already exists"
fi

# Add to PATH
export PATH="$PATH:$HOME/flutter/bin"
export PATH="$PATH:$HOME/flutter/bin/cache/dart-sdk/bin"

# Add to bashrc for persistence
if ! grep -q "flutter/bin" ~/.bashrc; then
    echo 'export PATH="$PATH:$HOME/flutter/bin"' >> ~/.bashrc
    echo 'export PATH="$PATH:$HOME/flutter/bin/cache/dart-sdk/bin"' >> ~/.bashrc
    echo "✓ Added Flutter to PATH in ~/.bashrc"
fi

# Run Flutter doctor
echo ""
echo "Running Flutter doctor..."
flutter doctor --android-licenses || true

echo ""
echo "✓ Flutter setup complete!"
echo ""
echo "Next steps:"
echo "1. Reload your shell: source ~/.bashrc"
echo "2. Run: flutter doctor"
echo "3. Check Android SDK: flutter doctor -v"
echo ""
