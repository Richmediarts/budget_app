from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
import database as db

app = Flask(__name__)
app.secret_key = 'budget-app-secret-key-2024'

db.init_db()

@app.context_processor
def inject_globals():
    return {
        'current_date': datetime.now().strftime('%B %d, %Y'),
        'datetime': datetime,
        'total_balance': sum(a['current_balance'] for a in db.get_all_bank_accounts()),
        'total_debt': sum(c['current_balance'] for c in db.get_all_credit_cards()),
        'total_budget': sum(c['monthly_limit'] for c in db.get_budget_categories()),
        'next_paycheck_date': db.get_next_paycheck_date()
    }

@app.route('/')
def dashboard():
    stats = db.get_dashboard_stats()
    return render_template('dashboard.html', stats=stats, next_paycheck_date=db.get_next_paycheck_date())

@app.route('/paychecks')
def paychecks():
    paychecks = db.get_all_paychecks()
    next_paycheck = db.get_next_paycheck_date()
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('paychecks.html', paychecks=paychecks, next_paycheck=next_paycheck, today=today, active_tab='history')

@app.route('/api/payslip/<int:paycheck_id>')
def get_payslip(paycheck_id):
    paychecks = db.get_all_paychecks()
    pc = next((p for p in paychecks if p['id'] == paycheck_id), None)
    if pc:
        return jsonify(pc)
    return jsonify({'error': 'Paycheck not found'}), 404

@app.route('/add_paycheck', methods=['POST'])
def add_paycheck():
    db.add_paycheck(
        pay_date=request.form.get('check_date', ''),
        pay_period_begin=request.form.get('pay_period_begin', ''),
        pay_period_end=request.form.get('pay_period_end', ''),
        check_date=request.form.get('check_date', ''),
        check_number=request.form.get('check_number', ''),
        employee_name=request.form.get('employee_name', ''),
        employee_id=request.form.get('employee_id', ''),
        company=request.form.get('company', ''),
        hours_worked=float(request.form.get('hours_worked') or 0),
        gross_pay=float(request.form.get('gross_pay') or 0),
        pre_tax_deductions=float(request.form.get('pre_tax_deductions') or 0),
        employee_taxes=float(request.form.get('employee_taxes') or 0),
        post_tax_deductions=float(request.form.get('post_tax_deductions') or 0),
        net_pay=float(request.form.get('net_pay') or 0),
        salary=float(request.form.get('salary') or 0),
        biometric_credit=float(request.form.get('biometric_credit') or 0),
        floating_holiday=float(request.form.get('floating_holiday') or 0),
        holiday_pay=float(request.form.get('holiday_pay') or 0),
        vacation_pay=float(request.form.get('vacation_pay') or 0),
        group_term_life=float(request.form.get('group_term_life') or 0),
        spousal_biometric=float(request.form.get('spousal_biometric') or 0),
        other_earnings=float(request.form.get('other_earnings') or 0),
        oasdi=float(request.form.get('oasdi') or 0),
        medicare=float(request.form.get('medicare') or 0),
        federal_tax=float(request.form.get('federal_tax') or 0),
        state_tax=float(request.form.get('state_tax') or 0),
        state_name=request.form.get('state_name', ''),
        social_security=float(request.form.get('social_security') or 0),
        retirement_401k=float(request.form.get('retirement_401k') or 0),
        add_insurance=float(request.form.get('add_insurance') or 0),
        dental_plan=float(request.form.get('dental_plan') or 0),
        eye_plan=float(request.form.get('eye_plan') or 0),
        health_care_fsa=float(request.form.get('health_care_fsa') or 0),
        health_insurance=float(request.form.get('health_insurance') or 0),
        optional_life=float(request.form.get('optional_life') or 0),
        hsa=float(request.form.get('hsa') or 0),
        loan_repayment=float(request.form.get('loan_repayment') or 0),
        dependent_life=float(request.form.get('dependent_life') or 0),
        stock_purchase=float(request.form.get('stock_purchase') or 0),
        spousal_life=float(request.form.get('spousal_life') or 0),
        employer_match=float(request.form.get('employer_match') or 0),
        federal_filing_status=request.form.get('federal_filing_status', ''),
        state_filing_status=request.form.get('state_filing_status', ''),
        bank_name=request.form.get('bank_name', ''),
        account_number=request.form.get('account_number', ''),
        deposit_amount=float(request.form.get('deposit_amount') or 0),
        bank2_name=request.form.get('bank2_name', ''),
        account2_number=request.form.get('account2_number', ''),
        deposit2_amount=float(request.form.get('deposit2_amount') or 0),
        notes=request.form.get('notes', '')
    )
    flash('Paycheck added successfully!', 'success')
    return redirect(url_for('paychecks'))

