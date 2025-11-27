# Demo Day Presentation Checklist

## Pre-Demo Setup (15 minutes before)

### 1. Environment Check
- [ ] Python 3.11+ installed and working
- [ ] Node.js 18+ installed and working
- [ ] VSCode with Carbonara extension installed and enabled
- [ ] Terminal ready with split panes

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
- [ ] Backend running at http://localhost:8000
- [ ] Visit http://localhost:8000/docs to verify API is working

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
- [ ] Frontend running at http://localhost:5173
- [ ] Open http://localhost:5173 in browser
- [ ] Verify app loads with sample tasks

### 4. VSCode Setup
- [ ] Open project in VSCode: `code /Users/pes/code/demo-day-app`
- [ ] Carbonara extension visible in sidebar
- [ ] Close unnecessary editor tabs for clean demo

## Demo Flow (10-15 minutes)

### Part 1: Introduction (2 min)
**Script**:
> "Today I'm showing you Carbonara, a VSCode extension that helps developers write more sustainable software by detecting performance anti-patterns and analyzing infrastructure carbon emissions."

- [ ] Show the running application in browser
- [ ] Click through tasks, dashboard, analytics
- [ ] Mention: "This looks like a normal task manager, but it's intentionally built with performance issues"

### Part 2: Run Carbonara Analysis (3 min)
**Script**:
> "Let's analyze this project with Carbonara to see what it finds..."

- [ ] Open Carbonara sidebar in VSCode
- [ ] Click "Analyze Project" button
- [ ] While scanning: "Carbonara uses semgrep rules to detect performance anti-patterns and analyzes Terraform configs for carbon intensity"
- [ ] Show progress/loading indicator

### Part 3: Review Findings (5 min)

#### Backend Issues
**Script**:
> "Carbonara found 15+ issues in our Python backend..."

Navigate to each example:

1. **SQL in Loop** (`backend/app/routes/tasks.py:47`)
   - [ ] Show the code
   - [ ] Explain: "Running queries in a loop causes excessive database round-trips"
   - [ ] Show Carbonara's recommendation: "Use IN clause instead"

2. **SELECT * Queries** (`backend/app/routes/tasks.py:29`)
   - [ ] Show the code
   - [ ] Explain: "Fetching all columns wastes network and processing"
   - [ ] Impact: "30-50% unnecessary data transfer"

3. **String Concatenation** (`backend/app/services/report_service.py:16`)
   - [ ] Show the += pattern
   - [ ] Explain: "Each += creates a new string object in memory"
   - [ ] Recommendation: "Use f-strings or join()"

#### Frontend Issues
**Script**:
> "And 8+ issues in our React frontend..."

4. **Multiple DOM Access** (`frontend/src/components/TaskList.jsx:10`)
   - [ ] Show getElementById called 3 times for same element
   - [ ] Explain: "DOM queries are expensive"
   - [ ] Recommendation: "Cache the element reference"

5. **Lodash Imports** (`frontend/src/components/Analytics.jsx:4`)
   - [ ] Show `import _ from 'lodash'`
   - [ ] Explain: "Importing entire library bloats bundle"
   - [ ] Impact: "Could save 50KB+ in bundle size"

6. **CSS Animations** (`frontend/src/components/Dashboard.jsx:38`)
   - [ ] Show transition properties
   - [ ] Explain: "Animations consume GPU power unnecessarily"

#### Infrastructure
**Script**:
> "But the biggest win is in infrastructure..."

7. **High-Carbon Region** (`terraform/main.tf:22`)
   - [ ] Show `region = "us-east-1"`
   - [ ] Explain: "This region runs on ~400 gCO2/kWh"
   - [ ] Show Carbonara's recommendation: "Migrate to eu-north-1"
   - [ ] Impact: **"89% CO2 reduction (45 vs 400 gCO2/kWh)"**
   - [ ] Calculate: "For 1 kWh/day, that's 130kg CO2 saved per year"

### Part 4: Demonstrate a Fix (2 min)
**Script**:
> "Let's fix one of these issues to show how it works..."

Pick the easiest to show (e.g., lodash import):

**Before**:
```javascript
import _ from 'lodash'
```

**After**:
```javascript
import { orderBy, capitalize, map } from 'lodash'
```

- [ ] Make the fix
- [ ] Save the file
- [ ] Re-run Carbonara (or show that issue is resolved)

### Part 5: Summary (1 min)
**Script**:
> "In summary, Carbonara helped us identify:"

- [ ] "**20+ performance issues** across frontend and backend"
- [ ] "**Potential 89% CO2 reduction** from infrastructure optimization"
- [ ] "All **automatically detected** during development"
- [ ] "With **actionable recommendations** for fixes"

**Closing**:
> "Carbonara makes sustainable software development measurable and actionable. It integrates into your existing workflow and helps reduce both energy consumption and cloud costs."

## Backup Talking Points

If there are questions:

### "How does this reduce CO2?"
- Efficient code → Less CPU/memory → Less energy
- Smaller bundles → Less data transfer → Less energy
- Better queries → Less database load → Less energy
- Green regions → Same work, cleaner electricity

### "What's the performance impact?"
- SQL optimization: 50-80% faster queries
- DOM batching: 2-3x fewer reflows
- Bundle optimization: 30-50% smaller downloads
- Overall: 15-30% improvement is typical

### "Can this work on our codebase?"
- Works with JavaScript, TypeScript, Python, Java, C#, PHP, Go, Swift
- 100+ built-in rules (based on Green Code Initiative)
- Analyzes Terraform, CloudFormation, Docker configs
- Free and open source

### "What about the Lambda zip file?"
- It's a placeholder for the demo
- In production, you'd package your actual application
- Terraform just needs the reference to validate

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.11+)
- Recreate venv: `rm -rf venv && python -m venv venv`
- Check port 8000 not in use: `lsof -i :8000`

### Frontend won't start
- Check Node version: `node --version` (need 18+)
- Clear node_modules: `rm -rf node_modules && npm install`
- Check port 5173 not in use: `lsof -i :5173`

### Carbonara not finding issues
- Make sure project is open in VSCode workspace
- Check Carbonara extension is enabled
- Try reloading VSCode window
- Check Carbonara output logs

### Database not initializing
- Delete tasks.db and restart backend
- Database auto-creates on first run
- Check write permissions in backend directory

## Post-Demo

- [ ] Stop servers (Ctrl+C in both terminals)
- [ ] Deactivate Python venv: `deactivate`
- [ ] Thank the audience
- [ ] Share GitHub link (if public)
- [ ] Be available for questions

---

**Good luck with the demo!**
