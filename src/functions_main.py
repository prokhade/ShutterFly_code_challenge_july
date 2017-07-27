import os
from event_class import Customer, SiteVisit, Image, Order
from collections import defaultdict
from datetime import datetime, timedelta
from contextlib import redirect_stdout
from functions_support import get_start_day_of_week, date_validation, currency_validation, is_number, key_validation, print_output
import globals
from exceptions_class import EventDoesNotExist, UndefinedVerb


# Global Lists to maintain keys of each event to handle duplicate events
customer_key_list = []
site_visit_key_list = []
image_key_list = []
order_key_list = []


def injest(event, dict_customers):
    """
    Function definition to create each event as its respective class instance and
    load into in-memory Data Structure (dict_customers) w.r.t its customer
    :param event: event to be ingested
    :param dict_customers: in memory data structure to store events
                           (dictionary with values as list of instances of respective classes)
    :return: None
    """
    global customer_key_list
    global site_visit_key_list
    global image_key_list
    global order_key_list

    try:
        # Unwrap 'CUSTOMER' event attributes into temp variables
        if event['type'] == 'CUSTOMER':
            type = event['type']
            key = event['key']
            verb = event['verb']
            event_time = event['event_time']
            last_name = event['last_name']
            adr_city = event['adr_city']
            adr_state = event['adr_state']

            if verb == 'NEW':
                # Handle duplicate Customer event
                if key not in customer_key_list:
                    # Date validation
                    date_validation(event_time, key)
                    # key vaidation
                    key_validation(key)

                    customer_key_list.append(key)

                    # create a dictionary w.r.t customer_id which stores values as list
                    dict_customers[key] = defaultdict(list)

                    # Create Customer class instance by passing unwrapped values
                    customer = Customer(key, verb, event_time, last_name, adr_city, adr_state)

                    # Load the event instance as value to customer_id key in dict_customers
                    dict_customers[key]['CUSTOMER'].append(customer)
                    dict_customers[key]['ORDERS_TOTAL'].append(float(0))
                    print('CUSTOMER event with key id : {0} INGESTED'.format(key))
                else:
                    print('CUSTOMER event with key id : {0} already exists'.format(key))

            # if verb is 'UPDATE' then update the values of existing customer's attributes
            elif verb == 'UPDATE':
                if key in customer_key_list:
                    # Date validation
                    date_validation(event_time, key)
                    customer = dict_customers[key]['CUSTOMER'][0]
                    customer.last_name = last_name
                    customer.adr_city = adr_city
                    customer.adr_state = adr_state
                    customer.update_time = event_time
                    print('CUSTOMER event with key id : {0} UPDATED'.format(key))
                else:
                    raise EventDoesNotExist(type, key)
            else:
                raise UndefinedVerb(verb, type, key)

        # Unwrap 'SITE_VISIT' event attributes into temp variables
        if event['type'] == 'SITE_VISIT':
            type = event['type']
            key = event['key']
            verb = event['verb']
            event_time = event['event_time']
            customer_id = event['customer_id']
            tags = event['tags']

            # Handle verb
            if verb == 'NEW':
                # Handle duplicate site visit event
                if key not in site_visit_key_list:
                    # Date validation
                    date_validation(event_time, customer_id, key)
                    # key vaidation
                    key_validation(key)

                    site_visit_key_list.append(key)

                    # If the customer_id is new, then create a dictionary w.r.t customer_id which stores values as list
                    if customer_id not in dict_customers:
                        dict_customers[customer_id] = defaultdict(list)

                    # Create Site_visit class instance by passing unwrapped values
                    site_visit = SiteVisit(key, verb, event_time, customer_id, tags)

                    # Load the event instance as value to customer_id key in dict_customers
                    dict_customers[customer_id]['SITE_VISIT'].append(site_visit)
                    print('SITE_VISIT event with key id : {0} INGESTED'.format(key))
                else:
                    print(' SITE_VISIT event with key id : {0} already exists'.format(key))
            else:
                raise UndefinedVerb(verb, type, key)

        # Unwrap 'IMAGE' event attributes into temp variables
        if event['type'] == 'IMAGE':
            type = event['type']
            key = event['key']
            verb = event['verb']
            event_time = event['event_time']
            customer_id = event['customer_id']
            camera_make = event['camera_make']
            camera_model = event['camera_model']

            # Handle duplicate image event and foreign key reference of customer_Id to key of customer event
            if verb == 'UPLOAD':
                if key not in image_key_list:
                    # Date validation
                    date_validation(event_time, customer_id, key)
                    # key vaidation
                    key_validation(key)

                    image_key_list.append(key)

                    # If the customer_id is new, then create a dictionary w.r.t customer_id which stores values as list
                    if customer_id not in dict_customers:
                        dict_customers[customer_id] = defaultdict(list)

                    # Create Image class instance by passing unwrapped values
                    image = Image(key, verb, event_time, customer_id, camera_make, camera_model)

                    # Load the event instance as value to customer_id key in dict_customers
                    dict_customers[customer_id]['IMAGE'].append(image)
                    print('IMAGE event with key id : {0} INGESTED'.format(key))
                else:
                    print('IMAGE event with key id : {0} already exists'.format(key))
            else:
                raise UndefinedVerb(verb, type, key)

        # Unwrap 'ORDER' event attributes into temp variables
        if event['type'] == 'ORDER':
            type = event['type']
            key = event['key']
            verb = event['verb']
            event_time = event['event_time']
            customer_id = event['customer_id']
            total_amount = event['total_amount']

            if verb == 'NEW':
                # Handle duplicate site visit event and foerign key validation of customer_Id
                if key not in order_key_list:
                    # Date validation
                    date_validation(event_time, customer_id, key)
                    # key vaidation
                    key_validation(key)
                    # Currency Validation
                    currency_validation(total_amount, customer_id, key)

                    order_key_list.append(key)

                    # If the customer_id is new, then create a dictionary w.r.t customer_id which stores values as list
                    if customer_id not in dict_customers:
                        dict_customers[customer_id] = defaultdict(list)

                    # Create Order class instance by passing unwrapped values
                    order = Order(key, verb, event_time, customer_id, total_amount)

                    # Load the event instance as value to customer_id key in dict_customers
                    dict_customers[customer_id]['ORDER'].append(order)
                    dict_customers[customer_id]['ORDERS_TOTAL'][0] += float(total_amount.split(' ')[0].strip())
                    print('ORDER event with key id : {0} INGESTED'.format(key))
                else:
                    print('ORDER event with key id : {0} already exists'.format(key))

            # if verb is 'UPDATE' then update the values of existing customer's order amount
            elif verb == 'UPDATE':
                if key in order_key_list:
                    orders_list = dict_customers[customer_id]['ORDER']
                    for order in orders_list:
                        old_total_amount = float(order.total_amount.split(' ')[0].strip())
                        if order.key == key:
                            dict_customers[customer_id]['ORDERS_TOTAL'][0] -= old_total_amount
                            order.total_amount = total_amount
                            order.update_time = event_time
                            dict_customers[customer_id]['ORDERS_TOTAL'][0] += float(total_amount.split(' ')[0].strip())
                            print('ORDER event with key id : {0} UPDATED'.format(key))
                else:
                    raise EventDoesNotExist(type, key)
            else:
                raise UndefinedVerb(verb, type, key)
    except EventDoesNotExist as e:
        print(e.msg)
        exit(1)
    except UndefinedVerb as e:
        print(e.msg)
        exit(1)


