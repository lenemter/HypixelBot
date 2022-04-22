def format_number(number):
    return '{:,}'.format(number).replace(',', ' ')

def format_date(date):
    return date.strftime('%d.%m.%Y %H:%M')

def round_number(number):
    return round(number, 2)