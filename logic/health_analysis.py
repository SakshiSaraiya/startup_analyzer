def analyze_financial_health(df):
    latest = df.iloc[-1]
    ratios = {
        "Net Margin (%)": round((latest['Net Profit'] / latest['Revenue']) * 100, 2),
        "Current Ratio": round(latest['Total Assets'] / latest['Total Liabilities'], 2),
        "Debt-to-Equity": round(latest['Total Liabilities'] / latest['Equity'], 2),
        "Interest Coverage": round(latest['Net Profit'] / latest['Interest Expense'], 2)
    }
    return ratios
