from datetime import datetime, timedelta
import re


def key_validation(key):
    """
    Function definition to validate key
    :param key: key(id) to be validated
    :return: None (if key is not valid then it exits the program with exit code 1 and error)
    """
    try:
        if re.match('^[a-z0-9]{12,}$', key) is None:
            raise ValueError
    except ValueError:
        print('{0} is invalid key'.format(key))
        exit(1)


# Function definition for date validation
def date_validation(date_str, customer_id, key=None):
    """
    Function definition to validate date.
    :param date_str: event_time (in the form of string)
    :param customer_id: respective customer id
    :param key: respective key id
    :return: None (if event_time is not valid then it exits the program with exit code 1 and error)
    """
    try:
        if key is None:
            key = customer_id
        datetime.strptime(date_str, '%Y-%m-%d:%H:%M:%S.%fZ')
    except ValueError:
        print("Error: Incorrect date or format for customer:", customer_id, 'in event key:', key)
        exit(1)


# Function definition for currency validation
def currency_validation(amount, customer_id, key):
    """
    Function definition to validate currency
    :param amount: attribute orders.total_amount
    :param customer_id: respective customer id
    :param key: respective key
    :return: None (if currency is not valid then it exits the program with exit code 1 and error)
    """
    try:
        currency = amount.split(' ')[1].strip()
        if currency != 'USD':
            raise ValueError
    except ValueError:
        print('Error: Currency not in USD for', customer_id, 'in event key:', key)
        exit(1)


def is_number(s):
    """
    Function definition to check if the numeric part of order.total_amount is of type float
    :param s: numeric part of order.total_amount
    :return: Boolean value : True/False
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_start_day_of_week(dt):
    """
    Function definition to get start day of the week for a given date
    ** I have considered a week to start from Monday and end on Sunday
    ** as the default date.weekday() in python points to Monday as start day
    :param dt: date part of event_time
    :return: start day of week
    """
    start = dt - timedelta(days=dt.weekday())
    return start


def print_output(LTV_customers):
    """
    Function definition for printing in tabular format
    :param topX_LTV_customers: dictionary containing top x customer_id : LTV key value pair
    :param dict_customers: in memory data structure to store events
                           (dictionary with values as list of instances of respective classes)
    :return: None
    """
    padding = 15
    x = len(LTV_customers)
    # print header
    header = ['Rank', 'Customer_ID', 'SimpleLTV (USD)']
    print(header[0], (5-len(header[0]))*' ', header[1], (padding-len(header[1]))*' ', header[2])
    print(56*'-')
    rank = 0
    for pair in LTV_customers:
        rank += 1
        customer_id = pair[0]
        simpleLTV = format(pair[1], '.2f')
        print(rank, (5-len(str(rank)))*' ', customer_id, (padding-len(customer_id))*' ', '$'+simpleLTV)
