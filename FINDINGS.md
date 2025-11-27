# Expected Carbonara Findings

This document lists all intentional anti-patterns in the demo application that Carbonara should detect.

## Python Backend Issues

### Database & SQL (5 issues)

1. **gci4-python-avoid-using-global-variables**
   - **File**: `backend/app/database.py:8`
   - **Issue**: Global variable `db_connection = None`
   - **Impact**: Memory leaks, threading issues
   - **Fix**: Use dependency injection or context managers

2. **gci72-python-avoid-sql-request-in-loop**
   - **File**: `backend/app/routes/tasks.py:47-50`
   - **Issue**: SQL query inside for loop iterating over user_ids
   - **Impact**: N+1 query problem, excessive database round-trips
   - **Fix**: Use `WHERE user_id IN (?)` with parameter list

3. **gci72-python-avoid-sql-request-in-loop**
   - **File**: `backend/app/routes/analytics.py:42-49`
   - **Issue**: Multiple SQL queries in loop for user summaries
   - **Impact**: Database connection overhead
   - **Fix**: Use JOIN or aggregation queries

4. **gci74-python-dont-use-the-query-select-star-from**
   - **File**: `backend/app/routes/tasks.py:29`
   - **Issue**: `SELECT * FROM tasks` without specifying columns
   - **Impact**: Fetching unnecessary data, wasting bandwidth
   - **Fix**: Specify needed columns: `SELECT id, title, status FROM tasks`

5. **gci74-python-dont-use-the-query-select-star-from**
   - **File**: `backend/app/routes/tasks.py:51`
   - **Issue**: Another `SELECT *` in loop
   - **Impact**: Compounded with loop issue
   - **Fix**: Specify columns and remove loop

### Control Flow (2 issues)

6. **gci2-python-avoid-multiple-if-else-statement**
   - **File**: `backend/app/routes/tasks.py:99-107`
   - **Issue**: Multiple if-elif statements for status mapping
   - **Impact**: Poor performance with many conditions
   - **Fix**: Use match-case (Python 3.10+) or dictionary mapping

7. **gci2-python-avoid-multiple-if-else-statement**
   - **File**: `backend/app/routes/analytics.py:92-100`
   - **Issue**: Multiple if-elif for priority labels
   - **Impact**: Cyclomatic complexity
   - **Fix**: Use dictionary mapping or match-case

### String Operations (2 issues)

8. **gci105-python-python-string-concatenation-use-join-instead-or-f-strings-instead-of-plus-equals**
   - **File**: `backend/app/services/report_service.py:16-28`
   - **Issue**: Using `+=` for string concatenation in report generation
   - **Impact**: Creates new string object each time, memory overhead
   - **Fix**: Use f-strings or list with join()

9. **gci105-python-python-string-concatenation-use-join-instead-or-f-strings-instead-of-plus-equals**
   - **File**: `backend/app/services/report_service.py:54-61`
   - **Issue**: More string concatenation in user report
   - **Impact**: Same memory allocation overhead
   - **Fix**: Build list and join, or use f-string

### Collections & Iteration (3 issues)

10. **gci404-python-use-generator-comprehension-instead-of-list-comprehension-in-for-loop-declaration**
    - **File**: `backend/app/services/report_service.py:32`
    - **Issue**: `for task in [t for t in tasks if len(t) > 2]:`
    - **Impact**: Creates full list in memory unnecessarily
    - **Fix**: Use generator: `for task in (t for t in tasks if len(t) > 2):`

11. **gci404-python-use-generator-comprehension-instead-of-list-comprehension-in-for-loop-declaration**
    - **File**: `backend/app/services/report_service.py:48`
    - **Issue**: Another list comprehension in loop
    - **Impact**: Memory allocation for temporary list
    - **Fix**: Use generator expression

12. **gci103-python-dont-use-items-to-iterate-over-a-dictionary-when-only-keys-or-values-are-needed**
    - **File**: `backend/app/routes/analytics.py:24-26`
    - **Issue**: Using `.items()` when only values are needed
    - **Impact**: Unnecessary tuple unpacking
    - **Fix**: Use `.values()` instead

### Object-Oriented (1 issue)

13. **gci7-python-avoid-creating-getter-and-setter-methods-in-classes**
    - **File**: `backend/app/models/task.py:15-45`
    - **Issue**: Using `get_*()` and `set_*()` methods instead of properties
    - **Impact**: Method call overhead, not Pythonic
    - **Fix**: Use `@property` decorator

## JavaScript/React Frontend Issues

### DOM Manipulation (2 issues)

