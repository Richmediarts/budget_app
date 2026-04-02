# Budget App Specification

## 1. Project Overview

**Project Name:** Budget Tracker  
**Type:** Web-based Financial Management Application  
**Core Functionality:** A comprehensive budget management system that tracks monthly budgets, bills, paychecks (biweekly), payees, bank accounts, and credit cards with a GUI paystub display.  
**Target Users:** Individuals managing personal finances who need cross-platform access via web browser.

## 2. Technology Stack

- **Backend:** Python 3.x with Flask
- **Database:** SQLite (simple, serverless, portable)
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Access:** Any web browser (desktop, mobile, tablet)

## 3. Data Models

### 3.1 Payees
- `id` (primary key)
- `name` (string)
- `category` (string: utilities, rent, subscriptions, insurance, etc.)
- `account_number` (string, optional)
- `notes` (text, optional)

### 3.2 Bank Accounts
- `id` (primary key)
- `name` (string: checking, savings, etc.)
- `account_type` (string: checking, savings, investment)
- `institution` (string: bank name)
- `account_number_last4` (string)
- `current_balance` (decimal)
- `is_active` (boolean)

### 3.3 Credit Cards
- `id` (primary key)
- `name` (string)
- `last_four` (string)
- `credit_limit` (decimal)
- `current_balance` (decimal)
- `interest_rate` (decimal)
- `is_active` (boolean)

### 3.4 Paychecks
- `id` (primary key)
- `pay_date` (date)
- `gross_pay` (decimal)
- `federal_tax` (decimal)
- `state_tax` (decimal)
- `social_security` (decimal)
- `medicare` (decimal)
- `health_insurance` (decimal)
- `retirement_401k` (decimal)
- `other_deductions` (decimal)
- `net_pay` (decimal, auto-calculated)
- `notes` (text, optional)

### 3.5 Bills
- `id` (primary key)
- `payee_id` (foreign key)
- `amount` (decimal)
- `due_date` (date)
- `is_paid` (boolean)
- `paid_date` (date, nullable)
- `is_recurring` (boolean)
- `recurrence_type` (string: weekly, biweekly, monthly, yearly, optional)
- `notes` (text, optional)

### 3.6 Budget Categories
- `id` (primary key)
- `name` (string)
- `monthly_limit` (decimal)
- `color` (string: hex color for UI)

## 4. UI/UX Design

### 4.1 Layout Structure
- **Sidebar Navigation:** Fixed left sidebar with main sections
- **Main Content Area:** Dynamic content based on selected section
- **Header:** Shows current month/year and quick stats

### 4.2 Color Scheme
- Primary: #2E7D32 (green - money theme)
- Secondary: #1565C0 (blue)
- Background: #F5F5F5 (light gray)
- Cards: #FFFFFF (white)
- Text: #212121 (dark gray)
- Danger: #D32F2F (red for overdue)
- Warning: #F57C00 (orange for upcoming)

### 4.3 Navigation Sections
1. **Dashboard** - Overview of all accounts and upcoming bills
2. **Paychecks** - Biweekly paycheck entry with paystub GUI
3. **Bills** - Bills to be paid list
4. **Payees** - Manage payees/vendors
5. **Bank Accounts** - Bank account balances
6. **Credit Cards** - Credit card balances
7. **Budget** - Monthly budget categories

## 5. Functional Requirements

### 5.1 Dashboard
- Total bank balance across all accounts
- Total credit card debt
- Next upcoming bill with days until due
- Next paycheck date and amount
- Bills due this week highlighted

### 5.2 Paycheck Section (Paystub GUI)
- Form to enter paycheck details
- Visual paystub display showing:
  - Employee info section
  - Earnings breakdown (gross, regular, overtime)
  - Deductions breakdown (federal, state, SS, Medicare, insurance, 401k)
  - Net pay prominently displayed
- Paycheck history list
- Upcoming paycheck calculator (biweekly schedule)

### 5.3 Bills Section
- List of all bills with:
  - Payee name
  - Amount due
  - Due date
  - Status (paid/unpaid/overdue)
  - Days until due
- Filter by: all, unpaid, paid, overdue
- Mark as paid functionality
- Add/edit bill forms

### 5.4 Payees Management
- CRUD operations for payees
- Search functionality
- Category grouping

### 5.5 Bank Accounts
- List all bank accounts
- Add/edit account forms
- Current balance display

### 5.6 Credit Cards
- List all credit cards
- Credit utilization percentage
- Add/edit card forms
- Due date and minimum payment display

### 5.7 Budget Categories
- Monthly budget limits per category
- Visual progress bars
- Spending vs. limit comparison

## 6. Features

### 6.1 Bill Payment Tracking
- Bills automatically roll to next period when paid
- Alerts for overdue bills (visual highlighting)
- Payment history tracking

### 6.2 Paycheck Integration
- Auto-calculate net pay from gross
- Biweekly paycheck schedule generation
- Budget alignment based on biweekly income

### 6.3 Data Persistence
- All data stored in SQLite database
- Automatic database initialization on first run

## 7. Acceptance Criteria

1. User can add, edit, and delete payees
2. User can add, edit, and delete bank accounts with balances
3. User can add, edit, and delete credit cards with balances
4. User can enter biweekly paychecks with full deduction breakdown
5. Paystub displays in professional GUI format
6. User can add, edit, and mark bills as paid
7. Bills show days until due with overdue highlighting
8. Dashboard shows financial overview
9. All data persists in SQLite database
10. Application accessible via web browser on any platform
11. Responsive design works on mobile and desktop
