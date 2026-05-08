import React from 'react';
import './index.css';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            Resume Skill Clustering
          </h1>
          <p className="text-xl text-purple-200">
            Upload your resume to see how you compare with other students
          </p>
        </div>
        
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-purple-500/20">
          <div className="text-center">
            <h2 className="text-2xl font-semibold text-white mb-4">
              🚀 App is Deployed Successfully!
            </h2>
            <p className="text-purple-200">
              Your Resume Clustering application is now live on Vercel.
            </p>
            <div className="mt-6">
              <div className="bg-green-500/20 border border-green-500/50 rounded-lg p-4">
                <p className="text-green-400 font-medium">
                  ✅ Frontend deployed successfully
                </p>
                <p className="text-green-400">
                  Next step: Deploy backend to complete full functionality
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
