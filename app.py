from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
import calendar
import csv
import io
import database as db

app = Flask(__name__)
app.secret_key = 'budget-app-secret-key-2024'

db.init_db()

def add_months(dt, months):
    # Safely add months to a date
    year = dt.year + (dt.month - 1 + months) // 12
    month = (dt.month - 1 + months) % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)

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

@app.route('/add_paycheck', methods=['GET'])
def add_paycheck_form():
    import json
    prefill = {}
    if request.args.get('prefill'):
        try:
            prefill = json.loads(request.args.get('prefill'))
        except:
            pass
    return render_template('add_paycheck.html', paycheck=prefill)


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
        employer_hsa=float(request.form.get('employer_hsa') or 0),
        federal_filing_status=request.form.get('federal_filing_status', ''),
        state_filing_status=request.form.get('state_filing_status', ''),
        bank_name=request.form.get('bank_name', ''),
        account_number=request.form.get('account_number', ''),
        deposit_amount=float(request.form.get('deposit_amount') or 0),
        bank2_name=request.form.get('bank2_name', ''),
        account2_number=request.form.get('account2_number', ''),
        deposit2_amount=float(request.form.get('deposit2_amount') or 0),
        gross_pay_ytd=float(request.form.get('gross_pay_ytd') or 0),
        pre_tax_deductions_ytd=float(request.form.get('pre_tax_deductions_ytd') or 0),
        employee_taxes_ytd=float(request.form.get('employee_taxes_ytd') or 0),
        post_tax_deductions_ytd=float(request.form.get('post_tax_deductions_ytd') or 0),
        net_pay_ytd=float(request.form.get('net_pay_ytd') or 0),
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
                      'employer_match', 'employer_hsa', 'deposit_amount', 'deposit2_amount',
                      'gross_pay_ytd', 'pre_tax_deductions_ytd', 'employee_taxes_ytd',
                      'post_tax_deductions_ytd', 'net_pay_ytd']
    
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
            name_words = []
            for word in words:
                if word[0].isupper() and len(word) > 2 and not any(c.isdigit() for c in word):
                    if 'voyix' not in word.lower() and 'corporation' not in word.lower() and word not in ['Name', 'Company', 'Employee', 'Description', 'Amount', 'Current', 'YTD', 'Hours', 'Gross', 'Tax', 'Net']:
                        name_words.append(word)
                        if len(name_words) >= 2:
                            break
            if name_words:
                result['employee_name'] = ' '.join(name_words)
    
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
    
    ytd_line = None
    for line in lines:
        line_lower = line.lower()
        if 'ytd' in line_lower and re.search(r'^\s*YTD', line):
            money_matches = re.findall(r'([\d,]+\.\d{2})', line)
            if len(money_matches) >= 5:
                ytd_line = line
                break
    
    if ytd_line:
        money_matches = re.findall(r'([\d,]+\.\d{2})', ytd_line)
        if len(money_matches) >= 6:
            result['hours_worked_ytd'] = extract_money(money_matches[0])
            result['gross_pay_ytd'] = extract_money(money_matches[1])
            result['pre_tax_deductions_ytd'] = extract_money(money_matches[2])
            result['employee_taxes_ytd'] = extract_money(money_matches[3])
            result['post_tax_deductions_ytd'] = extract_money(money_matches[4])
            result['net_pay_ytd'] = extract_money(money_matches[5])
    
    def get_value_after_label(line, label, default=None, ytd=False):
        idx = line.lower().find(label)
        if idx == -1:
            return default
        after_label = line[idx + len(label):]
        matches = re.findall(r'([\d,]+\.\d{2})', after_label)
        if matches:
            idx = 1 if ytd else 0
            if idx < len(matches):
                return extract_money(matches[idx])
            return extract_money(matches[0])
        return default
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        if any(x in line_lower for x in ['401k savings plan', '401(k) savings plan']):
            result['retirement_401k'] = get_value_after_label(line, '401k')
            result['retirement_401k_ytd'] = get_value_after_label(line, '401k', ytd=True)
        
        if 'medical' in line_lower and ('plan' in line_lower or 'ins' in line_lower):
            result['health_insurance'] = get_value_after_label(line, 'medical')
            result['health_insurance_ytd'] = get_value_after_label(line, 'medical', ytd=True)
        
        if 'dental plan' in line_lower:
            result['dental_plan'] = get_value_after_label(line, 'dental')
            result['dental_plan_ytd'] = get_value_after_label(line, 'dental', ytd=True)
        
        if 'eye plan' in line_lower:
            result['eye_plan'] = get_value_after_label(line, 'eye')
            result['eye_plan_ytd'] = get_value_after_label(line, 'eye', ytd=True)
        
        if 'health care fsa' in line_lower:
            result['health_care_fsa'] = get_value_after_label(line, 'fsa')
            result['health_care_fsa_ytd'] = get_value_after_label(line, 'fsa', ytd=True)
        
        if 'optional life' in line_lower:
            result['optional_life'] = get_value_after_label(line, 'optional life')
            result['optional_life_ytd'] = get_value_after_label(line, 'optional life', ytd=True)
        
        if 'add insurance' in line_lower:
            result['add_insurance'] = get_value_after_label(line, 'add')
            result['add_insurance_ytd'] = get_value_after_label(line, 'add', ytd=True)
        
        if 'federal withholding' in line_lower and 'taxable' not in line_lower:
            result['federal_tax'] = get_value_after_label(line, 'federal withholding')
            result['federal_tax_ytd'] = get_value_after_label(line, 'federal withholding', ytd=True)
        
        if ('state tax' in line_lower or 'ga withholding' in line_lower or 'withholding' in line_lower or 'ga' in line_lower) and 'federal' not in line_lower and 'taxable' not in line_lower:
            if 'federal' not in line_lower:
                tax_val = get_value_after_label(line, 'withholding') or get_value_after_label(line, 'state')
                if tax_val:
                    result['state_tax'] = tax_val
                    result['state_name'] = 'GA'
                    result['state_tax_ytd'] = get_value_after_label(line, 'state', ytd=True) or get_value_after_label(line, 'withholding', ytd=True)
        
        if 'oasdi' in line_lower and 'taxable' not in line_lower and 'social security' not in line_lower:
            result['oasdi'] = get_value_after_label(line, 'oasdi')
            result['oasdi_ytd'] = get_value_after_label(line, 'oasdi', ytd=True)
        
        if re.search(r'medicare', line_lower) and 'taxable' not in line_lower:
            result['medicare'] = get_value_after_label(line, 'medicare')
            result['medicare_ytd'] = get_value_after_label(line, 'medicare', ytd=True)
        
        if '401k' in line_lower and 'employer' in line_lower and 'match' in line_lower:
            result['employer_match'] = get_value_after_label(line, 'match')
            result['employer_match_ytd'] = get_value_after_label(line, 'match', ytd=True)
        
        if 'hsa' in line_lower and 'employee' in line_lower:
            result['hsa'] = get_value_after_label(line, 'hsa')
            result['hsa_ytd'] = get_value_after_label(line, 'hsa', ytd=True)
        
        if 'hsa' in line_lower and 'employer' in line_lower:
            result['employer_hsa'] = get_value_after_label(line, 'hsa')
            result['employer_hsa_ytd'] = get_value_after_label(line, 'hsa', ytd=True)
        
        if 'loan repayment' in line_lower or '401k loan' in line_lower:
            result['loan_repayment'] = get_value_after_label(line, 'loan')
            result['loan_repayment_ytd'] = get_value_after_label(line, 'loan', ytd=True)
        
        if 'dependent life' in line_lower:
            result['dependent_life'] = get_value_after_label(line, 'dependent life')
            result['dependent_life_ytd'] = get_value_after_label(line, 'dependent life', ytd=True)
        
        if 'stock purchase' in line_lower or 'employee stock' in line_lower:
            result['stock_purchase'] = get_value_after_label(line, 'stock')
            result['stock_purchase_ytd'] = get_value_after_label(line, 'stock', ytd=True)
        
        if 'spousal life' in line_lower:
            result['spousal_life'] = get_value_after_label(line, 'spousal life')
            result['spousal_life_ytd'] = get_value_after_label(line, 'spousal life', ytd=True)
        
        if 'biometric credit' in line_lower and 'spousal' not in line_lower:
            result['biometric_credit'] = get_value_after_label(line, 'biometric')
            result['biometric_credit_ytd'] = get_value_after_label(line, 'biometric', ytd=True)
        
        if 'spousal biometric credit' in line_lower:
            result['spousal_biometric'] = get_value_after_label(line, 'spousal biometric')
            result['spousal_biometric_ytd'] = get_value_after_label(line, 'spousal biometric', ytd=True)
        
        if 'group term life' in line_lower:
            result['group_term_life'] = get_value_after_label(line, 'group term')
            result['group_term_life_ytd'] = get_value_after_label(line, 'group term', ytd=True)
        
        if 'floating holiday' in line_lower:
            result['floating_holiday'] = get_value_after_label(line, 'floating holiday')
            result['floating_holiday_ytd'] = get_value_after_label(line, 'floating holiday', ytd=True)
        
        if re.search(r'\bholiday\b', line_lower) and 'holiday pay' not in line_lower and 'floating' not in line_lower:
            result['holiday_pay'] = get_value_after_label(line, 'holiday')
            result['holiday_pay_ytd'] = get_value_after_label(line, 'holiday', ytd=True)
        
        if re.search(r'^vacation\s', line_lower):
            result['vacation_pay'] = get_value_after_label(line, 'vacation')
            result['vacation_pay_ytd'] = get_value_after_label(line, 'vacation', ytd=True)
        
        if re.search(r'^salary\s', line_lower):
            result['salary'] = get_value_after_label(line, 'salary')
            result['salary_ytd'] = get_value_after_label(line, 'salary', ytd=True)
        
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
    import json
    
    data = request.form.to_dict()
    if 'parsed_json' in data:
        try:
            parsed = json.loads(data['parsed_json'])
            data.update(parsed)
        except:
            pass
    
    numeric_fields = ['hours_worked', 'gross_pay', 'net_pay', 'pre_tax_deductions', 'employee_taxes', 
                     'post_tax_deductions', 'salary', 'biometric_credit', 'floating_holiday', 
                     'holiday_pay', 'vacation_pay', 'group_term_life', 'spousal_biometric',
                     'oasdi', 'medicare', 'federal_tax', 'state_tax', 'social_security',
                     'retirement_401k', 'add_insurance', 'dental_plan', 'eye_plan', 
                     'health_care_fsa', 'health_insurance', 'optional_life', 'hsa',
                     'loan_repayment', 'dependent_life', 'stock_purchase', 'spousal_life',
                     'employer_match', 'employer_hsa', 'deposit_amount', 'deposit2_amount',
                     'gross_pay_ytd', 'pre_tax_deductions_ytd', 'employee_taxes_ytd',
                     'post_tax_deductions_ytd', 'net_pay_ytd', 'hours_worked_ytd',
                     'salary_ytd', 'vacation_pay_ytd', 'biometric_credit_ytd', 'spousal_biometric_ytd',
                     'group_term_life_ytd', 'floating_holiday_ytd', 'holiday_pay_ytd',
                     'retirement_401k_ytd', 'health_insurance_ytd', 'dental_plan_ytd', 'eye_plan_ytd',
                     'health_care_fsa_ytd', 'optional_life_ytd', 'add_insurance_ytd', 'hsa_ytd',
                     'federal_tax_ytd', 'state_tax_ytd', 'oasdi_ytd', 'medicare_ytd',
                     'loan_repayment_ytd', 'dependent_life_ytd', 'stock_purchase_ytd', 'spousal_life_ytd',
                     'employer_match_ytd', 'employer_hsa_ytd']
    
    kwargs = {}
    for field in numeric_fields:
        val = str(data.get(field, '0')).replace(',', '')
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
    categories = db.get_budget_categories()
    return render_template('bills.html', bills=bills, payees=payees, categories=categories, filter_type=filter_type)