def update_missing_values_and_set_start_end_week(dict_customers):
    """
    Function definition to update missing values order total_amount and also to calculate the no_of_weeks (span of weeks
    for which the data is available in the input files)
    :param dict_customers: in memory data structure to store events
                           (dictionary with values as list of instances of respective classes)
    :return: None
    """
    end_date = None
    for customer_id in dict_customers.keys():
        orders_list = dict_customers[customer_id]['ORDER']
        orders_sum = dict_customers[customer_id]['ORDERS_TOTAL'][0]
        if orders_list is not None:
            no_of_orders = len(orders_list)
            for order in orders_list:
                # update order missing total amount
                total_amount = order.total_amount.split(' ')[0].strip()
                if not is_number(total_amount) or total_amount == 0:
                    total_amount = orders_sum/no_of_orders
                    order.total_amount = str(total_amount) + ' ' + order.total_amount.split(' ')[1]

        site_visits_list = dict_customers[customer_id]['SITE_VISIT']
        start_date = None
        if site_visits_list is not None:
            for site_visit in site_visits_list:
                # set start_date and end_date
                dt = datetime.strptime(site_visit.event_time, '%Y-%m-%d:%H:%M:%S.%fZ').date()
                if start_date is None or dt < start_date:
                    start_date = dt
                if end_date is None or dt > end_date:
                    end_date = dt
        if start_date is not None:
            start_week = get_start_day_of_week(start_date)
            dict_customers[customer_id]['start_week'].append(start_week)

    if end_date is not None:
        globals.end_week = get_start_day_of_week(end_date) + timedelta(days=7)


