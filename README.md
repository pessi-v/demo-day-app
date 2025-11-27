# Task Manager - Carbonara Demo Application

A full-stack web application intentionally built with performance and sustainability anti-patterns to demonstrate the capabilities of the **Carbonara** VSCode extension - a tool for analyzing and reducing CO2 emissions in software projects.

## Purpose

This demo application showcases how Carbonara can:

- Detect performance anti-patterns in frontend (JavaScript/React) and backend (Python) code
- Identify inefficient database queries and operations
- Analyze cloud infrastructure deployments for carbon optimization
- Provide actionable recommendations to reduce software carbon footprint

## Architecture

- **Frontend**: React 18 + Vite (JavaScript)
- **Backend**: FastAPI (Python 3.11+)
- **Database**: SQLite (local dev) / PostgreSQL (production)
- **Infrastructure**: AWS Lambda + RDS (configured for us-east-1)

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- VSCode with Carbonara extension installed

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

The app will be available at `http://localhost:5173`

### 3. Access the Application

Open your browser to `http://localhost:5173` and you should see:

- A dashboard with task statistics
- A task list with sample data
- Analytics showing user summaries

## Running Carbonara Analysis

### Step 1: Open in VSCode

```bash
code /Users/pes/code/demo-day-app
```

### Step 2: Run Carbonara

1. Open the Carbonara extension sidebar
2. Click "Analyze Project"
3. Wait for the analysis to complete

### Step 3: Review Findings

Carbonara should detect approximately **20+ issues**:

#### Backend Issues (~15 findings)

- ✗ SQL queries without LIMIT clauses
- ✗ Database queries inside loops
- ✗ String concatenation with +=
- ✗ Multiple if-elif statements
- ✗ List comprehensions in loops
- ✗ Using .items() when only values needed
- ✗ Global variables
- ✗ Getter/setter methods instead of properties

#### Frontend Issues (~8 findings)

- ✗ Multiple accesses to same DOM elements
- ✗ Unbatched style changes
- ✗ Unnecessary CSS animations
- ✗ Non-shorthand CSS properties
- ✗ Importing entire lodash library

#### Infrastructure Issues (~1 finding)

- ✗ High-carbon AWS region (us-east-1)
- → Recommended: eu-north-1 for 89% CO2 reduction

## Infrastructure Optimization

Migrating from us-east-1 to eu-north-1:

- **Current**: 400 gCO2/kWh
- **Optimized**: 45 gCO2/kWh
- **Reduction**: 89%

## Project Structure

```
demo-day-app/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── tasks.py          # Task CRUD operations
│   │   │   └── analytics.py      # Analytics endpoints
│   │   ├── models/
│   │   │   └── task.py           # Task model with getters/setters
│   │   ├── services/
│   │   │   └── report_service.py # Report generation
│   │   ├── database.py           # Database setup
│   │   └── main.py               # FastAPI app
│   ├── requirements.txt
│   └── tasks.db                  # SQLite database (auto-generated)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── TaskList.jsx      # Task list with DOM issues
│   │   │   ├── Dashboard.jsx     # Stats with CSS issues
│   │   │   └── Analytics.jsx     # Analytics with lodash
│   │   ├── utils/
│   │   │   └── helpers.js        # Utility functions
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
│
├── terraform/
│   ├── main.tf                   # AWS infrastructure (high-carbon)
│   └── README.md
│
└── README.md                      # This file
```

## Intentional Anti-Patterns

This application is deliberately written with anti-patterns that Carbonara will detect:

### Python Backend (15+ Issues)

| Rule ID | Anti-Pattern                          | Location                         | Impact                     |
| ------- | ------------------------------------- | -------------------------------- | -------------------------- |
| gci4    | Global variables                      | `database.py:8`                  | Memory leaks               |
| gci72   | SQL queries in loops                  | `tasks.py:47`, `analytics.py:42` | Database overhead          |
| gci74   | SELECT \* queries                     | `tasks.py:29`, `tasks.py:51`     | Unnecessary data transfer  |
| gci2    | Multiple if-else chains               | `tasks.py:99`, `analytics.py:92` | CPU overhead               |
| gci105  | String concatenation with +=          | `report_service.py:16-40`        | Memory allocation overhead |
| gci404  | List comprehension in loops           | `report_service.py:32`           | Unnecessary memory usage   |
| gci103  | Dict .items() when only values needed | `analytics.py:24`                | Iterator overhead          |
| gci7    | Getter/setter methods                 | `models/task.py:15-45`           | Method call overhead       |

### JavaScript Frontend (8+ Issues)

| Rule ID | Anti-Pattern                 | Location                                     | Impact              |
| ------- | ---------------------------- | -------------------------------------------- | ------------------- |
| gci11   | Multiple DOM element access  | `TaskList.jsx:10-12`                         | DOM reflow overhead |
| gci12   | Multiple style changes       | `TaskList.jsx:25-28`, `Dashboard.jsx:52-54`  | Rendering overhead  |
| gci29   | CSS animations/transitions   | `Dashboard.jsx:38-40`, `Analytics.jsx:96`    | GPU usage           |
| gci26   | Non-shorthand CSS properties | `Dashboard.jsx:66-72`, `Analytics.jsx:54-60` | Stylesheet size     |
| gci9    | Full library imports         | `Analytics.jsx:4`, `helpers.js:3`            | Bundle size         |

### Infrastructure (1 Issue)

| Issue              | Description             | Location               | Impact                       |
| ------------------ | ----------------------- | ---------------------- | ---------------------------- |
| High-carbon region | Deployment to us-east-1 | `terraform/main.tf:22` | ~400 gCO2/kWh                |
| **Recommendation** | Migrate to eu-north-1   |                        | ~45 gCO2/kWh (89% reduction) |

## License

MIT License - This is a demo application for educational purposes.

## Related Links

- [Carbonara VSCode Extension](#) - Your link here
- [Green Software Foundation](https://greensoftware.foundation/)
- [Website Carbon Calculator](https://www.websitecarbon.com/)
- [Electricity Maps](https://app.electricitymaps.com/)
