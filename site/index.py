from flask import Flask
from flask import render_template
from flask import request
from util import loan
app = Flask(__name__)

@app.route("/")
def index():
  return "Hello World!"

@app.route('/form/')
@app.route('/form/<name>')
def form(name=None):
  return render_template('form.html', name=name)

@app.route("/calc", methods=['POST'])
def calc():
  price = float(request.form["price"])
  down = float(request.form["down"]) / 100
  rate = float(request.form["interest"]) / 100
  years = float(request.form["years"])
  insurance = float(request.form["insurance"])
  property_tax_rate = float(request.form["propertytax"]) / 100
  hoa = float(request.form["hoa"])

  # Interest and Principal Payment
  p_i = loan.monthly_payment(rate / 12, years * 12, price * (1 - down))
  monthly_payment = "%.2f" % p_i
  # Property tax
  p_t = price * property_tax_rate / 12
  monthly_property_tax = "%.2f" % p_t
  # Insurance
  i_s = insurance / 12
  monthly_insurance = "%.2f" % i_s
  # Monthly cost
  piti = p_i + p_t + i_s + hoa
  monthly_cost = "%.2f" % piti
  # Amortize Table
  full_amortize_table = loan.full_amortize_table(
    monthly_rate=rate / 12,
    terms=years * 12,
    principal=price * (1 - down),
    down_payment=price * down + float(request.form["closing"]),
    property_value=price,
    annual_appreciation=float(request.form["apprec"]) / 100,
    hoa=hoa,
    hoa_annual_growth=float(request.form["hoainc"]) / 100,
    property_tax_rate=property_tax_rate / 12,
    personal_tax_marginal_rate=float(request.form["income_tax"]) / 100,
    capital_gain_marginal_rate=float(request.form["capital_tax"]) / 100,
    sale_cost_ratio=float(request.form["sale_cost"]) / 100,
    structure_value=float(request.form["structurevalue"]),
    monthly_insurance=float(request.form["insurance"]) / 12,
    annual_insurance_increase=float(request.form["insurance_increase"]) / 100,
    upkeeping_ratio=float(request.form["upkeeping"]) / 100,
    initial_rental=float(request.form["monthly_rental"]),
    vacancy_rate=1 - (float(request.form["vacancy_rate"])/100),
    annual_rental_increase=float(request.form["annual_rental_increase"]) / 100,
    property_tax_annual_growth_cap=float(request.form["property_tax_cap"]) / 100
  )

  return render_template('result.html',
      monthly_payment=monthly_payment,
      monthly_property_tax=monthly_property_tax,
      monthly_insurance=monthly_insurance,
      monthly_cost=monthly_cost,
      tb=full_amortize_table)