def topXSimpleLTVCustomers(x, dict_customers):
    """
    Function to calculate top X Customers with highest LTV value
    :param x: paramater x for top'X'
    :param dict_customers: in memory data structure to store events
                           (dictionary with values as list of instances of respective classes)
    :return: dictionary containing customer_id: LTV pair of top X customers
    """
    # Error Handling if X is greater than the No. of customers present in the file
    try:
        if x > len(dict_customers):
            raise ValueError
    except ValueError:
        print('Error: X is greater than the No. of customers present in the file')
        exit(1)

    # As mentioned in the README, I have taken avg. Liefspan of a ShutterFly customer as 10 years
    t = 10
    # Dictionary to store LTV vales w.r.t. each customer
    customer_LTV_dict = {}
    for customer_id in dict_customers.keys():
        # get the total customer expenditure from value of 'ORDERS_TOTAL' key of respective customer
        total_customer_exp = dict_customers[customer_id]['ORDERS_TOTAL'][0]

        # Initialize No. of Site Visits variable
        no_of_site_visits = 0

        customer_start_week = dict_customers[customer_id]['start_week'][0]
        if globals.end_week is not None and customer_start_week is not None:
            no_of_weeks = int(abs((globals.end_week - customer_start_week).days/7))
        else:
            no_of_weeks = 0

        # Calculate No. of site visits
        # Get the site visits list for respective customer
        site_visits_list = dict_customers[customer_id].get('SITE_VISIT', None)

        # Check if site_visits_list exist for that customer
        if site_visits_list is not None:
            no_of_site_visits = len(site_visits_list)

        # Handling DivideByZero error
        if no_of_site_visits != 0 and no_of_weeks != 0:
            # Calculating Avg. Site Visits per Week
            site_visits_per_week = no_of_site_visits/no_of_weeks
            # Calculating Avg. Customer Expenditure per Visit
            customer_exp_per_visit = total_customer_exp/no_of_site_visits
            # Calculating 'a' as per formula given
            a = customer_exp_per_visit * site_visits_per_week
            # Calculating Simple LTV for respective customer
            simple_LTV = 52 * a * t
        else:
            simple_LTV = 0

        # Adding LTV value to dictionary w.r.t. Customer_ID
        customer_LTV_dict[customer_id] = simple_LTV

    # Getting Top X Customers having highest SimpleLTV
    sorted_customers = sorted(customer_LTV_dict.items(), key=lambda y: y[1], reverse=True)
    output_file = os.path.join(globals.output_path, 'output.txt')
    with open(output_file, 'w') as of:
        with redirect_stdout(of):
            print()
            print('customers with respective Simple Lifetime Value')
            print()
            print_output(sorted_customers)

    topX_customers = sorted_customers[:x]

    return topX_customers