@app.route('/add_bill')
def add_bill_form():
    payees = db.get_all_payees()
    categories = db.get_budget_categories()
    return render_template('add_bill.html', payees=payees, categories=categories)

@app.route('/add_bill', methods=['POST'])
def add_bill():
    payee_id = request.form.get('payee_id') or None
    amount = request.form.get('amount', '0')
    due_date = request.form.get('due_date', '')
    
    if not due_date or not amount or float(amount) == 0:
        flash('Amount and due date are required!', 'danger')
        return redirect(url_for('add_bill_form'))
    
    db.add_bill(
        payee_id,
        float(amount),
        due_date,
        1 if request.form.get('is_recurring') else 0,
        request.form.get('recurrence_type'),
        request.form.get('notes', ''),
        request.form.get('category_id') or None,
        request.form.get('account') or None
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
        request.form.get('notes', ''),
        request.form.get('category_id') or None,
        request.form.get('account') or None
    )
    flash('Bill updated successfully!', 'success')
    return redirect(url_for('bills'))

@app.route('/mark_bill_paid/<int:id>')
def mark_bill_paid(id):
    conn = db.get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT is_recurring, recurrence_type, due_date FROM bills WHERE id = ?', (id,))
    bill = cursor.fetchone()
    
    if not bill:
        flash('Bill not found', 'danger')
        return redirect(url_for('bills'))
    
    is_recurring, recurrence_type, old_due_date = bill[0], bill[1], bill[2]
    
    if is_recurring and old_due_date:
        try:
            old_due = datetime.strptime(old_due_date, '%Y-%m-%d')
            today = datetime.now()
            
            # Compute next due date - keep adding recurrence until we get a date >= today
            new_due = old_due
            while new_due < today:
                if recurrence_type == 'weekly':
                    new_due = new_due + timedelta(weeks=1)
                elif recurrence_type == 'biweekly':
                    new_due = new_due + timedelta(weeks=2)
                elif recurrence_type == 'monthly':
                    new_due = add_months(new_due, 1)
                elif recurrence_type == 'quarterly':
                    new_due = add_months(new_due, 3)
                elif recurrence_type == 'semi-monthly':
                    if new_due.day < 15:
                        new_due = new_due.replace(day=15)
                    else:
                        new_due = add_months(new_due, 1)
                        new_due = new_due.replace(day=1)
                else:
                    break
            
            # Reset to unpaid with new due date
            cursor.execute('UPDATE bills SET is_paid=0, paid_date=NULL, due_date=? WHERE id=?',
                        (new_due.strftime('%Y-%m-%d'), id))
            flash(f'Bill marked as paid. Next due: {new_due.strftime("%m/%d/%Y")}', 'success')
        except Exception as e:
            flash(f'Error updating recurring bill: {e}', 'danger')
            # Still mark as paid for this period
            cursor.execute('UPDATE bills SET is_paid=1, paid_date=? WHERE id=?',
                        (datetime.now().strftime('%Y-%m-%d'), id))
    else:
        cursor.execute('UPDATE bills SET is_paid=1, paid_date=? WHERE id=?',
                    (datetime.now().strftime('%Y-%m-%d'), id))
        flash('Bill marked as paid!', 'success')
    
    conn.commit()
    conn.close()
    
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

