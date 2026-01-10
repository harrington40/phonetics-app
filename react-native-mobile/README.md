# Phonetics Mobile App (React Native)

Cross-platform mobile application for Android and iOS built with React Native.

## Prerequisites

- Node.js >= 18
- React Native CLI
- Android Studio (for Android development)
- Xcode (for iOS development, macOS only)

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. iOS Setup (macOS only)

```bash
cd ios
pod install
cd ..
```

### 3. Run the App

**Android:**
```bash
npm run android
```

**iOS:**
```bash
npm run ios
```

## Project Structure

```
react-native-mobile/
├── src/
│   ├── screens/
│   │   ├── auth/          # Authentication screens
│   │   └── main/          # Main app screens
│   ├── services/          # API services
│   ├── store/             # State management (Zustand)
│   └── App.js             # Main app component
├── android/               # Android native code
├── ios/                   # iOS native code
└── index.js              # Entry point
```

## Features

- 📱 Native performance on iOS and Android
- 🎨 Beautiful native UI components
- 🔐 Secure authentication
- 🎤 Audio recording for phonics practice
- 📊 Progress tracking
- 🎯 State management with Zustand
- 🚀 Fast navigation with React Navigation

## Backend Configuration

Update the API URL in `src/services/api.js`:

```javascript
const API_BASE_URL = __DEV__ 
  ? 'http://10.0.2.2:8000'  // Android emulator
  : 'https://your-production-api.com';
```

For iOS simulator, use `http://localhost:8000`

## Build for Production

### Android

```bash
cd android
./gradlew assembleRelease
```

### iOS

1. Open `ios/PhoneticsApp.xcworkspace` in Xcode
2. Select your device/simulator
3. Product > Archive
4. Follow App Store distribution steps

## Troubleshooting

### Android Issues

```bash
# Clean build
npm run clean
cd android && ./gradlew clean && cd ..

# Rebuild
npm run android
```

### iOS Issues

```bash
# Clean build
npm run clean:ios

# Reinstall pods
npm run pod-install

# Rebuild
npm run ios
```

## Technologies

- React Native 0.73
- React Navigation v6
- Zustand (State Management)
- Axios
- React Native Vector Icons
- React Native Audio Recorder
- React Native Linear Gradient