@app.route('/delete_paycheck/<int:id>')
def delete_paycheck(id):
    db.delete_paycheck(id)
    flash('Paycheck deleted.', 'info')
    return redirect(url_for('paychecks'))

@app.route('/edit_paycheck/<int:id>')
def edit_paycheck(id):
    paycheck = db.get_paycheck(id)
    if not paycheck:
        flash('Paycheck not found.', 'danger')
        return redirect(url_for('paychecks'))
    paychecks = db.get_all_paychecks()
    next_paycheck = db.get_next_paycheck_date()
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('paychecks.html', paychecks=paychecks, next_paycheck=next_paycheck, today=today, edit_paycheck=paycheck, active_tab='history')

@app.route('/update_paycheck/<int:id>', methods=['POST'])
def update_paycheck(id):
    numeric_fields = ['hours_worked', 'gross_pay', 'net_pay', 'pre_tax_deductions', 'employee_taxes', 
                      'post_tax_deductions', 'salary', 'biometric_credit', 'floating_holiday', 
                      'holiday_pay', 'vacation_pay', 'group_term_life', 'spousal_biometric',
                      'oasdi', 'medicare', 'federal_tax', 'state_tax', 'social_security',
                      'retirement_401k', 'add_insurance', 'dental_plan', 'eye_plan', 
                      'health_care_fsa', 'health_insurance', 'optional_life', 'hsa',
                      'loan_repayment', 'dependent_life', 'stock_purchase', 'spousal_life',
                      'employer_match', 'deposit_amount', 'deposit2_amount']
    
    kwargs = {'id': id}
    for field in numeric_fields:
        val = request.form.get(field, '0').replace(',', '')
        kwargs[field] = float(val) if val else 0
    
    kwargs['pay_date'] = request.form.get('check_date', '')
    kwargs['pay_period_begin'] = request.form.get('pay_period_begin', '')
    kwargs['pay_period_end'] = request.form.get('pay_period_end', '')
    kwargs['check_date'] = request.form.get('check_date', '')
    kwargs['check_number'] = request.form.get('check_number', '')
    kwargs['employee_name'] = request.form.get('employee_name', '')
    kwargs['employee_id'] = request.form.get('employee_id', '')
    kwargs['company'] = request.form.get('company', '')
    kwargs['state_name'] = request.form.get('state_name', '')
    kwargs['federal_filing_status'] = request.form.get('federal_filing_status', '')
    kwargs['state_filing_status'] = request.form.get('state_filing_status', '')
    kwargs['bank_name'] = request.form.get('bank_name', '')
    kwargs['account_number'] = request.form.get('account_number', '')
    kwargs['bank2_name'] = request.form.get('bank2_name', '')
    kwargs['account2_number'] = request.form.get('account2_number', '')
    kwargs['notes'] = request.form.get('notes', '')
    
    db.update_paycheck(id, **kwargs)
    flash('Paycheck updated successfully!', 'success')
    return redirect(url_for('paychecks'))

import re
from dateutil import parser as date_parser

