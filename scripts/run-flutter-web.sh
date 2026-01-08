#!/bin/bash
export PATH="/root/flutter/bin:$PATH"
export FLUTTER_ROOT="/root/flutter"
cd /mnt/c/Users/harri/designProject2020/education-projs/phonetics-app/frontend
echo "Starting Flutter web app on port 3001..."
flutter run -d chrome --web-port=3001 --no-fast-start
