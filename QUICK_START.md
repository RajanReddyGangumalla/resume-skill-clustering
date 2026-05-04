# 🚀 Quick Start Guide - Full Stack Resume Clustering

Get your full-stack resume clustering application running in minutes!

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## ⚡ One-Command Setup

### Option 1: Manual Setup (Recommended)

**Step 1: Start Backend**
```bash
cd backend
../start_backend.sh
```

**Step 2: Start Frontend** (in new terminal)
```bash
cd frontend
../start_frontend.sh
```

### Option 2: Manual Commands

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## 🌐 Access Points

Once running:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## ✅ Verification

1. **Backend Health**: Visit http://localhost:8000/api/health
2. **Frontend**: Open http://localhost:3000 in browser
3. **Test Upload**: Try uploading a resume file

## 🐛 Quick Fixes

**Model not found?**
```bash
python save_model.py
```

**Port already in use?**
```bash
# Kill processes on ports 8000 and 3000
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

**Permission denied?**
```bash
chmod +x start_backend.sh start_frontend.sh
```

## 🎯 First Test

1. Open http://localhost:3000
2. Click "Text Input" tab
3. Paste: "Experienced Python developer with machine learning, React, and AWS skills"
4. Click "Analyze Resume"
5. View your cluster assignment!

## 📞 Need Help?

- Check README_FULLSTACK.md for detailed documentation
- Review troubleshooting section
- Create an issue on GitHub