def parse_paycheck_text(raw_text):
    result = {}
    lines = raw_text.strip().split('\n')
    text = raw_text
    
    def extract_money(s):
        s = s.strip().replace('$', '').replace(',', '')
        try:
            return float(s)
        except:
            return None
    
    def parse_date(s):
        s = s.strip()
        for fmt in ['%m/%d/%Y', '%Y-%m-%d', '%m-%d-%Y', '%B %d, %Y']:
            try:
                return datetime.strptime(s, fmt).strftime('%Y-%m-%d')
            except:
                pass
        try:
            return date_parser.parse(s).strftime('%Y-%m-%d')
        except:
            return None
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        if 'voyix' in line_lower:
            result['company'] = 'NCR Voyix Corporation'
        
        emp_id = re.search(r'\b(\d{10,11})\b', line)
        if emp_id and 'employee_id' not in result:
            result['employee_id'] = emp_id.group(1)
        
        dates = re.findall(r'(\d{2}/\d{2}/\d{4})', line)
        if len(dates) >= 2:
            begin_date = parse_date(dates[0])
            end_date = parse_date(dates[1])
            if begin_date and 'pay_period_begin' not in result:
                result['pay_period_begin'] = begin_date
            if end_date and 'pay_period_end' not in result:
                result['pay_period_end'] = end_date
        
        if len(dates) >= 3 and 'check_date' not in result:
            cd = parse_date(dates[2])
            if cd:
                result['check_date'] = cd
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        words = line.split()
        
        if 'richard' in line_lower or 'johnson' in line_lower:
            for word in words:
                if word[0].isupper() and len(word) > 2 and not any(c.isdigit() for c in word):
                    if 'voyix' not in word.lower() and 'corporation' not in word.lower() and word not in ['Name', 'Company', 'Employee', 'Description', 'Amount', 'Current', 'YTD', 'Hours', 'Gross', 'Tax', 'Net']:
                        result['employee_name'] = line.strip()
                        break
            if 'employee_name' in result:
                break
    
    summary_line = None
    for line in lines:
        line_lower = line.lower()
        if 'current' in line_lower and re.search(r'\b\d{2}\.\d{2}\b', line) and not line_lower.strip().startswith('hours worked'):
            money_matches = re.findall(r'([\d,]+\.\d{2})', line)
            if len(money_matches) >= 5:
                summary_line = line
                break
    
    if summary_line:
        money_matches = re.findall(r'([\d,]+\.\d{2})', summary_line)
        if len(money_matches) >= 6:
            result['hours_worked'] = extract_money(money_matches[0])
            result['gross_pay'] = extract_money(money_matches[1])
            result['pre_tax_deductions'] = extract_money(money_matches[2])
            result['employee_taxes'] = extract_money(money_matches[3])
            result['post_tax_deductions'] = extract_money(money_matches[4])
            result['net_pay'] = extract_money(money_matches[5])
    
    def get_value_after_label(line, label, default=None):
        idx = line.lower().find(label)
        if idx == -1:
            return default
        after_label = line[idx + len(label):]
        match = re.search(r'([\d,]+\.\d{2})', after_label)
        if match:
            return extract_money(match.group(1))
        return default
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        if any(x in line_lower for x in ['401k savings plan', '401(k) savings plan']):
            result['retirement_401k'] = get_value_after_label(line, '401k')
        
        if 'medical' in line_lower and ('plan' in line_lower or 'ins' in line_lower):
            result['health_insurance'] = get_value_after_label(line, 'medical')
        
        if 'dental plan' in line_lower:
            result['dental_plan'] = get_value_after_label(line, 'dental')
        
        if 'eye plan' in line_lower:
            result['eye_plan'] = get_value_after_label(line, 'eye')
        
        if 'health care fsa' in line_lower:
            result['health_care_fsa'] = get_value_after_label(line, 'fsa')
        
        if 'optional life' in line_lower:
            result['optional_life'] = get_value_after_label(line, 'optional life')
        
        if 'add insurance' in line_lower:
            result['add_insurance'] = get_value_after_label(line, 'add')
        
        if 'federal withholding' in line_lower and 'taxable' not in line_lower:
            result['federal_tax'] = get_value_after_label(line, 'federal withholding')
        
        if ('state tax' in line_lower or 'ga withholding' in line_lower or 'withholding' in line_lower or 'ga' in line_lower) and 'federal' not in line_lower and 'taxable' not in line_lower:
            if 'federal' not in line_lower:
                tax_val = get_value_after_label(line, 'withholding') or get_value_after_label(line, 'state')
                if tax_val:
                    result['state_tax'] = tax_val
                    result['state_name'] = 'GA'
        
        if 'oasdi' in line_lower and 'taxable' not in line_lower and 'social security' not in line_lower:
            result['oasdi'] = get_value_after_label(line, 'oasdi')
        
        if re.search(r'medicare', line_lower) and 'taxable' not in line_lower:
            result['medicare'] = get_value_after_label(line, 'medicare')
        
        if '401k' in line_lower and 'employer' in line_lower and 'match' in line_lower:
            result['employer_match'] = get_value_after_label(line, 'match')
        
        if 'loan repayment' in line_lower or '401k loan' in line_lower:
            result['loan_repayment'] = get_value_after_label(line, 'loan')
        
        if 'dependent life' in line_lower:
            result['dependent_life'] = get_value_after_label(line, 'dependent life')
        
        if 'stock purchase' in line_lower or 'employee stock' in line_lower:
            result['stock_purchase'] = get_value_after_label(line, 'stock')
        
        if 'spousal life' in line_lower:
            result['spousal_life'] = get_value_after_label(line, 'spousal life')
        
        if 'biometric credit' in line_lower and 'spousal' not in line_lower:
            result['biometric_credit'] = get_value_after_label(line, 'biometric')
        
        if 'spousal biometric credit' in line_lower:
            result['spousal_biometric'] = get_value_after_label(line, 'spousal biometric')
        
        if 'group term life' in line_lower:
            result['group_term_life'] = get_value_after_label(line, 'group term')
        
        if 'floating holiday' in line_lower:
            result['floating_holiday'] = get_value_after_label(line, 'floating holiday')
        
        if re.search(r'\bholiday\b', line_lower) and 'holiday pay' not in line_lower and 'floating' not in line_lower:
            result['holiday_pay'] = get_value_after_label(line, 'holiday')
        
        if re.search(r'^vacation\s', line_lower):
            result['vacation_pay'] = get_value_after_label(line, 'vacation')
        
        if re.search(r'^salary\s', line_lower):
            result['salary'] = get_value_after_label(line, 'salary')
        
        if 'pnc' in line_lower:
            result['bank_name'] = 'PNC Bank'
            deposit_val = get_value_after_label(line, 'pnc')
            if deposit_val:
                result['deposit_amount'] = deposit_val
        
        if 'first tech' in line_lower or 'firsttech' in line_lower:
            result['bank2_name'] = 'First Tech Federal Credit Union'
            deposit_val = get_value_after_label(line, 'first') or get_value_after_label(line, 'tech')
            if deposit_val:
                result['deposit2_amount'] = deposit_val
        
        if re.search(r'\*{6}(\d{4})', line):
            acc_match = re.search(r'\*{6}(\d{4})', line)
            if acc_match:
                if result.get('bank_name') == 'PNC Bank' and 'account_number' not in result:
                    result['account_number'] = '****' + acc_match.group(1)
                elif result.get('bank2_name') and 'account2_number' not in result:
                    result['account2_number'] = '****' + acc_match.group(1)
    
    if 'account_number' not in result:
        for line in lines:
            if re.search(r'\*+\d{4}', line):
                acc_match = re.search(r'\*+(\d{4})', line)
                if acc_match and 'account_number' not in result:
                    result['account_number'] = '****' + acc_match.group(1)
    
    return result

