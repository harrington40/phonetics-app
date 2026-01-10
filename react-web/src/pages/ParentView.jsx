import { Users } from 'lucide-react';

export default function ParentView() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-24 md:pb-8">
      <h1 className="text-3xl font-display font-bold text-gray-900 mb-6">
        Parent Dashboard
      </h1>
      
      <div className="card">
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-400 to-indigo-400 rounded-xl flex items-center justify-center">
            <Users className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900">Monitor Learning</h2>
            <p className="text-gray-600">Track your child's progress</p>
          </div>
        </div>

        <div className="text-center py-12">
          <p className="text-gray-600">
            Parent dashboard features coming soon!
          </p>
        </div>
      </div>
    </div>
  );
}