14. **gci11-javascript-multiple-access-of-same-dom-element-should-be-limited**
    - **File**: `frontend/src/components/TaskList.jsx:10-12`
    - **Issue**: `document.getElementById('task-container')` called 4 times
    - **Impact**: DOM query overhead, potential reflows
    - **Fix**: Cache element reference: `const container = document.getElementById(...)`

15. **gci12-javascript-multiple-style-changes-should-be-batched**
    - **File**: `frontend/src/components/TaskList.jsx:25-28`
    - **Issue**: Setting individual style properties (backgroundColor, borderColor, etc.)
    - **Impact**: Multiple layout recalculations
    - **Fix**: Use className or cssText for batching

16. **gci12-javascript-multiple-style-changes-should-be-batched**
    - **File**: `frontend/src/components/Dashboard.jsx:52-54`
    - **Issue**: Multiple style changes in mouse events
    - **Impact**: Rendering overhead
    - **Fix**: Toggle CSS class instead

### CSS Optimizations (3 issues)

17. **gci29-javascript-css-animations-should-be-avoided**
    - **File**: `frontend/src/components/Dashboard.jsx:38-40`
    - **Issue**: CSS transition on stat boxes
    - **Impact**: GPU usage, battery drain on mobile
    - **Fix**: Remove unnecessary animations

18. **gci29-javascript-css-animations-should-be-avoided**
    - **File**: `frontend/src/components/Analytics.jsx:96`
    - **Issue**: Transition on analytics card
    - **Impact**: Constant GPU activity
    - **Fix**: Use static styles

19. **gci26-javascript-shorthand-css-notations-should-be-used-to-reduce-stylesheets-size**
    - **File**: `frontend/src/components/Dashboard.jsx:66-72`
    - **Issue**: Individual margin/padding properties instead of shorthand
    - **Impact**: Larger stylesheet, more parsing
    - **Fix**: Use `margin: 0` and `padding: 15px`

20. **gci26-javascript-shorthand-css-notations-should-be-used-to-reduce-stylesheets-size**
    - **File**: `frontend/src/components/Analytics.jsx:54-60`
    - **Issue**: Non-shorthand CSS properties
    - **Impact**: CSS file size
    - **Fix**: Use shorthand properties

### Import Optimization (3+ issues)

21. **gci9-javascript-importing-everything-from-library-should-be-avoided**
    - **File**: `frontend/src/components/Analytics.jsx:4`
    - **Issue**: `import _ from 'lodash'`
    - **Impact**: Entire lodash library in bundle (~70KB)
    - **Fix**: `import { sum, values, isEmpty, orderBy, first, map, capitalize } from 'lodash'`

22. **gci9-javascript-importing-everything-from-library-should-be-avoided**
    - **File**: `frontend/src/utils/helpers.js:3`
    - **Issue**: `import * as _ from 'lodash'`
    - **Impact**: Full library import
    - **Fix**: Import only needed functions

## Infrastructure Issues

### Cloud Deployment (1 major issue)

23. **High Carbon Intensity Region**
    - **File**: `terraform/main.tf:22`
    - **Issue**: `region = "us-east-1"` (Virginia)
    - **Carbon Intensity**: ~400 gCO2/kWh
    - **Impact**: High carbon emissions from electricity grid
    - **Fix**: Migrate to `eu-north-1` (Stockholm, Sweden)
    - **Optimized Carbon Intensity**: ~45 gCO2/kWh
    - **Reduction**: 89% CO2 reduction
    - **Annual Savings**: ~130 kg CO2 per deployment (at 1 kWh/day)

## Summary Statistics

| Category | Count | Primary Impact |
|----------|-------|----------------|
| Python Backend | 13 | CPU, Memory, Database |
| JavaScript Frontend | 9 | Network, Rendering, Bundle Size |
| Infrastructure | 1 | CO2 Emissions |
| **Total** | **23** | **Energy & Carbon** |

## Estimated Impact After Fixes

### Performance Improvements
- **Database queries**: 50-80% faster
- **Memory usage**: 20-40% reduction
- **Bundle size**: 40-60KB smaller (~30%)
- **Page load**: 15-25% faster
- **CPU usage**: 15-30% reduction

### Carbon Reduction
- **Code optimization**: 15-30% energy reduction
- **Infrastructure**: 89% carbon intensity reduction
- **Combined**: ~90% total carbon footprint reduction

### Cost Savings
- **Database**: Fewer queries = lower RDS costs
- **Lambda**: Less CPU time = lower compute costs
- **Network**: Smaller bundles = lower data transfer
- **Overall**: 20-40% infrastructure cost reduction

---

**Note**: This list is comprehensive for demo purposes. A real application would typically have a subset of these issues, but this demo is designed to showcase Carbonara's full detection capabilities.
