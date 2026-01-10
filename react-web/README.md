# Phonetics Web App (React)

Modern web application built with React, Vite, and Tailwind CSS.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Features

- ⚡ Lightning-fast development with Vite
- 🎨 Beautiful UI with Tailwind CSS
- 📱 Responsive design for all devices
- 🔐 Secure authentication with JWT
- 🎯 State management with Zustand
- ✨ Smooth animations with Framer Motion
- 📝 Form validation with React Hook Form & Zod

## Project Structure

```
react-web/
├── src/
│   ├── components/      # Reusable UI components
│   ├── pages/          # Page components
│   ├── services/       # API services
│   ├── store/          # State management
│   ├── App.jsx         # Main app component
│   ├── main.jsx        # Entry point
│   └── index.css       # Global styles
├── public/             # Static assets
└── index.html          # HTML template
```

## Environment Variables

Create a `.env` file in the root:

```
VITE_API_URL=http://localhost:8000
```

## Available Scripts

- `npm run dev` - Start development server on http://localhost:3000
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

## Backend Integration

The app connects to the FastAPI backend at `http://localhost:8000` by default.
Make sure the backend is running before starting the web app.

## Technologies

- React 18
- Vite 5
- Tailwind CSS 3
- Zustand (State Management)
- React Router v6
- Axios
- Framer Motion
- React Hook Form
- Zod
