# Utility functions for loan computation.
import collections

def monthly_payment(monthly_rate, terms, principal):
  payment = principal * (
      monthly_rate * (
        1 + monthly_rate) ** terms) / (
            (1 + monthly_rate) ** terms - 1)
  return payment


def remaining_balance(monthly_rate, terms, principal,
                      after_n_th_payment):
  L = principal
  n = terms
  c = monthly_rate
  p = after_n_th_payment
  B = L * ((1 + c) ** n - (1 + c) ** p) / ((1 + c) **n - 1)
  return B

def total_interest_paid(monthly_rate, terms, principal,
                        after_n_th_payment):
  principal_paid = principal - remaining_balance(
      monthly_rate, terms, principal, after_n_th_payment)
  total_paid = monthly_payment(
      monthly_rate, terms, principal) * after_n_th_payment
  interest_paid = total_paid - principal_paid
  return interest_paid

MonthState = collections.namedtuple("MonthState", " ".join(["month",
  "interest_paid", "principal_paid", "principal_remain", "hoa", "property_tax",
  "depreciation", "total_depreciation", "upkeeping_paid",
  "total_upkeeping_paid", "rental_income", "net_cost", "insurance", "total_insurance",
  "total_interest_paid", "total_pricipal_paid", "total_hoa_paid",
  "total_property_tax_paid", "cash_flow", "total_net_cash_flow", "after_tax_cash_flow",
  "tax_saving", "property_value", "cost_if_sold", "total_tax_saving",
  "capital_gain_if_sold", "tax_if_sold", "net_proceeding_after_tax",
  "total_net_gain_loss", "roi", "annualized_roi"]))

def full_amortize_table(monthly_rate, terms, principal, down_payment,
                        property_value, annual_appreciation,
                        hoa, hoa_annual_growth, property_tax_rate,
                        personal_tax_marginal_rate,
                        capital_gain_marginal_rate,
                        sale_cost_ratio, structure_value,
                        monthly_insurance, annual_insurance_increase,
                        upkeeping_ratio, initial_rental, vacancy_rate,
                        annual_rental_increase,
                        property_tax_annual_growth_cap=-1):
  full_table = []
  last_month = MonthState(
    month=0,
    interest_paid=0,
    principal_paid=0,
    principal_remain=principal,
    hoa=0,
    property_tax=0,
    insurance=0,
    total_insurance=0,
    depreciation=0,
    total_depreciation=0,
    upkeeping_paid=0,
    total_upkeeping_paid=0,
    rental_income=0,
    total_interest_paid=0,
    total_pricipal_paid=0,
    total_hoa_paid=0,
    total_property_tax_paid=0,
    cash_flow=0,
    after_tax_cash_flow=0,
    total_net_cash_flow=-down_payment,
    tax_saving=0,
    net_cost=0,
    property_value=property_value,
    cost_if_sold=property_value * sale_cost_ratio,
    total_tax_saving=0,
    capital_gain_if_sold=0,
    tax_if_sold=0,
    net_proceeding_after_tax=property_value - principal - property_value * sale_cost_ratio,
    total_net_gain_loss=down_payment - (property_value - principal - property_value * sale_cost_ratio),
    roi=(down_payment - (property_value - principal - property_value * sale_cost_ratio))/down_payment,
    annualized_roi=(down_payment - (property_value - principal - property_value * sale_cost_ratio))/down_payment
  )
  # full_table.append(last_month)
  # Never change
  payment = monthly_payment(monthly_rate, terms, principal)
  for i in range(int(terms)):
    month = last_month.month + 1
    balance = remaining_balance(monthly_rate, terms, principal, month)
    principal_paid = last_month.principal_remain - balance
    interest_paid = payment - principal_paid
    new_hoa = hoa * ((1 + hoa_annual_growth) ** int((month - 1) / 12))
    new_property_value = property_value * ((1 + annual_appreciation) ** int((month - 1) / 12))
    property_tax = new_property_value * property_tax_rate
    if (property_tax_annual_growth_cap > 0):
      new_property_value_cap = property_value * ((1 + property_tax_annual_growth_cap) ** int((month - 1) / 12))
      if new_property_value_cap < new_property_value:
        property_tax = new_property_value_cap * property_tax_rate
    
    depreciation = structure_value / (38.5) / 12
    total_depreciation = last_month.total_depreciation + depreciation
    upkeeping_paid = upkeeping_ratio * new_property_value / 12
    total_upkeeping_paid = last_month.total_upkeeping_paid + upkeeping_paid
    rental_income = initial_rental * ((1 + annual_rental_increase) ** int((month - 1) / 12)) * vacancy_rate
    total_interest_paid = last_month.total_interest_paid + interest_paid
    total_pricipal_paid = principal - balance
    total_hoa_paid = last_month.total_hoa_paid + new_hoa
    total_property_tax_paid = last_month.total_property_tax_paid + property_tax
    insurance = monthly_insurance * ((1 + annual_insurance_increase) ** int((month - 1) / 12))
    total_insurance = last_month.total_insurance + insurance
    net_cost = property_tax + depreciation + upkeeping_paid + interest_paid + hoa + insurance
    taxable_gain_loss = rental_income - net_cost
    tax_saving = - taxable_gain_loss * personal_tax_marginal_rate
    cash_flow = rental_income - property_tax - payment + tax_saving - hoa - insurance - upkeeping_paid
    after_tax_cash_flow = cash_flow + tax_saving
    total_net_cash_flow = last_month.total_net_cash_flow + after_tax_cash_flow
    total_tax_saving = last_month.total_tax_saving + tax_saving
    cost_basic = property_value - total_depreciation # upkeeping is deducted, not investment
    cost_if_sold = new_property_value * sale_cost_ratio
    capital_gain_if_sold = new_property_value - cost_if_sold - cost_basic
    tax_if_sold = max(0, capital_gain_if_sold) * capital_gain_marginal_rate
    net_proceeding_after_tax=new_property_value - cost_if_sold - tax_if_sold - balance
    total_net_gain_loss = total_net_cash_flow + net_proceeding_after_tax
    roi = total_net_gain_loss / float(down_payment)
    if roi < -1:
      annualized_roi = -1
    else:
      annualized_roi = abs(1+roi) ** (1 / (month / 12)) - 1.0
    new_month = MonthState(
      month=month,
      interest_paid=interest_paid,
      principal_paid=principal_paid,
      principal_remain=balance,
      hoa=new_hoa,
      insurance=insurance,
      total_insurance=insurance,
      property_tax=property_tax,
      depreciation=depreciation,
      total_depreciation=total_depreciation,
      upkeeping_paid=upkeeping_paid,
      total_upkeeping_paid=total_upkeeping_paid,
      rental_income=rental_income,
      total_interest_paid=total_interest_paid,
      total_pricipal_paid=total_pricipal_paid,
      total_hoa_paid=total_hoa_paid,
      total_property_tax_paid=total_property_tax_paid,
      net_cost=net_cost,
      cash_flow=cash_flow,
      after_tax_cash_flow=after_tax_cash_flow,
      total_net_cash_flow=total_net_cash_flow,
      tax_saving=tax_saving,
      property_value=new_property_value,
      cost_if_sold=cost_if_sold,
      total_tax_saving=total_tax_saving,
      capital_gain_if_sold=capital_gain_if_sold,
      tax_if_sold=tax_if_sold,
      net_proceeding_after_tax=net_proceeding_after_tax,
      total_net_gain_loss=total_net_gain_loss,
      roi=roi*100,
      annualized_roi=annualized_roi*100
    )
    full_table.append(new_month)
    last_month = new_month
  return full_table