@app.route('/categories')
def categories():
    payees = db.get_all_payees()
    payee_categories = list(set(p['category'] for p in payees if p.get('category')))
    budget_categories = db.get_budget_categories()
    return render_template('categories.html', payee_categories=payee_categories, budget_categories=budget_categories)

@app.route('/add_payee_category', methods=['POST'])
def add_payee_category():
    category = request.form.get('category', '').strip()
    if category:
        db.add_payee_category_name(category)
    flash('Category added successfully!', 'success')
    return redirect(url_for('categories'))

@app.route('/delete_payee_category', methods=['POST'])
def delete_payee_category():
    category = request.form.get('category', '').strip()
    if category:
        db.delete_payee_category_by_name(category)
    flash('Category deleted.', 'info')
    return redirect(url_for('categories'))

@app.route('/add_payee')
def add_payee_form():
    return render_template('add_payee.html')

@app.route('/add_payee', methods=['POST'])
def add_payee():
    payee_id = db.add_payee(
        request.form['name'],
        request.form.get('category', ''),
        request.form.get('account_number', ''),
        request.form.get('notes', ''),
        request.form.get('website', '')
    )
    flash('Payee added successfully!', 'success')
    return redirect(url_for('payees'))

@app.route('/add_payee_ajax', methods=['POST'])
def add_payee_ajax():
    try:
        name = request.form.get('name', '').strip()
        if not name:
            return jsonify({'success': False, 'error': 'Name is required'}), 400
        
        payee_id = db.add_payee(
            name,
            request.form.get('category', ''),
            request.form.get('account_number', ''),
            request.form.get('notes', ''),
            request.form.get('website', '')
        )
        return jsonify({'success': True, 'payee_id': payee_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

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

@app.route('/transactions')
def transactions():
    account_id = request.args.get('account_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    search = request.args.get('search', '')
    
    txns = db.get_transactions(account_id, start_date, end_date)
    
    if search:
        txns = [t for t in txns if search.lower() in t['description'].lower()]
    
    accounts = db.get_all_bank_accounts()
    selected_account_name = None
    if account_id:
        selected_account = db.get_bank_account(account_id)
        if selected_account:
            selected_account_name = selected_account['name']
    else:
        selected_account_name = "All Accounts"
    
    return render_template('transactions.html', 
                     transactions=txns, 
                     accounts=accounts, 
                     selected_account=account_id, 
                     selected_account_name=selected_account_name)

@app.route('/import_transactions', methods=['POST'])
def import_transactions():
    account_id = request.form.get('account_id', type=int)
    clear_existing = request.form.get('clear_existing') == 'on'
    skip_duplicates = request.form.get('skip_duplicates') == 'on'
    
    if clear_existing:
        db.clear_transactions(account_id)
    
    if 'csv_file' not in request.files:
        flash('No file uploaded', 'danger')
        return redirect(url_for('transactions'))
    
    file = request.files['csv_file']
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('transactions'))
    
    try:
        content = file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(content))
        
        transactions_list = []
        duplicates = []
        for row in reader:
            date = row.get('Date', row.get('Posting Date', row.get('Transaction Date', ''))).strip()
            description = row.get('Description', row.get('Transaction Description', row.get('Memo', ''))).strip()
            amount_str = row.get('Amount', row.get('Transaction Amount', '0')).strip().replace('$', '').replace(',', '').replace(' ', '')
            balance_str = row.get('Balance', '0').strip().replace('$', '').replace(',', '').replace(' ', '')
            
            try:
                amount = float(amount_str)
            except:
                amount = 0
            
            try:
                balance = float(balance_str)
            except:
                balance = 0
            
            if date and amount != 0:
                transactions_list.append({
                    'date': date,
                    'description': description,
                    'amount': amount,
                    'balance': balance
                })
        
        if transactions_list:
            existing = db.get_transactions(account_id)
            existing_keys = set((tx['date'], tx['amount']) for tx in existing)
            
            new_transactions = []
            duplicate_count = 0
            for tx in transactions_list:
                key = (tx['date'], tx['amount'])
                if key in existing_keys:
                    duplicate_count += 1
                    if not skip_duplicates:
                        duplicates.append(tx)
                else:
                    new_transactions.append(tx)
            
            if duplicates and not skip_duplicates:
                return render_template('transactions.html', 
                    transactions=existing, 
                    accounts=db.get_all_bank_accounts(), 
                    selected_account=account_id,
                    duplicate_prompt=True,
                    duplicate_transactions=duplicates,
                    new_count=len(transactions_list),
                    csv_content=content)
            
            if new_transactions:
                db.add_transactions(account_id, new_transactions)
                
                # Sort by date to get the oldest (most recent) transaction for balance
                sorted_txns = sorted(new_transactions, key=lambda x: x['date'], reverse=True)
                latest_balance = sorted_txns[0]['balance'] if sorted_txns else 0
                
                account = db.get_bank_account(account_id)
                if account:
                    db.update_bank_account(account_id, account['name'], account['account_type'], 
                        account['institution'], account['account_number_last4'], latest_balance, account.get('website', ''))
                
                flash(f'Imported {len(new_transactions)} transactions', 'success')
            else:
                flash('All transactions already exist', 'info')
        else:
            flash('No transactions found in file', 'warning')
    except Exception as e:
        flash(f'Error importing: {str(e)}', 'danger')
    
    return redirect(url_for('transactions'))

@app.route('/import_transactions/confirm', methods=['POST'])
def import_transactions_confirm():
    account_id = request.form.get('account_id', type=int)
    skip_duplicates = True
    
    try:
        content = request.form.get('csv_content', '')
        if content:
            reader = csv.DictReader(io.StringIO(content))
            
            transactions_list = []
            for row in reader:
                date = row.get('Date', row.get('Posting Date', row.get('Transaction Date', ''))).strip()
                description = row.get('Description', row.get('Transaction Description', row.get('Memo', ''))).strip()
                amount_str = row.get('Amount', row.get('Transaction Amount', '0')).strip().replace('$', '').replace(',', '').replace(' ', '')
                balance_str = row.get('Balance', '0').strip().replace('$', '').replace(',', '').replace(' ', '')
                
                try:
                    amount = float(amount_str)
                except:
                    amount = 0
                
                try:
                    balance = float(balance_str)
                except:
                    balance = 0
                
                if date and amount != 0:
                    transactions_list.append({
                        'date': date,
                        'description': description,
                        'amount': amount,
                        'balance': balance
                    })
            
            existing = db.get_transactions(account_id)
            existing_keys = set((tx['date'], tx['amount']) for tx in existing)
            
            new_transactions = [tx for tx in transactions_list if (tx['date'], tx['amount']) not in existing_keys]
            
            if new_transactions:
                db.add_transactions(account_id, new_transactions)
                
                latest_balance = new_transactions[-1]['balance'] if new_transactions else 0
                if latest_balance != 0:
                    account = db.get_bank_account(account_id)
                    if account:
                        db.update_bank_account(account_id, account['name'], account['account_type'], 
                            account['institution'], account['account_number_last4'], latest_balance, account.get('website', ''))
                
                flash(f'Imported {len(new_transactions)} transactions (skipped duplicates)', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('transactions'))
    
    file = request.files['csv_file']
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('transactions'))
    
    try:
        content = file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(content))
        
        transactions_list = []
        for row in reader:
            date = row.get('Date', row.get('Posting Date', row.get('Transaction Date', ''))).strip()
            description = row.get('Description', row.get('Transaction Description', row.get('Memo', ''))).strip()
            amount_str = row.get('Amount', row.get('Transaction Amount', '0')).strip().replace('$', '').replace(',', '')
            balance_str = row.get('Balance', '0').strip().replace('$', '').replace(',', '')
            
            try:
                amount = float(amount_str)
            except:
                amount = 0
            
            try:
                balance = float(balance_str)
            except:
                balance = 0
            
            if date:
                transactions_list.append({
                    'date': date,
                    'description': description,
                    'amount': amount,
                    'balance': balance
                })
        
        if transactions_list:
            db.add_transactions(account_id, transactions_list)
            flash(f'Imported {len(transactions_list)} transactions', 'success')
        else:
            flash('No transactions found in file', 'warning')
    except Exception as e:
        flash(f'Error importing: {str(e)}', 'danger')
    
    return redirect(url_for('transactions'))