def extract_text_from_pdf(pdf_file):
    import io
    
    raw_text = ""
    pdf_bytes = None
    
    if hasattr(pdf_file, 'read'):
        pdf_file.seek(0)
        pdf_bytes = pdf_file.read()
        pdf_file.seek(0)
    
    if not pdf_bytes:
        print("No PDF bytes received")
        return ""
    
    print(f"PDF file size: {len(pdf_bytes)} bytes")
    print(f"PDF header: {pdf_bytes[:20]}")
    
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            print(f"pdfplumber: {len(pdf.pages)} pages")
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    raw_text += text + "\n"
        if raw_text.strip():
            print(f"pdfplumber extracted {len(raw_text)} chars")
            return raw_text
    except Exception as e:
        print(f"pdfplumber error: {e}")
    
    try:
        import fitz
        doc = fitz.open(io.BytesIO(pdf_bytes))
        print(f"PyMuPDF: {len(doc)} pages")
        for page in doc:
            text = page.get_text()
            if text:
                raw_text += text + "\n"
        doc.close()
        if raw_text.strip():
            print(f"PyMuPDF extracted {len(raw_text)} chars")
            return raw_text
    except Exception as e:
        print(f"PyMuPDF error: {e}")
    
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        print(f"PyPDF2: {len(reader.pages)} pages")
        for page in reader.pages:
            text = page.extract_text()
            if text:
                raw_text += text + "\n"
        if raw_text.strip():
            print(f"PyPDF2 extracted {len(raw_text)} chars")
            return raw_text
    except Exception as e:
        print(f"PyPDF2 error: {e}")
    
    print(f"Total extracted: {len(raw_text)} chars")
    return raw_text

