import sqlite3
from datetime import datetime, timedelta

import os
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'budget.db')

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS payees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            account_number TEXT,
            notes TEXT
        );
        
        CREATE TABLE IF NOT EXISTS bank_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            account_type TEXT NOT NULL,
            institution TEXT,
            account_number_last4 TEXT,
            current_balance REAL DEFAULT 0,
            website TEXT,
            is_active INTEGER DEFAULT 1
        );
        
        CREATE TABLE IF NOT EXISTS credit_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            last_four TEXT,
            credit_limit REAL DEFAULT 0,
            current_balance REAL DEFAULT 0,
            interest_rate REAL DEFAULT 0,
            is_active INTEGER DEFAULT 1
        );
        
        CREATE TABLE IF NOT EXISTS paychecks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pay_date TEXT,
            pay_period_begin TEXT,
            pay_period_end TEXT,
            check_date TEXT,
            check_number TEXT,
            employee_name TEXT,
            employee_id TEXT,
            company TEXT,
            hours_worked REAL DEFAULT 0,
            gross_pay REAL DEFAULT 0,
            pre_tax_deductions REAL DEFAULT 0,
            employee_taxes REAL DEFAULT 0,
            post_tax_deductions REAL DEFAULT 0,
            net_pay REAL DEFAULT 0,
            salary REAL DEFAULT 0,
            biometric_credit REAL DEFAULT 0,
            floating_holiday REAL DEFAULT 0,
            holiday_pay REAL DEFAULT 0,
            vacation_pay REAL DEFAULT 0,
            group_term_life REAL DEFAULT 0,
            spousal_biometric REAL DEFAULT 0,
            other_earnings REAL DEFAULT 0,
            oasdi REAL DEFAULT 0,
            medicare REAL DEFAULT 0,
            federal_tax REAL DEFAULT 0,
            state_tax REAL DEFAULT 0,
            state_name TEXT,
            social_security REAL DEFAULT 0,
            retirement_401k REAL DEFAULT 0,
            add_insurance REAL DEFAULT 0,
            dental_plan REAL DEFAULT 0,
            eye_plan REAL DEFAULT 0,
            health_care_fsa REAL DEFAULT 0,
            health_insurance REAL DEFAULT 0,
            optional_life REAL DEFAULT 0,
            hsa REAL DEFAULT 0,
            loan_repayment REAL DEFAULT 0,
            dependent_life REAL DEFAULT 0,
            stock_purchase REAL DEFAULT 0,
            spousal_life REAL DEFAULT 0,
            employer_match REAL DEFAULT 0,
            federal_filing_status TEXT,
            state_filing_status TEXT,
            bank_name TEXT,
            account_number TEXT,
            deposit_amount REAL DEFAULT 0,
            bank2_name TEXT,
            account2_number TEXT,
            deposit2_amount REAL DEFAULT 0,
            notes TEXT
        );
        
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payee_id INTEGER,
            amount REAL DEFAULT 0,
            due_date TEXT NOT NULL,
            is_paid INTEGER DEFAULT 0,
            paid_date TEXT,
            is_recurring INTEGER DEFAULT 0,
            recurrence_type TEXT,
            notes TEXT,
            FOREIGN KEY (payee_id) REFERENCES payees(id)
        );
        
        CREATE TABLE IF NOT EXISTS budget_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            monthly_limit REAL DEFAULT 0,
            color TEXT DEFAULT '#2E7D32'
        );
    ''')
    
    cursor.execute("PRAGMA table_info(paychecks)")
    existing_cols = [col[1] for col in cursor.fetchall()]
    
    new_columns = {
        'pay_period_begin': 'TEXT',
        'pay_period_end': 'TEXT',
        'check_date': 'TEXT',
        'check_number': 'TEXT',
        'employee_name': 'TEXT',
        'employee_id': 'TEXT',
        'company': 'TEXT',
        'hours_worked': 'REAL DEFAULT 0',
        'pre_tax_deductions': 'REAL DEFAULT 0',
        'employee_taxes': 'REAL DEFAULT 0',
        'post_tax_deductions': 'REAL DEFAULT 0',
        'salary': 'REAL DEFAULT 0',
        'biometric_credit': 'REAL DEFAULT 0',
        'floating_holiday': 'REAL DEFAULT 0',
        'holiday_pay': 'REAL DEFAULT 0',
        'vacation_pay': 'REAL DEFAULT 0',
        'group_term_life': 'REAL DEFAULT 0',
        'spousal_biometric': 'REAL DEFAULT 0',
        'other_earnings': 'REAL DEFAULT 0',
        'oasdi': 'REAL DEFAULT 0',
        'state_name': 'TEXT',
        'add_insurance': 'REAL DEFAULT 0',
        'dental_plan': 'REAL DEFAULT 0',
        'eye_plan': 'REAL DEFAULT 0',
        'health_care_fsa': 'REAL DEFAULT 0',
        'optional_life': 'REAL DEFAULT 0',
        'hsa': 'REAL DEFAULT 0',
        'loan_repayment': 'REAL DEFAULT 0',
        'dependent_life': 'REAL DEFAULT 0',
        'stock_purchase': 'REAL DEFAULT 0',
        'spousal_life': 'REAL DEFAULT 0',
        'employer_match': 'REAL DEFAULT 0',
        'employer_hsa': 'REAL DEFAULT 0',
        'federal_filing_status': 'TEXT',
        'federal_allowances': 'INTEGER DEFAULT 0',
        'dependent_amount': 'REAL DEFAULT 0',
        'additional_withholding': 'REAL DEFAULT 0',
        'state_filing_status': 'TEXT',
        'bank_name': 'TEXT',
        'deposit_amount': 'REAL DEFAULT 0',
        'bank2_name': 'TEXT',
        'account2_number': 'TEXT',
        'deposit2_amount': 'REAL DEFAULT 0',
        'gross_pay_ytd': 'REAL DEFAULT 0',
        'pre_tax_deductions_ytd': 'REAL DEFAULT 0',
        'employee_taxes_ytd': 'REAL DEFAULT 0',
        'post_tax_deductions_ytd': 'REAL DEFAULT 0',
        'net_pay_ytd': 'REAL DEFAULT 0'
    }
    
    for col_name, col_type in new_columns.items():
        if col_name not in existing_cols:
            try:
                cursor.execute(f'ALTER TABLE paychecks ADD COLUMN {col_name} {col_type}')
            except:
                pass
    
    conn.commit()
    conn.close()

def get_all_payees():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM payees ORDER BY name')
    payees = cursor.fetchall()
    conn.close()
    return [dict(row) for row in payees]

def add_payee(name, category, account_number, notes):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO payees (name, category, account_number, notes) VALUES (?, ?, ?, ?)',
                   (name, category, account_number, notes))
    conn.commit()
    conn.close()

def update_payee(id, name, category, account_number, notes, website=''):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE payees SET name=?, category=?, account_number=?, notes=?, website=? WHERE id=?',
                   (name, category, account_number, notes, website, id))
    conn.commit()
    conn.close()

def delete_payee(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM payees WHERE id=?', (id,))
    conn.commit()
    conn.close()

def get_all_bank_accounts():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bank_accounts WHERE is_active=1 ORDER BY name')
    accounts = cursor.fetchall()
    conn.close()
    return [dict(row) for row in accounts]

def add_bank_account(name, account_type, institution, account_number_last4, current_balance, website=''):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO bank_accounts (name, account_type, institution, account_number_last4, current_balance, website) VALUES (?, ?, ?, ?, ?, ?)',
                   (name, account_type, institution, account_number_last4, current_balance, website))
    conn.commit()
    conn.close()

def update_bank_account(id, name, account_type, institution, account_number_last4, current_balance, website=''):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE bank_accounts SET name=?, account_type=?, institution=?, account_number_last4=?, current_balance=?, website=? WHERE id=?',
                   (name, account_type, institution, account_number_last4, current_balance, website, id))
    conn.commit()
    conn.close()

def delete_bank_account(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE bank_accounts SET is_active=0 WHERE id=?', (id,))
    conn.commit()
    conn.close()

def get_all_credit_cards():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM credit_cards WHERE is_active=1 ORDER BY name')
    cards = cursor.fetchall()
    conn.close()
    return [dict(row) for row in cards]

def add_credit_card(name, last_four, credit_limit, current_balance, interest_rate, website=''):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO credit_cards (name, last_four, credit_limit, current_balance, interest_rate, website) VALUES (?, ?, ?, ?, ?, ?)',
                   (name, last_four, credit_limit, current_balance, interest_rate, website))
    conn.commit()
    conn.close()

def update_credit_card(id, name, last_four, credit_limit, current_balance, interest_rate, website=''):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE credit_cards SET name=?, last_four=?, credit_limit=?, current_balance=?, interest_rate=?, website=? WHERE id=?',
                   (name, last_four, credit_limit, current_balance, interest_rate, website, id))
    conn.commit()
    conn.close()

def delete_credit_card(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE credit_cards SET is_active=0 WHERE id=?', (id,))
    conn.commit()
    conn.close()

def get_all_paychecks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM paychecks ORDER BY check_date DESC, pay_date DESC')
    paychecks = cursor.fetchall()
    conn.close()
    return [dict(row) for row in paychecks]

def get_paycheck(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM paychecks WHERE id = ?', (id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_paycheck(id, **kwargs):
    conn = get_db()
    cursor = conn.cursor()
    
    fields = [
        'pay_date', 'pay_period_begin', 'pay_period_end', 'check_date', 'check_number',
        'employee_name', 'employee_id', 'company', 'hours_worked', 'gross_pay',
        'pre_tax_deductions', 'employee_taxes', 'post_tax_deductions', 'net_pay',
        'salary', 'biometric_credit', 'floating_holiday', 'holiday_pay', 'vacation_pay',
        'group_term_life', 'spousal_biometric', 'other_earnings', 'oasdi', 'medicare',
        'federal_tax', 'state_tax', 'state_name', 'social_security', 'retirement_401k',
        'add_insurance', 'dental_plan', 'eye_plan', 'health_care_fsa', 'health_insurance',
        'optional_life', 'hsa', 'loan_repayment', 'dependent_life', 'stock_purchase',
        'spousal_life', 'employer_match', 'employer_hsa', 'federal_filing_status', 'federal_allowances',
        'dependent_amount', 'additional_withholding', 'state_filing_status',
        'bank_name', 'account_number', 'deposit_amount', 'bank2_name', 'account2_number',
        'deposit2_amount', 'gross_pay_ytd', 'pre_tax_deductions_ytd', 'employee_taxes_ytd',
        'post_tax_deductions_ytd', 'net_pay_ytd', 'notes'
    ]
    
    numeric_fields = ['hours_worked', 'gross_pay', 'pre_tax_deductions', 'employee_taxes', 
                      'post_tax_deductions', 'net_pay', 'salary', 'biometric_credit', 
                      'floating_holiday', 'holiday_pay', 'vacation_pay', 'group_term_life', 
                      'spousal_biometric', 'other_earnings', 'oasdi', 'medicare', 'federal_tax', 
                      'state_tax', 'social_security', 'retirement_401k', 'add_insurance', 
                      'dental_plan', 'eye_plan', 'health_care_fsa', 'health_insurance',
                      'optional_life', 'hsa', 'loan_repayment', 'dependent_life', 'stock_purchase',
                      'spousal_life', 'employer_match', 'employer_hsa', 'deposit_amount', 'deposit2_amount']
    
    non_numeric = ['pay_date', 'pay_period_begin', 'pay_period_end', 'check_date', 'check_number',
                   'employee_name', 'employee_id', 'company', 'state_name', 'federal_filing_status',
                   'state_filing_status', 'bank_name', 'account_number', 'bank2_name', 
                   'account2_number', 'notes']
    
    set_clauses = []
    values = []
    for f in fields:
        if f in kwargs:
            val = kwargs[f]
            if f in numeric_fields:
                val = float(val) if val not in [None, ''] else 0
            elif f in non_numeric:
                val = str(val) if val not in [None, ''] else ''
            set_clauses.append(f' {f} = ?')
            values.append(val)
    
    if set_clauses:
        values.append(id)
        cursor.execute(f'UPDATE paychecks SET {",".join(set_clauses)} WHERE id = ?', values)
        conn.commit()
    conn.close()

def add_paycheck(**kwargs):
    conn = get_db()
    cursor = conn.cursor()
    
    fields = [
        'pay_date', 'pay_period_begin', 'pay_period_end', 'check_date', 'check_number',
        'employee_name', 'employee_id', 'company', 'hours_worked', 'gross_pay',
        'pre_tax_deductions', 'employee_taxes', 'post_tax_deductions', 'net_pay',
        'salary', 'biometric_credit', 'floating_holiday', 'holiday_pay', 'vacation_pay',
        'group_term_life', 'spousal_biometric', 'other_earnings', 'oasdi', 'medicare',
        'federal_tax', 'state_tax', 'state_name', 'social_security', 'retirement_401k',
        'add_insurance', 'dental_plan', 'eye_plan', 'health_care_fsa', 'health_insurance',
        'optional_life', 'hsa', 'loan_repayment', 'dependent_life', 'stock_purchase',
        'spousal_life', 'employer_match', 'federal_filing_status', 'federal_allowances',
        'dependent_amount', 'additional_withholding', 'state_filing_status',
        'bank_name', 'account_number', 'deposit_amount', 'bank2_name', 'account2_number',
        'deposit2_amount', 'notes'
    ]
    
    placeholders = ', '.join(['?' for _ in fields])
    columns = ', '.join(fields)
    
    values = [kwargs.get(f, 0 if f not in ['pay_date', 'pay_period_begin', 'pay_period_end', 'check_date', 'check_number', 'employee_name', 'employee_id', 'company', 'state_name', 'federal_filing_status', 'state_filing_status', 'bank_name', 'account_number', 'bank2_name', 'account2_number', 'notes'] else '') for f in fields]
    
    cursor.execute(f'INSERT INTO paychecks ({columns}) VALUES ({placeholders})', values)
    conn.commit()
    conn.close()

def delete_paycheck(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM paychecks WHERE id=?', (id,))
    conn.commit()
    conn.close()

def get_bills_with_payees():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT bills.*, payees.name as payee_name, payees.category as payee_category
        FROM bills
        LEFT JOIN payees ON bills.payee_id = payees.id
        ORDER BY bills.due_date ASC
    ''')
    bills = cursor.fetchall()
    conn.close()
    return [dict(row) for row in bills]

