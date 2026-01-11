/**
 * React Native Configuration
 * Required for React Native 0.76+ autolinking system
 */
module.exports = {
  project: {
    android: {
      packageName: 'com.phoneticsapp',
      sourceDir: './android/app',
    },
    ios: {
      sourceDir: './ios',
    },
  },
  dependencies: {
    // Native module configurations if needed
  },
};