@app.route('/import_paycheck', methods=['POST'])
def import_paycheck():
    raw_text = request.form.get('raw_text', '')
    
    pdf_file = request.files.get('pdf_file')
    
    if pdf_file and pdf_file.filename:
        if pdf_file.filename.lower().endswith('.pdf'):
            extracted = extract_text_from_pdf(pdf_file)
            if extracted.strip():
                raw_text = extracted
    
    if not raw_text or raw_text.strip() == '':
        flash('No text could be extracted. Please paste your paystub text manually below.', 'warning')
        paychecks = db.get_all_paychecks()
        next_paycheck = db.get_next_paycheck_date()
        today = datetime.now().strftime('%Y-%m-%d')
        return render_template('paychecks.html', 
                            paychecks=paychecks, 
                            next_paycheck=next_paycheck, 
                            today=today,
                            parsed_data={},
                            raw_text='',
                            active_tab='import')
    
    parsed = parse_paycheck_text(raw_text)
    
    paychecks = db.get_all_paychecks()
    next_paycheck = db.get_next_paycheck_date()
    today = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('paychecks.html', 
                          paychecks=paychecks, 
                          next_paycheck=next_paycheck, 
                          today=today,
                          parsed_data=parsed,
                          raw_text=raw_text,
                          active_tab='import')

