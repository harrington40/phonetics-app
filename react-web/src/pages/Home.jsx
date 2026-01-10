import { Link } from 'react-router-dom';
import { BookOpen, Sparkles, Trophy, Users } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Home() {
  const features = [
    {
      icon: BookOpen,
      title: 'Interactive Lessons',
      description: 'Fun phonics lessons with animated characters',
    },
    {
      icon: Sparkles,
      title: 'AI-Powered',
      description: 'Personalized learning paths for every child',
    },
    {
      icon: Trophy,
      title: 'Track Progress',
      description: 'Monitor achievements and celebrate milestones',
    },
    {
      icon: Users,
      title: 'Parent Dashboard',
      description: 'Stay connected with your child\'s learning journey',
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-br from-pink-400 via-purple-400 to-blue-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h1 className="text-5xl md:text-7xl font-display font-bold text-white mb-6">
                Learn Phonics
                <br />
                <span className="text-yellow-200">The Fun Way!</span>
              </h1>
              <p className="text-xl md:text-2xl text-white/90 mb-8 max-w-2xl mx-auto">
                Interactive phonetics learning with cartoon friends, 
                perfect for early learners aged 3-8
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link
                  to="/register"
                  className="btn-primary text-lg px-8 py-4 bg-white text-purple-600 hover:bg-yellow-100"
                >
                  Start Learning Free
                </Link>
                <Link
                  to="/login"
                  className="btn-secondary text-lg px-8 py-4 bg-white/20 text-white border-white hover:bg-white/30"
                >
                  Sign In
                </Link>
              </div>
            </motion.div>
          </div>
        </div>

        {/* Decorative elements */}
        <div className="absolute top-20 left-10 w-20 h-20 bg-yellow-300 rounded-full opacity-50 animate-bounce-slow"></div>
        <div className="absolute bottom-20 right-20 w-32 h-32 bg-pink-300 rounded-full opacity-50 animate-pulse-slow"></div>
      </div>

      {/* Features Section */}
      <div className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-display font-bold text-gray-900 mb-4">
              Why Kids Love Learning With Us
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Engaging, effective, and designed specifically for young learners
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="card text-center hover:scale-105"
                >
                  <div className="w-16 h-16 bg-gradient-to-br from-pink-400 to-purple-400 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600">{feature.description}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-24 bg-gradient-to-r from-purple-500 to-pink-500">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-display font-bold text-white mb-6">
            Ready to Start the Adventure?
          </h2>
          <p className="text-xl text-white/90 mb-8">
            Join thousands of children learning phonics the fun way!
          </p>
          <Link
            to="/register"
            className="btn-primary text-lg px-8 py-4 bg-white text-purple-600 hover:bg-yellow-100 inline-block"
          >
            Get Started Today
          </Link>
        </div>
      </div>
    </div>
  );
}
