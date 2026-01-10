# Phonetics App - React Architecture

> **🎉 Complete migration from Flutter to React + React Native**

A comprehensive phonetics learning application with:
- **React Web App** - Modern web interface with Vite + Tailwind CSS
- **React Native Mobile** - Native iOS & Android apps
- **Python FastAPI Backend** - Same robust backend (unchanged)

## 📁 Project Structure

```
phonetics-app/
├── backend/                      # Python FastAPI (UNCHANGED)
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   ├── models/
│   │   └── services/
│   └── requirements.txt
│
├── react-web/                    # NEW: React Web App
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── store/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── react-native-mobile/          # NEW: React Native Mobile
│   ├── src/
│   │   ├── screens/
│   │   ├── services/
│   │   ├── store/
│   │   └── App.js
│   ├── android/
│   ├── ios/
│   └── package.json
│
├── flutter_app/                  # OLD: Flutter (can be removed)
└── frontend/                     # OLD: Flutter (can be removed)
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.8+
- **Android Studio** (for Android development)
- **Xcode** (for iOS development, macOS only)

### Setup Everything at Once

```bash
# Make setup script executable
chmod +x setup-react.sh

# Run setup
./setup-react.sh
```

### Manual Setup

#### 1. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
```

#### 2. Web App Setup

```bash
cd react-web
npm install
cp .env.example .env
# VITE_API_URL=http://localhost:8000
```

#### 3. Mobile App Setup

```bash
cd react-native-mobile
npm install

# For iOS (macOS only)
cd ios && pod install && cd ..
```

## 🎯 Running the Apps

### Option 1: Start All Services (Recommended)

```bash
chmod +x start-react-dev.sh
./start-react-dev.sh
```

This starts:
- Backend on http://localhost:8000
- Web app on http://localhost:3000

### Option 2: Start Services Individually

**Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Web App:**
```bash
cd react-web
npm run dev
```

**Mobile App - Android:**
```bash
cd react-native-mobile
npm run android
```

**Mobile App - iOS:**
```bash
cd react-native-mobile
npm run ios
```

## 🐳 Docker Deployment

```bash
# Build and start all services
docker-compose -f docker-compose-react.yml up -d

# Stop all services
docker-compose -f docker-compose-react.yml down
```

## 🌟 Features

### Web App (React + Vite)
- ⚡ Lightning-fast development with Vite
- 🎨 Beautiful UI with Tailwind CSS
- 📱 Fully responsive design
- 🔐 JWT authentication
- 🎯 Zustand state management
- ✨ Framer Motion animations
- 📝 Form validation with React Hook Form + Zod

### Mobile App (React Native)
- 📱 Native iOS & Android apps
- 🎨 Native UI components
- 🔐 Secure authentication
- 🎤 Audio recording for phonics
- 📊 Progress tracking
- 🚀 React Navigation
- 💾 AsyncStorage persistence

### Backend (FastAPI) - UNCHANGED
- 🐍 Python FastAPI
- 🗃️ PostgreSQL database
- 🔒 JWT authentication
- 📝 Pydantic validation
- 📚 OpenAPI documentation
- 🚀 High performance

## 📚 Documentation

- [React Web README](react-web/README.md)
- [React Native README](react-native-mobile/README.md)
- [Backend README](backend/README.md)

## 🔧 Development

### Web App

```bash
cd react-web

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Format code
npm run format
```

### Mobile App

```bash
cd react-native-mobile

# Run on Android
npm run android

# Run on iOS
npm run ios

# Clean build
npm run clean

# Clean iOS build
npm run clean:ios
```

## 📦 Building for Production

### Web App

```bash
cd react-web
npm run build
# Files will be in dist/
```

### Android APK

```bash
cd react-native-mobile/android
./gradlew assembleRelease
# APK: android/app/build/outputs/apk/release/
```

### iOS IPA

1. Open `react-native-mobile/ios/PhoneticsApp.xcworkspace` in Xcode
2. Select Product > Archive
3. Follow App Store distribution steps

## 🗑️ Removing Flutter

Once you've tested the React apps and confirmed everything works:

```bash
# Remove Flutter directories
rm -rf flutter_app/
rm -rf frontend/
rm -rf flutter_plugins/

# Remove Flutter documentation files
rm -f FLUTTER_*.md
```

## 🔄 Migration Benefits

### Why React + React Native?

1. **Single Language**: JavaScript/TypeScript across web and mobile
2. **Code Sharing**: Share logic, utilities, and components
3. **Larger Ecosystem**: More packages, better community support
4. **Web + Mobile**: True cross-platform with React Native Web option
5. **Better Developer Experience**: Hot reload, better debugging
6. **Industry Standard**: More developers know React than Flutter

### What Changed?

- ✅ **Frontend**: Flutter → React (web) + React Native (mobile)
- ✅ **State Management**: Riverpod → Zustand
- ✅ **Styling**: Flutter widgets → Tailwind CSS (web) + StyleSheet (mobile)
- ✅ **Navigation**: Flutter Router → React Router (web) + React Navigation (mobile)
- ⚡ **Backend**: NO CHANGES - same FastAPI backend

## 🤝 Contributing

The app now uses React and React Native. All Flutter code in `flutter_app/` and `frontend/` directories is deprecated.

## 📄 License

MIT License - see LICENSE file

## 🆘 Support

- **Backend Issues**: Same as before
- **Web Issues**: Check [react-web/README.md](react-web/README.md)
- **Mobile Issues**: Check [react-native-mobile/README.md](react-native-mobile/README.md)

---

**🎉 Welcome to the React + React Native version of Phonetics App!**
