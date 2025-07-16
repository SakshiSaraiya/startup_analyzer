def calculate_valuation(inputs):
    revenue = inputs['base_revenue']
    growth = inputs['growth_rate'] / 100
    ebitda_margin = inputs['ebitda_margin'] / 100
    discount = inputs['discount_rate'] / 100
    terminal_growth = inputs['terminal_growth'] / 100
    horizon = inputs['horizon']

    cash_flows = []
    for year in range(1, horizon + 1):
        revenue *= (1 + growth)
        ebitda = revenue * ebitda_margin
        discounted = ebitda / ((1 + discount) ** year)
        cash_flows.append(discounted)

    terminal_value = (ebitda * (1 + terminal_growth)) / (discount - terminal_growth)
    terminal_discounted = terminal_value / ((1 + discount) ** horizon)

    dcf_valuation = sum(cash_flows) + terminal_discounted

    vc_exit = revenue * inputs['exit_multiple']
    vc_today = vc_exit / ((1 + inputs['irr'] / 100) ** horizon)

    multiple_val = None
    if inputs['metric_type'] == 'Revenue':
        multiple_val = revenue * inputs['peer_multiple']
    else:
        ebitda = revenue * ebitda_margin
        multiple_val = ebitda * inputs['peer_multiple']

    return {
        "DCF Valuation (₹)": round(dcf_valuation, 2),
        "VC Method Valuation (₹)": round(vc_today, 2),
        "Multiples Valuation (₹)": round(multiple_val, 2)
    }