@app.route('/add_bank_account')
def add_bank_account_form():
    return render_template('add_bank_account.html')

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

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    account_id = request.form.get('account_id', type=int)
    transaction_date = request.form.get('transaction_date')
    description = request.form.get('description')
    amount = float(request.form.get('amount', 0))
    running_balance = float(request.form.get('running_balance', 0))
    
    db.add_transaction(account_id, transaction_date, description, amount, running_balance)
    
    if account_id:
        account = db.get_bank_account(account_id)
        if account:
            db.update_bank_account(account_id, account['name'], account['account_type'], 
                account['institution'], account['account_number_last4'], running_balance, account.get('website', ''))
    
    flash('Transaction added successfully!', 'success')
    return redirect(url_for('transactions', account_id=account_id))

@app.route('/update_transaction', methods=['POST'])
def update_transaction():
    id = request.form.get('id', type=int)
    account_id = request.form.get('account_id', type=int)
    transaction_date = request.form.get('transaction_date')
    description = request.form.get('description')
    amount = float(request.form.get('amount', 0))
    running_balance = float(request.form.get('running_balance', 0))
    
    db.update_transaction(id, transaction_date, description, amount, running_balance)
    
    if account_id:
        account = db.get_bank_account(account_id)
        if account:
            db.update_bank_account(account_id, account['name'], account['account_type'], 
                account['institution'], account['account_number_last4'], running_balance, account.get('website', ''))
    
    flash('Transaction updated successfully!', 'success')
    return redirect(url_for('transactions', account_id=account_id))

