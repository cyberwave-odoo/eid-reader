from datetime import datetime

"""
The date of birth is written to the card in a localized format. This
means we need to read it from the card, parse it, and then convert it
to the same format in the language of the current user.

Clearly someone never heard of ISO 8601

"""

month_dict = {
    'JAN': 1,
    'FEB': 2,
    'MÄR': 3,
    'APR': 4,
    'MAI': 5,
    'JUN': 6,
    'JUL': 7,
    'AUG': 8,
    'SEP': 9,
    'OKT': 10,
    'NOV': 11,
    'DEZ': 12,
    'JAN': 1,
    'FEV': 2,
    'MARS': 3,
    'AVR': 4,
    'MAI': 5,
    'JUIN': 6,
    'JUIL': 7,
    'AOUT': 8,
    'SEPT': 9,
    'OCT': 10,
    'NOV': 11,
    'DEC': 12,
    'JAN': 1,
    'FEB': 2,
    'MAAR': 3,
    'APR': 4,
    'MEI': 5,
    'JUN': 6,
    'JUL': 7,
    'AUG': 8,
    'SEP': 9,
    'OKT': 10,
    'NOV': 11,
    'DEC': 12,
    'JAN': 1,
    'FEB': 2,
    'MAR': 3,
    'APR': 4,
    'MAY': 5,
    'JUN': 6,
    'JUL': 7,
    'AUG': 8,
    'SEP': 9,
    'OCT': 10,
    'NOV': 11,
    'DEC': 12
}

def fix_date(string) :
    
    date = str.split(string)
    return datetime.strptime(date[0] + " " + str(month_dict[date[1]]) + " " + date[2], '%d %m %Y').date()