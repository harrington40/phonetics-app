import { Link } from 'react-router-dom';

export default function Practice() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-24 md:pb-8">
      <h1 className="text-3xl font-display font-bold text-gray-900 mb-6">
        Practice
      </h1>
      <div className="card text-center py-12">
        <p className="text-xl text-gray-600 mb-4">
          Practice features coming soon!
        </p>
        <Link to="/dashboard" className="btn-secondary inline-block">
          Back to Dashboard
        </Link>
      </div>
    </div>
  );
}
