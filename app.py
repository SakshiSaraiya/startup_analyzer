from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pandas as pd
from logic.health_analysis import analyze_financial_health
from logic.valuation import calculate_valuation

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

REQUIRED_COLUMNS = ['Year', 'Revenue', 'COGS', 'Operating Expense', 'Net Profit',
                    'Total Assets', 'Total Liabilities', 'Equity',
                    'Inventory', 'Receivables', 'Interest Expense']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('financials')
        if not file:
            flash("Please upload a financial CSV file.")
            return redirect(request.url)

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        df = pd.read_csv(filepath)

        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            flash(f"Missing required columns: {', '.join(missing_cols)}")
            return redirect(request.url)

        try:
            valuation_inputs = {
                'startup_name': request.form['startup_name'],
                'base_revenue': float(request.form['base_revenue']),
                'growth_rate': float(request.form['growth_rate']),
                'ebitda_margin': float(request.form['ebitda_margin']),
                'discount_rate': float(request.form['discount_rate']),
                'terminal_growth': float(request.form['terminal_growth']),
                'horizon': int(request.form['horizon']),
                'exit_multiple': float(request.form['exit_multiple']),
                'irr': float(request.form['irr']),
                'peer_multiple': float(request.form['peer_multiple']),
                'metric_type': request.form['metric_type'],
                'amount_raising': float(request.form['amount_raising'] or 0)
            }
        except Exception as e:
            flash(f"Error in input fields: {e}")
            return redirect(request.url)

        health_data = analyze_financial_health(df)
        valuation_data = calculate_valuation(valuation_inputs)

        return render_template('result.html',
                               health=health_data,
                               valuation=valuation_data,
                               startup_name=valuation_inputs['startup_name'])

    return render_template('index.html')
