# settlement_app/calculations.py
from datetime import date, timedelta

# Define rating systems per council
COUNCIL_RATING_SYSTEMS = {
    "Auckland Council": "quarterly",
    "Bay of Plenty Regional Council": "annual",
    "Carterton District Council": "quarterly",
    #"Far North District Council": "annual",
    #"Wellington City Council": "annual",
    #"Whangarei District Council": "six-monthly",
    #"Christchurch City Council": "six-monthly",
    #"Hamilton City Council": "quarterly",
    "Tauranga City Council": "six-monthly",
    #"Dunedin City Council": "annual",
    #"Auckland Regional Council": "annual",
    "Kawerau District Council": "quarterly",
    "Opotiki District Council": "six-monthly",
    "Rotorua District Council": "quarterly",
    "Taupo District Council": "quarterly", #doing 3 quarterly periods until 30 June 2025
    #"Wellington Regional Council": "annual",
    "Waikato Regional Council": "annual",
    "Western Bay of Plenty District Council": "six-monthly",
    #"Canterbury Regional Council": "six-monthly",
    #"Waikato Regional Council": "quarterly",
    "Whakatane District Council": "quarterly",

    #"Otago Regional Council": "annual",
}

# Fixed quarter and half-year dates
# Create a list of quarters, and a list of half-years.
# the "date" tuple is represented by:
# - the year in the date (hardcoded to 1 because it doesn't matter)
# - the month 
# - the day of the month
# so (1, 7, 1) represents 1 July

# QUARTERS
# Q1 = 1 Jul - 30 Sep
# Q2 = 1 Oct - 31 Dec
# Q3 = 1 Jan - 31 Mar
# Q4 = 1 Apr - 30 Jun

QUARTERS = [
    (date(1, 7, 1), date(1, 9, 30)),
    (date(1, 10, 1), date(1, 12, 31)),
    (date(1, 1, 1), date(1, 3, 31)),
    (date(1, 4, 1), date(1, 6, 30))
]

# HALF-YEARS
# H1 = 1 Jul - 31 Dec
# H2 = 1 Jan - 30 Jun

HALF_YEARS = [
    (date(1, 7, 1), date(1, 12, 31)),
    (date(1, 1, 1), date(1, 6, 30))
]

# a leap year has an extra day (Feb 29th) so it has 366 days instead of 365
# a leap years is divisible by 4, but if yes, and it's also divisble by 100, it must be divisible by 400
# 2028 (the next leap year) is divisible by 4, so it will return true

def is_rating_leap_year(start_year):
    """Given the start year of the rating year (July 1 - June 30),
    determine if the rating year includes a leap day (Feb 29). We test if the second year is a leap year."""
    second_year = start_year + 1  # because Feb 29 would be in the next calendar year
    return second_year % 4 == 0 and (second_year % 100 != 0 or second_year % 400 == 0)

# this function finds the period (quarter or half-year) that the settlement date falls into
# it takes the settlement date and the list of periods (quarters, half-years)
# it calculates the real start and end dates using the actual settlement year (e.g. 2028 is a leap year)
# it loops through the periods, checking if the settlement date falls on or between each period's start and end dates
# if yes, then it returns the period's start and end dates
# if no, then return the first period of the next rating year

def find_period(date_of_settlement, periods):
    # periods = list of (start, end) relative to year 1
    for start, end in periods:
        real_start = start.replace(year=date_of_settlement.year)
        real_end = end.replace(year=date_of_settlement.year)
        if real_start <= date_of_settlement <= real_end:
            return real_start, real_end
    # If none match, it's the first period of the next year
    first_start, first_end = periods[0]
    return first_start.replace(year=date_of_settlement.year), first_end.replace(year=date_of_settlement.year)

