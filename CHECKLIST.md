# Getting Started Checklist

Use this checklist to set up and test your new React-based Phonetics App.

## ✅ Setup Checklist

### Prerequisites
- [ ] Node.js 18+ installed (`node --version`)
- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] npm installed (`npm --version`)
- [ ] Git installed (optional, for version control)

### For Mobile Development
- [ ] Android Studio installed (for Android)
- [ ] Xcode installed (for iOS, macOS only)
- [ ] React Native CLI installed (`npm install -g react-native-cli`)

## 📦 Installation Steps

### 1. Initial Setup
```bash
# Navigate to project
cd /path/to/phonetics-app

# Make scripts executable
chmod +x setup-react.sh start-react-dev.sh

# Run setup (installs all dependencies)
./setup-react.sh
```

- [ ] Backend dependencies installed
- [ ] Web app dependencies installed
- [ ] Mobile app dependencies installed
- [ ] iOS pods installed (macOS only)

### 2. Configuration

**Backend (.env):**
```bash
cd backend
cp .env.example .env
# Edit .env file with your settings
```

- [ ] Database URL configured
- [ ] JWT secret set
- [ ] CORS origins configured

**Web App (.env):**
```bash
cd react-web
cp .env.example .env
# VITE_API_URL=http://localhost:8000
```

- [ ] API URL configured

**Mobile App:**
```bash
cd react-native-mobile/src/services/api.js
# Update API_BASE_URL for your environment
```

- [ ] API URL configured for development
- [ ] API URL configured for production

## 🚀 Running the Apps

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

- [ ] Backend starts without errors
- [ ] Accessible at http://localhost:8000
- [ ] API docs available at http://localhost:8000/docs

### Web App
```bash
cd react-web
npm run dev
```

- [ ] Web app starts without errors
- [ ] Accessible at http://localhost:3000
- [ ] Hot reload works

### Mobile - Android
```bash
cd react-native-mobile
npm run android
```

- [ ] Android emulator launches
- [ ] App installs and opens
- [ ] No red error screens

### Mobile - iOS (macOS only)
```bash
cd react-native-mobile
npm run ios
```

- [ ] iOS simulator launches
- [ ] App installs and opens
- [ ] No red error screens

## 🧪 Testing Checklist

### Backend Testing
- [ ] Visit http://localhost:8000/docs
- [ ] API documentation loads
- [ ] Can see all endpoints

### Web App Testing

**Authentication:**
- [ ] Can access landing page (/)
- [ ] Can navigate to login page
- [ ] Can navigate to register page
- [ ] Can create new account
- [ ] Can login with credentials
- [ ] Redirects to dashboard after login
- [ ] Can logout

**Main Features:**
- [ ] Dashboard displays stats
- [ ] Can navigate to Today's Lesson
- [ ] Can navigate to Practice
- [ ] Can navigate to Progress
- [ ] Can navigate to Parent View
- [ ] All pages load without errors

**Today's Lesson:**
- [ ] Lesson data loads
- [ ] Phoneme displays correctly
- [ ] Can start audio recording
- [ ] Can stop audio recording
- [ ] Recording submits successfully

### Mobile App Testing

**Authentication:**
- [ ] Welcome screen displays
- [ ] Can navigate to login
- [ ] Can navigate to register
- [ ] Can create account
- [ ] Can login
- [ ] Can logout

**Navigation:**
- [ ] Bottom tabs work
- [ ] Dashboard tab active
- [ ] Today tab works
- [ ] Practice tab works
- [ ] Progress tab works
- [ ] Profile tab works

**Features:**
- [ ] Dashboard shows stats
- [ ] Today's lesson loads
- [ ] Audio recording works
- [ ] Progress displays
- [ ] Profile shows user info

## 🐛 Troubleshooting

### Backend Issues
- [ ] Check Python version (3.8+)
- [ ] Verify virtual environment is activated
- [ ] Reinstall dependencies: `pip install -r requirements.txt`
- [ ] Check .env file exists and is configured
- [ ] Verify database is running

### Web App Issues
- [ ] Check Node version (18+)
- [ ] Clear node_modules: `rm -rf node_modules package-lock.json && npm install`
- [ ] Check .env file exists
- [ ] Verify backend is running
- [ ] Check browser console for errors

### Mobile App Issues

**General:**
- [ ] Check Node version (18+)
- [ ] Clear node_modules: `rm -rf node_modules && npm install`
- [ ] Verify backend is running
- [ ] Check Metro bundler is running

**Android:**
- [ ] Android Studio properly configured
- [ ] Emulator is running
- [ ] Check `adb devices` shows device
- [ ] Clean build: `cd android && ./gradlew clean`
- [ ] Check API URL is correct (use 10.0.2.2 for emulator)

**iOS:**
- [ ] Xcode properly installed
- [ ] CocoaPods installed
- [ ] Pods installed: `cd ios && pod install`
- [ ] Simulator is running
- [ ] Check API URL is correct (use localhost for simulator)

## 📊 Performance Checklist

### Web App
- [ ] Page loads in < 3 seconds
- [ ] Navigation is smooth
- [ ] No console errors
- [ ] Responsive on mobile browsers
- [ ] Animations are smooth

### Mobile App
- [ ] App launches in < 3 seconds
- [ ] Navigation is smooth
- [ ] No crash errors
- [ ] Scrolling is smooth
- [ ] Audio recording works properly

## 🚢 Production Readiness

### Before Deploying

**Web App:**
- [ ] Update API URL in .env for production
- [ ] Build production bundle: `npm run build`
- [ ] Test production build: `npm run preview`
- [ ] Check bundle size (should be < 500KB)
- [ ] Test on different browsers

**Mobile Apps:**
- [ ] Update API URL to production
- [ ] Change app icon
- [ ] Update app name in app.json
- [ ] Test on real devices
- [ ] Generate signed APK (Android)
- [ ] Archive and submit (iOS)

**Backend:**
- [ ] Set production environment variables
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up database backups
- [ ] Enable logging
- [ ] Set up monitoring

### Security Checklist
- [ ] All secrets in environment variables
- [ ] No hardcoded credentials
- [ ] HTTPS enabled
- [ ] JWT tokens properly secured
- [ ] Input validation working
- [ ] Rate limiting configured

## 📚 Documentation Review

- [ ] Read [README_REACT.md](README_REACT.md)
- [ ] Read [QUICK_START_REACT.md](QUICK_START_REACT.md)
- [ ] Read [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- [ ] Read [react-web/README.md](react-web/README.md)
- [ ] Read [react-native-mobile/README.md](react-native-mobile/README.md)

## 🎉 Final Steps

- [ ] All tests passing
- [ ] No critical bugs
- [ ] Documentation complete
- [ ] Team trained on new stack
- [ ] Backup of old Flutter code (optional)
- [ ] Ready to delete Flutter directories

### Optional: Remove Flutter Code
```bash
# Only do this after confirming React version works!
rm -rf flutter_app/
rm -rf frontend/
rm -rf flutter_plugins/
rm -f FLUTTER_*.md
```

- [ ] Flutter code removed
- [ ] Git commit: "Complete migration to React"

## ✅ Sign-Off

- [ ] Developer tested: _______________
- [ ] QA tested: _______________
- [ ] Product owner approved: _______________
- [ ] Ready for production: _______________

---

**Congratulations! Your React migration is complete! 🎉**

*Use this checklist to ensure everything is working correctly before going to production.*