@app.route('/delete_transaction/<int:id>')
def delete_transaction(id):
    tx = db.get_transaction(id)
    if not tx:
        flash('Transaction not found.', 'danger')
        return redirect(url_for('transactions'))

    account_id = tx['account_id']

    # Delete first, then recompute balance from remaining transactions
    db.delete_transaction(id)

    new_balance = 0
    if account_id:
        txns = db.get_transactions(account_id)
        new_balance = txns[0]['balance'] if txns else 0
        account = db.get_bank_account(account_id)
        if account:
            db.update_bank_account(account_id, account['name'], account['account_type'], 
                account['institution'], account['account_number_last4'], new_balance, account.get('website', ''))

    flash('Transaction deleted.', 'info')
    return redirect(url_for('transactions', account_id=account_id))

@app.route('/clear_transactions')
def clear_transactions():
    account_id = request.args.get('account_id', type=int)
    if account_id:
        db.clear_transactions(account_id)
        flash('All transactions cleared for this account.', 'info')
    return redirect(url_for('transactions', account_id=account_id))

@app.route('/credit_cards')
def credit_cards():
    cards = db.get_all_credit_cards()
    return render_template('credit_cards.html', cards=cards)

@app.route('/add_credit_card')
def add_credit_card_form():
    return render_template('add_credit_card.html')