@app.route('/save_imported_paycheck', methods=['POST'])
def save_imported_paycheck():
    data = request.form.to_dict()
    
    numeric_fields = ['hours_worked', 'gross_pay', 'net_pay', 'pre_tax_deductions', 'employee_taxes', 
                     'post_tax_deductions', 'salary', 'biometric_credit', 'floating_holiday', 
                     'holiday_pay', 'vacation_pay', 'group_term_life', 'spousal_biometric',
                     'oasdi', 'medicare', 'federal_tax', 'state_tax', 'social_security',
                     'retirement_401k', 'add_insurance', 'dental_plan', 'eye_plan', 
                     'health_care_fsa', 'health_insurance', 'optional_life', 'hsa',
                     'loan_repayment', 'dependent_life', 'stock_purchase', 'spousal_life',
                     'employer_match', 'deposit_amount', 'deposit2_amount']
    
    kwargs = {}
    for field in numeric_fields:
        val = data.get(field, '0').replace(',', '')
        kwargs[field] = float(val) if val else 0
    
    kwargs['pay_date'] = data.get('check_date', '')
    kwargs['pay_period_begin'] = data.get('pay_period_begin', '')
    kwargs['pay_period_end'] = data.get('pay_period_end', '')
    kwargs['check_date'] = data.get('check_date', '')
    kwargs['check_number'] = data.get('check_number', '')
    kwargs['employee_name'] = data.get('employee_name', '')
    kwargs['employee_id'] = data.get('employee_id', '')
    kwargs['company'] = data.get('company', '')
    kwargs['state_name'] = data.get('state_name', '')
    kwargs['federal_filing_status'] = data.get('federal_filing_status', '')
    kwargs['state_filing_status'] = data.get('state_filing_status', '')
    kwargs['bank_name'] = data.get('bank_name', '')
    kwargs['account_number'] = data.get('account_number', '')
    kwargs['bank2_name'] = data.get('bank2_name', '')
    kwargs['account2_number'] = data.get('account2_number', '')
    kwargs['notes'] = f"Imported from paystub text"
    
    db.add_paycheck(**kwargs)
    flash('Paycheck imported and saved successfully!', 'success')
    return redirect(url_for('paychecks'))

@app.route('/bills')
def bills():
    filter_type = request.args.get('filter', 'all')
    all_bills = db.get_bills_with_payees()
    
    if filter_type == 'unpaid':
        bills = [b for b in all_bills if not b['is_paid']]
    elif filter_type == 'paid':
        bills = [b for b in all_bills if b['is_paid']]
    elif filter_type == 'overdue':
        today = datetime.now().strftime('%Y-%m-%d')
        bills = [b for b in all_bills if not b['is_paid'] and b['due_date'] < today]
    else:
        bills = all_bills
    
    payees = db.get_all_payees()
    return render_template('bills.html', bills=bills, payees=payees, filter_type=filter_type)

@app.route('/add_bill', methods=['POST'])
def add_bill():
    db.add_bill(
        request.form['payee_id'] or None,
        float(request.form['amount']),
        request.form['due_date'],
        1 if request.form.get('is_recurring') else 0,
        request.form.get('recurrence_type'),
        request.form.get('notes', '')
    )
    flash('Bill added successfully!', 'success')
    return redirect(url_for('bills'))

@app.route('/update_bill/<int:id>', methods=['POST'])
def update_bill(id):
    db.update_bill(
        id,
        request.form['payee_id'] or None,
        float(request.form['amount']),
        request.form['due_date'],
        1 if request.form.get('is_recurring') else 0,
        request.form.get('recurrence_type'),
        request.form.get('notes', '')
    )
    flash('Bill updated successfully!', 'success')
    return redirect(url_for('bills'))

@app.route('/mark_bill_paid/<int:id>')
def mark_bill_paid(id):
    db.mark_bill_paid(id)
    flash('Bill marked as paid!', 'success')
    return redirect(url_for('bills'))

@app.route('/mark_bill_unpaid/<int:id>')
def mark_bill_unpaid(id):
    db.mark_bill_unpaid(id)
    flash('Bill marked as unpaid.', 'info')
    return redirect(url_for('bills'))

@app.route('/delete_bill/<int:id>')
def delete_bill(id):
    db.delete_bill(id)
    flash('Bill deleted.', 'info')
    return redirect(url_for('bills'))

@app.route('/payees')
def payees():
    payees = db.get_all_payees()
    return render_template('payees.html', payees=payees)

@app.route('/add_payee', methods=['POST'])
def add_payee():
    db.add_payee(
        request.form['name'],
        request.form.get('category', ''),
        request.form.get('account_number', ''),
        request.form.get('notes', ''),
        request.form.get('website', '')
    )
    flash('Payee added successfully!', 'success')
    return redirect(url_for('payees'))