def get_unpaid_bills():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT bills.*, payees.name as payee_name, payees.category as payee_category
        FROM bills
        LEFT JOIN payees ON bills.payee_id = payees.id
        WHERE bills.is_paid = 0
        ORDER BY bills.due_date ASC
    ''')
    bills = cursor.fetchall()
    conn.close()
    return [dict(row) for row in bills]

def add_bill(payee_id, amount, due_date, is_recurring, recurrence_type, notes):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO bills (payee_id, amount, due_date, is_recurring, recurrence_type, notes) VALUES (?, ?, ?, ?, ?, ?)',
                   (payee_id, amount, due_date, is_recurring, recurrence_type, notes))
    conn.commit()
    conn.close()

def update_bill(id, payee_id, amount, due_date, is_recurring, recurrence_type, notes):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE bills SET payee_id=?, amount=?, due_date=?, is_recurring=?, recurrence_type=?, notes=? WHERE id=?',
                   (payee_id, amount, due_date, is_recurring, recurrence_type, notes, id))
    conn.commit()
    conn.close()

def mark_bill_paid(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE bills SET is_paid=1, paid_date=? WHERE id=?', (datetime.now().strftime('%Y-%m-%d'), id))
    conn.commit()
    conn.close()

def mark_bill_unpaid(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE bills SET is_paid=0, paid_date=NULL WHERE id=?', (id,))
    conn.commit()
    conn.close()

def delete_bill(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bills WHERE id=?', (id,))
    conn.commit()
    conn.close()

def get_budget_categories():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM budget_categories ORDER BY name')
    categories = cursor.fetchall()
    conn.close()
    return [dict(row) for row in categories]

def add_budget_category(name, monthly_limit, color):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO budget_categories (name, monthly_limit, color) VALUES (?, ?, ?)',
                   (name, monthly_limit, color))
    conn.commit()
    conn.close()

def update_budget_category(id, name, monthly_limit, color):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE budget_categories SET name=?, monthly_limit=?, color=? WHERE id=?',
                   (name, monthly_limit, color, id))
    conn.commit()
    conn.close()

def delete_budget_category(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM budget_categories WHERE id=?', (id,))
    conn.commit()
    conn.close()

def get_dashboard_stats():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT SUM(current_balance) as total FROM bank_accounts WHERE is_active=1')
    total_bank = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT SUM(current_balance) as total FROM credit_cards WHERE is_active=1')
    total_credit = cursor.fetchone()[0] or 0
    
    cursor.execute('''
        SELECT bills.*, payees.name as payee_name 
        FROM bills 
        LEFT JOIN payees ON bills.payee_id = payees.id 
        WHERE bills.is_paid = 0 
        ORDER BY bills.due_date ASC LIMIT 5
    ''')
    upcoming_bills = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute('SELECT * FROM paychecks ORDER BY check_date DESC LIMIT 1')
    row = cursor.fetchone()
    last_paycheck = dict(row) if row else None
    
    conn.close()
    
    return {
        'total_bank': total_bank,
        'total_credit': total_credit,
        'upcoming_bills': upcoming_bills,
        'last_paycheck': last_paycheck
    }

def get_next_paycheck_date():
    paychecks = get_all_paychecks()
    if not paychecks:
        return None
    for pc in paychecks:
        if pc.get('check_date'):
            last_date = datetime.strptime(pc['check_date'], '%Y-%m-%d')
            break
    else:
        return None
    next_date = last_date + timedelta(days=14)
    while next_date < datetime.now():
        next_date += timedelta(days=14)
    return next_date.strftime('%Y-%m-%d')
