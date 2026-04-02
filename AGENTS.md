# Agent Guidelines for Budget Tracker

## Project Overview

This is a Flask-based personal finance management application for tracking budgets, bills, paychecks, payees, bank accounts, and credit cards. The app uses SQLite for data storage, Jinja2 templates for rendering, and Bootstrap 5 for the UI.

## Build & Run Commands

### Installation
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
python app.py
```

### Testing
- No formal test framework is currently configured
- Manual testing via browser at http://localhost:5000
- If adding tests, use pytest and place in `tests/` directory

## Code Style Guidelines

### Python (app.py, database.py)

#### Imports
- Standard library imports first, then third-party
- Group imports by: stdlib → third-party → local
- Example:
```python
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
import re
from dateutil import parser as date_parser
import database as db
```

#### Naming Conventions
- Functions: `snake_case` (e.g., `get_all_paychecks`, `add_payee`)
- Variables: `snake_case` (e.g., `current_balance`, `pay_period_begin`)
- Constants: `SCREAMING_SNAKE_CASE` (e.g., `DATABASE`)
- Classes: Not currently used, but if added: `PascalCase`
- Route handlers: `snake_case` (e.g., `add_paycheck`, `update_bill`)

#### Flask Routes
- Use `@app.route()` decorator with explicit HTTP methods
- Use type hints in route parameters: `@app.route('/delete_paycheck/<int:id>')`
- Return `redirect(url_for('endpoint'))` for successful POSTs
- Use `flash()` for user feedback messages with categories: `'success'`, `'info'`, `'warning'`, `'danger'`

#### Error Handling
- Return JSON with error messages for API endpoints: `return jsonify({'error': 'message'}), 404`
- Use try/except blocks for PDF parsing and database operations
- Silent failures acceptable for non-critical operations (e.g., column already exists)

#### Database (database.py)
- Use `sqlite3.connect()` with context manager pattern where possible
- Set `row_factory = sqlite3.Row` for dict-like access
- Always close connections after use
- Use parameterized queries to prevent SQL injection
- Numeric fields should default to 0, text fields to empty string
- Soft deletes preferred (use `is_active` flag) over hard deletes

#### Date Handling
- Store dates as ISO format strings: `'YYYY-MM-DD'`
- Use `datetime.strptime()` and `datetime.strftime()` for parsing/formatting
- Use `timedelta` for date calculations (e.g., biweekly paychecks)

### HTML Templates (Jinja2)

#### Structure
- Extend `base.html` for consistent layout
- Use Bootstrap 5 classes for styling
- Define `{% block title %}` and `{% block content %}` blocks

#### Variables
- Use `url_for('function_name')` for all URLs
- Access flashed messages with `get_flashed_messages()`
- Pass data via render_template kwargs

#### Filters
- Use Jinja2 built-in filters: `|safe`, `|truncate`, `|datetime`

### CSS (style.css)

#### Variables
- Define colors in `:root` at top of file
- Use hex colors for brand palette
- Example:
```css
:root {
    --primary: #2E7D32;
    --secondary: #1565C0;
    --danger: #D32F2F;
}
```

#### Selectors
- Use class-based selectors, avoid `!important`
- BEM-lite naming: `.component-name`, `.component-name__element`
- Use hyphenated names: `.stat-card`, `.account-card`

#### Responsive Design
- Mobile-first approach with `min-width` media queries
- Breakpoints: 576px, 768px, 992px, 1200px, 1400px, 1920px
- Test at all breakpoints before committing

### JavaScript (app.js)

#### Pattern
- Vanilla JS only (no frameworks)
- Wrap in `DOMContentLoaded` event listener
- Use `document.addEventListener('DOMContentLoaded', function() { ... })`

#### Functions
- PascalCase for function names: `formatCurrency()`, `calculateNetPay()`
- Event handlers on individual elements with arrow functions when simple
- Use `querySelectorAll` with `forEach` for multiple elements

#### Best Practices
- Use `Intl.NumberFormat` for currency formatting
- Always check element existence before manipulating (`if (element)`)
- Use `confirm()` for delete confirmations

## Project Structure

```
budget_app/
├── app.py              # Main Flask application, routes, and PDF parsing
├── database.py         # SQLite database operations
├── requirements.txt    # Python dependencies
├── templates/          # Jinja2 HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── paychecks.html
│   ├── bills.html
│   ├── payees.html
│   ├── bank_accounts.html
│   ├── credit_cards.html
│   ├── budget.html
│   └── paystub_template.html
├── static/
│   ├── css/style.css
│   └── js/app.js
└── DATA/budget_app/budget.db  # SQLite database location
```

## Key Technical Details

### Database Path
- Configured in `database.py`: `DATABASE = '/DATA/budget_app/budget.db'`
- This is a Linux path; Windows users may need to modify

### Paycheck Data Model
- Contains 50+ fields for detailed payroll tracking
- Supports multiple bank deposits per paycheck
- Tracks pre-tax and post-tax deductions separately

### PDF Parsing
- Uses three libraries as fallbacks: pdfplumber, PyMuPDF, PyPDF2
- Extracts data via regex pattern matching
- Supports paystub text import from NCR Voyix Corporation

### API Endpoints
- `GET /api/payslip/<id>` - Returns paycheck JSON
- `GET /api/dashboard_stats` - Returns dashboard statistics

## Development Notes

### Adding New Features
1. Add database functions in `database.py`
2. Add route handlers in `app.py`
3. Create or extend templates
4. Add any needed CSS in `style.css`
5. Add any needed JS in `app.js`

### Adding Database Columns
- Use `ALTER TABLE` in `init_db()` with `IF NOT EXISTS` pattern
- Handle migration gracefully (try/except)

### Bootstrap Components
- Use Bootstrap 5.3.2 from CDN
- Icons from Bootstrap Icons 1.11.1
- Use card-based layouts with shadows
- Flash messages use Bootstrap alert classes
