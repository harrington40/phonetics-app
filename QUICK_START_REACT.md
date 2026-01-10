# Quick Start Guide - React Version

## 🚀 Get Started in 5 Minutes

### Step 1: Setup (One Time Only)

```bash
# Make scripts executable
chmod +x setup-react.sh start-react-dev.sh

# Run setup
./setup-react.sh
```

This installs all dependencies for backend, web, and mobile apps.

### Step 2: Start Development

```bash
# Start backend + web app together
./start-react-dev.sh
```

**URLs:**
- Web App: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Step 3: Start Mobile App (Optional)

**Android:**
```bash
cd react-native-mobile
npm run android
```

**iOS (macOS only):**
```bash
cd react-native-mobile
npm run ios
```

## 📱 What You Get

### Web App (React)
- Modern responsive design
- Works on desktop, tablet, mobile browsers
- Fast loading with Vite
- Beautiful animations

### Mobile Apps (React Native)
- Native iOS app
- Native Android app
- Smooth performance
- Native UI components

### Backend (Python FastAPI)
- Same backend as before
- No changes needed
- RESTful API
- Auto-generated docs

## 🎯 Common Tasks

### Run Backend Only
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Run Web App Only
```bash
cd react-web
npm run dev
```

### Build Web for Production
```bash
cd react-web
npm run build
# Files in dist/
```

### Build Android APK
```bash
cd react-native-mobile/android
./gradlew assembleRelease
```

## 🐛 Troubleshooting

### Backend Issues
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Web App Issues
```bash
cd react-web
rm -rf node_modules package-lock.json
npm install
```

### Mobile App Issues
```bash
cd react-native-mobile
rm -rf node_modules package-lock.json
npm install

# Android
npm run clean
npm run android

# iOS
npm run clean:ios
npm run pod-install
npm run ios
```

## 📚 Learn More

- [Full README](README_REACT.md)
- [Migration Guide](MIGRATION_GUIDE.md)
- [Web App Docs](react-web/README.md)
- [Mobile App Docs](react-native-mobile/README.md)

## 🎉 That's It!

You now have:
- ✅ React web app
- ✅ React Native mobile apps (iOS + Android)
- ✅ Python backend
- ✅ Complete phonetics learning platform

**No more Flutter! Pure JavaScript/React ecosystem!**