@app.route('/update_payee/<int:id>', methods=['POST'])
def update_payee(id):
    db.update_payee(
        id,
        request.form['name'],
        request.form.get('category', ''),
        request.form.get('account_number', ''),
        request.form.get('notes', ''),
        request.form.get('website', '')
    )
    flash('Payee updated successfully!', 'success')
    return redirect(url_for('payees'))

@app.route('/delete_payee/<int:id>')
def delete_payee(id):
    db.delete_payee(id)
    flash('Payee deleted.', 'info')
    return redirect(url_for('payees'))

@app.route('/bank_accounts')
def bank_accounts():
    accounts = db.get_all_bank_accounts()
    return render_template('bank_accounts.html', accounts=accounts)

@app.route('/add_bank_account', methods=['POST'])
def add_bank_account():
    db.add_bank_account(
        request.form['name'],
        request.form['account_type'],
        request.form.get('institution', ''),
        request.form.get('account_number_last4', ''),
        float(request.form['current_balance']),
        request.form.get('website', '')
    )
    flash('Bank account added successfully!', 'success')
    return redirect(url_for('bank_accounts'))

@app.route('/update_bank_account/<int:id>', methods=['POST'])
def update_bank_account(id):
    db.update_bank_account(
        id,
        request.form['name'],
        request.form['account_type'],
        request.form.get('institution', ''),
        request.form.get('account_number_last4', ''),
        float(request.form['current_balance']),
        request.form.get('website', '')
    )
    flash('Bank account updated successfully!', 'success')
    return redirect(url_for('bank_accounts'))

@app.route('/delete_bank_account/<int:id>')
def delete_bank_account(id):
    db.delete_bank_account(id)
    flash('Bank account deleted.', 'info')
    return redirect(url_for('bank_accounts'))

@app.route('/credit_cards')
def credit_cards():
    cards = db.get_all_credit_cards()
    return render_template('credit_cards.html', cards=cards)

@app.route('/add_credit_card', methods=['POST'])
def add_credit_card():
    db.add_credit_card(
        request.form['name'],
        request.form.get('last_four', ''),
        float(request.form['credit_limit']),
        float(request.form['current_balance']),
        float(request.form.get('interest_rate', 0)),
        request.form.get('website', '')
    )
    flash('Credit card added successfully!', 'success')
    return redirect(url_for('credit_cards'))

@app.route('/update_credit_card/<int:id>', methods=['POST'])
def update_credit_card(id):
    db.update_credit_card(
        id,
        request.form['name'],
        request.form.get('last_four', ''),
        float(request.form['credit_limit']),
        float(request.form['current_balance']),
        float(request.form.get('interest_rate', 0)),
        request.form.get('website', '')
    )
    flash('Credit card updated successfully!', 'success')
    return redirect(url_for('credit_cards'))

@app.route('/delete_credit_card/<int:id>')
def delete_credit_card(id):
    db.delete_credit_card(id)
    flash('Credit card deleted.', 'info')
    return redirect(url_for('credit_cards'))

@app.route('/budget')
def budget():
    categories = db.get_budget_categories()
    return render_template('budget.html', categories=categories)

@app.route('/add_budget_category', methods=['POST'])
def add_budget_category():
    db.add_budget_category(
        request.form['name'],
        float(request.form['monthly_limit']),
        request.form.get('color', '#2E7D32')
    )
    flash('Budget category added successfully!', 'success')
    return redirect(url_for('budget'))

@app.route('/update_budget_category/<int:id>', methods=['POST'])
def update_budget_category(id):
    db.update_budget_category(
        id,
        request.form['name'],
        float(request.form['monthly_limit']),
        request.form.get('color', '#2E7D32')
    )
    flash('Budget category updated successfully!', 'success')
    return redirect(url_for('budget'))

@app.route('/delete_budget_category/<int:id>')
def delete_budget_category(id):
    db.delete_budget_category(id)
    flash('Budget category deleted.', 'info')
    return redirect(url_for('budget'))

@app.route('/api/dashboard_stats')
def api_dashboard_stats():
    return jsonify(db.get_dashboard_stats())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
