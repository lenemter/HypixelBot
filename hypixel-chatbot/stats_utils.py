def format_number(number):
    return '{:,}'.format(number).replace(',', ' ')

def format_date(date):
    return date.strftime('%d.%m.%Y %H:%M:%S')