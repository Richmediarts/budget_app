# Budget Tracker

A web-based personal finance management application for tracking budgets, bills, paychecks, payees, bank accounts, and credit cards.

## Features

- **Dashboard** - Overview of your financial status
- **Paychecks** - Track biweekly paychecks with a visual paystub display
- **Bills** - Manage bills with due date tracking and payment status
- **Payees** - Store and manage payee information
- **Bank Accounts** - Track multiple bank accounts and balances
- **Credit Cards** - Monitor credit card debt and utilization
- **Budget** - Set monthly budget limits per category

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and go to:
```
http://localhost:5000
```

## Accessing Remotely

To access from other devices on your network:

1. Run the app with:
```bash
python app.py
```

2. Find your server's IP address:
```bash
hostname -I
```

3. Access from any device using:
```
http://<your-server-ip>:5000
```

## Data Storage

All data is stored in SQLite database at:
```
/DATA/budget_app/budget.db
```

## Screenshots

The app features a clean, modern interface with:
- Dark sidebar navigation
- Card-based layout
- Color-coded status indicators
- Responsive design for mobile/desktop