# this function calculates the portions based on the rating system (quarterly, 6-monthly, annual)
# first, check if it's a leap year. If yes, use 366 days, otherwise use 365. NOTE THIS VARIABLE IS NOT CURRENTLY USED IN THE FUNCTION
# second, check the rating system:
# -- annual: daily rate = annual rates / # of days in the year
# -- 6-monthly: daily rate = annual rates / 2 instalments / # of days in the applicable 6-month period
# -- quarterly: daily rate = annual rates / 4 instalments / # of days in the applicable quarter

# this function calculates the vendor and purchaser portions for a single installment
# it takes the yearly rates, the settlement date, the rating system, and whether the vendor pays to the end of the installment

def calculate_single_apportionment(yearly_rates, settlement_date, rating_system, installment_paid=True):
    year_days = 366 if is_rating_leap_year(settlement_date.year) else 365
    
    if rating_system == "annual":
        # If the settlement date is between January 1 and June 30, use the previous year's July 1 as the start
        if settlement_date.month >= 1 and settlement_date.month <= 6:
            period_start = date(settlement_date.year - 1, 7, 1)
            period_end = date(settlement_date.year, 6, 30)  # End date is 30 June of the current year
        else:
            period_start = date(settlement_date.year, 7, 1)
            period_end = date(settlement_date.year + 1, 6, 30)  # End date is 30 June of the next year
        
        days_in_period = (period_end - period_start).days + 1
        daily_rate = yearly_rates / days_in_period

    elif rating_system == "six-monthly":
        period_start, period_end = find_period(settlement_date, HALF_YEARS)
        days_in_period = (period_end - period_start).days + 1
        daily_rate = (yearly_rates / 2) / days_in_period

    elif rating_system == "quarterly":
        period_start, period_end = find_period(settlement_date, QUARTERS)
        days_in_period = (period_end - period_start).days + 1
        daily_rate = (yearly_rates / 4) / days_in_period

    else:
        raise ValueError("Unknown rating system.")

 # calculate # of vendor days vs. purchaser days
 # vendor days are plus 1 because they are inclusive of the settlement date
 # purchaser days are minus 1 because they exclude the settlement date
 
    vendor_days = (settlement_date - period_start).days + 1
    purchaser_days = (period_end - settlement_date).days 

# this function returns vendor and purchaser portions
# multiply the # of vendor or purchaser days by the daily rate, rounded to 2 decimal places

    vendor_amount = round(vendor_days * daily_rate, 2)
    purchaser_amount = round(purchaser_days * daily_rate, 2)


    return vendor_days, vendor_amount, purchaser_days, purchaser_amount, installment_paid

# this function returns the vendor and purchaser portions for local and regional council rates
# it takes the user inputs and calls the functions above it

def calculate_apportionments(local_council, local_yearly_rates, regional_council, regional_yearly_rates, settlement_date, local_installment_paid, regional_installment_paid):
    local_rating_system = COUNCIL_RATING_SYSTEMS.get(local_council, "annual")
    regional_rating_system = COUNCIL_RATING_SYSTEMS.get(regional_council, "annual")

    local_vendor_days, local_vendor_amount, local_purchaser_days, local_purchaser_amount, local_installment_paid = calculate_single_apportionment(local_yearly_rates, settlement_date, local_rating_system, local_installment_paid)
    regional_vendor_days, regional_vendor_amount, regional_purchaser_days, regional_purchaser_amount, regional_installment_paid = calculate_single_apportionment(regional_yearly_rates, settlement_date, regional_rating_system, regional_installment_paid)

    return {
        "local": {
            "vendor_days": local_vendor_days,
            "vendor_amount": local_vendor_amount,
            "purchaser_days": local_purchaser_days,
            "purchaser_amount": local_purchaser_amount,
            "installment_paid": local_installment_paid
        },
        "regional": {
            "vendor_days": regional_vendor_days,
            "vendor_amount": regional_vendor_amount,
            "purchaser_days": regional_purchaser_days,
            "purchaser_amount": regional_purchaser_amount,
            "installment_paid": regional_installment_paid
        }
    }

