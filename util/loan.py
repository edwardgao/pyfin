# Utility functions for loan computation.


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

