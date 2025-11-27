# Quick Start Guide

Get the demo app running in under 5 minutes.

## Prerequisites

- Python 3.11+
- Node.js 18+
- VSCode with Carbonara extension

## Setup (First Time Only)

### Terminal 1 - Backend

```bash
cd /Users/pes/code/demo-day-app/backend

# Create virtual environment
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload --port 8000
```

### Terminal 2 - Frontend

```bash
cd /Users/pes/code/demo-day-app/frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

## Verify

1. **Backend**: Visit http://localhost:8000/docs
   - Should see FastAPI documentation

2. **Frontend**: Visit http://localhost:5173
   - Should see Task Manager app with sample data

## Run Carbonara

1. Open in VSCode:
   ```bash
   code /Users/pes/code/demo-day-app
   ```

2. Open Carbonara sidebar
3. Click "Analyze Project"
4. Wait for results (~20-30 seconds)

## Expected Results

Carbonara should detect:
- **~13 Python backend issues** (SQL, strings, loops)
- **~9 JavaScript frontend issues** (DOM, CSS, imports)
- **1 infrastructure issue** (high-carbon AWS region)

## Next Steps

- Read `README.md` for full documentation
- Check `DEMO_CHECKLIST.md` for presentation guide
- Review `FINDINGS.md` for detailed issue list

## Troubleshooting

**Backend won't start?**
- Check Python version: `python --version`
- Try: `pip install --upgrade pip`
- Delete venv and recreate

**Frontend won't start?**
- Check Node version: `node --version`
- Try: `rm -rf node_modules && npm install`
- Check if port 5173 is free

**Database error?**
- Delete `backend/tasks.db` if it exists
- Restart backend (database auto-creates)

## Stopping the Servers

Press `Ctrl+C` in each terminal to stop the servers.

---

Ready for demo day!
