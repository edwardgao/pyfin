class ReturnOfRealEstate(object):
  """
  Computing ROI of real estate investment.
  Parameters of real estate investment:
  1. Purchase price.
  2. Loan amount.
  3. Closing Cost.
  4. Interest Rate.
  5. Property Tax. (A function of initial tax or a function of appreciation).
  6. HOA.
  7. HOA increase rate.
  8. Appreciation rate (hypo).
  9. Sale cost (tax, agent fee), as proportion of the sale.
  10. Marginal personal tax income rate.
  11. Property type: investment or residence? Different treatment of tax.
  12. Loan Terms (in months).
  13. Structure value.
  14. Rent per month.
  15. Rent increase rate (per year)
  16. Vacancy rate.
  Outputs:
  1. Initial investment.
  2. Cash flow.
  3. Net taxation effect.
  4. Net after tax cash flow.
  5. Net worth of the investment if sold at each month.
  6. ROI of the investment if sold at each month.
  """
  def __init__(self,
               purchase_price,
               loan_amount,
               loan_terms_in_month,
               interest_rate,
               property_tax_func,
               hoa_monthly,
               hoa_increase_rate,
               apprec_rate,
               sale_cost,
               marginal_personal_tax_rate,
               structure_value,
               property_is_investment,
               rent_per_month,
               rent_increase_rate,
               rent_vacancy_rate):
  pass 