@app.route('/add_credit_card', methods=['POST'])
def add_credit_card():
    db.add_credit_card(
        request.form['name'],
        request.form.get('last_four', ''),
        float(request.form['credit_limit']),
        float(request.form['current_balance']),
        float(request.form.get('interest_rate', 0)),
        request.form.get('due_date', ''),
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
        request.form.get('due_date', ''),
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
    all_bills = db.get_bills_with_payees()
    
    bills_by_category = {}
    total_actual = 0
    for cat in categories:
        cat_id = cat['id']
        cat_bills = [b for b in all_bills if b.get('category_id') == cat_id]
        bills_by_category[cat_id] = cat_bills
        for bill in cat_bills:
            if bill.get('is_paid'):
                total_actual += bill.get('amount', 0)
    
    total_budget = sum(cat['monthly_limit'] for cat in categories)
    return render_template('budget.html', 
                        categories=categories, 
                        bills_by_category=bills_by_category,
                        all_bills=all_bills,
                        total_actual=total_actual,
                        total_budget=total_budget)

@app.route('/add_budget_category')
def add_budget_category_form():
    return render_template('add_budget_category.html')

@app.route('/add_budget_category', methods=['POST'])
def add_budget_category():
    db.add_budget_category(
        request.form['name'],
        float(request.form['monthly_limit']),
        request.form.get('color', '#2E7D32'),
        request.form.get('due_date', ''),
        request.form.get('notes', ''),
        float(request.form.get('actual_spent') or 0)
    )
    flash('Budget category added successfully!', 'success')
    return redirect(url_for('budget'))

@app.route('/update_budget_category/<int:id>', methods=['POST'])
def update_budget_category(id):
    actual = request.form.get('actual_spent')
    db.update_budget_category(
        id,
        request.form['name'],
        float(request.form['monthly_limit']),
        request.form.get('color', '#2E7D32'),
        request.form.get('due_date', ''),
        request.form.get('notes', ''),
        float(actual) if actual else None
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


@app.route('/api/account/<int:id>')
def api_account(id):
    account = db.get_bank_account(id)
    if account:
        return jsonify(dict(account))
    return jsonify({'error': 'Account not found'}), 404


@app.route('/import_paycheck_pdf', methods=['POST'])
def import_paycheck_pdf():
    if 'pdf_file' not in request.files:
        flash('No file uploaded', 'danger')
        return redirect(url_for('import_paystub'))
    file = request.files['pdf_file']
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('import_paystub'))
    if file and file.filename.endswith('.pdf'):
        import os
        import uuid
        import tempfile
        
        try:
            from pypdf import PdfReader
            
            file_content = file.read()
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                tmp.write(file_content)
                tmp_path = tmp.name
            
            text = PdfReader(tmp_path).pages[0].extract_text()
            os.unlink(tmp_path)
        except Exception as e:
            flash(f'Error reading PDF: {str(e)}', 'danger')
            return redirect(url_for('import_paystub'))
        
        data = parse_paycheck_text(text)
        import json
        return render_template('import_paystub.html', parsed_data=data)
    
    flash('Invalid file type', 'danger')
    return redirect(url_for('import_paystub'))


@app.route('/import_paystub')
def import_paystub_form():
    return render_template('import_paystub.html')


@app.route('/view_paycheck/<int:id>')
def view_paycheck(id):
    paycheck = db.get_paycheck(id)
    if not paycheck:
        flash('Paycheck not found', 'danger')
        return redirect(url_for('paychecks'))
    return render_template('view_paycheck.html', paycheck=paycheck)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
