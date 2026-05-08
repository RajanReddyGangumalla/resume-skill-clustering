import React from 'react';

function App() {
  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #1e293b 0%, #7c3aed 50%, #1e293b 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      <div style={{
        backgroundColor: 'rgba(30, 41, 59, 0.8)',
        backdropFilter: 'blur(10px)',
        borderRadius: '20px',
        padding: '40px',
        textAlign: 'center',
        border: '1px solid rgba(124, 58, 237, 0.2)',
        maxWidth: '600px'
      }}>
        <h1 style={{
          fontSize: '3rem',
          fontWeight: 'bold',
          color: 'white',
          marginBottom: '20px'
        }}>
          Resume Skill Clustering
        </h1>
        <p style={{
          fontSize: '1.2rem',
          color: '#e9d5ff',
          marginBottom: '30px'
        }}>
          🚀 Successfully Deployed to Vercel!
        </p>
        <div style={{
          backgroundColor: 'rgba(34, 197, 94, 0.2)',
          border: '1px solid rgba(34, 197, 94, 0.5)',
          borderRadius: '10px',
          padding: '20px',
          marginBottom: '20px'
        }}>
          <p style={{
            color: '#4ade80',
            fontWeight: 'bold',
            margin: '0'
          }}>
            ✅ Frontend Deployment Complete
          </p>
          <p style={{
            color: '#4ade80',
            margin: '10px 0 0 0'
          }}>
            Your React app is now live on Vercel
          </p>
        </div>
        <p style={{
          color: '#a78bfa',
          fontSize: '0.9rem'
        }}>
          Next: Deploy backend to complete full functionality
        </p>
      </div>
    </div>
  );
}

export default App;
