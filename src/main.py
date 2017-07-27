import simplejson as json
import sys
import os
import time
import globals
from functions_main import injest, topXSimpleLTVCustomers, update_missing_values_and_set_start_end_week
from functions_support import print_output
from contextlib import redirect_stdout


# ----------------------------MAIN--------------------------------------

# Calculate run time
start = time.time()

# Initialize global variables
globals.init()

# in memory Data Structure (Dictionary) which stores events (class instances) w.r.t each customer
dict_customers = {}

# create a list of input files (files from input directory)
os.chdir(globals.input_path)
input_files = [file for file in os.listdir(globals.input_path) if os.path.isfile(file) and file.endswith('.txt') and os.path.getsize(file) > 0]

# Input arguments :
# argv[1] -> x (for top X customers)
x = int(sys.argv[1])

# Open each json file and load into dict_customers global Data Structure
print('------DATA INGESTION------')
print()
for file in input_files:
    with open(file) as json_file:
        json_object = json.load(json_file)

    print('INGESTING file: {0}'.format(file))
    print()
    for event in json_object:
        # Function call to injest each event into dict_customers
        injest(event, dict_customers)
    print()
print('-------INGESTION COMPLETE-------')
print()

os.chdir(globals.src_path)

# dict customers is empty if INPUT file/files is/are empty or the input directory does not have any files
if len(dict_customers) > 0:
    # Function call to Update missing order.total_amount values and calculate no_of_weeks global variable
    print('-----UPDATING missing values and calculating END WEEK-------')
    update_missing_values_and_set_start_end_week(dict_customers)
    print('-----UPDATE COMPLETE-----')
    print()

    # Function call to calculate top X highest LTV customers (function def in 'functions_main.py' file)
    print('------CALCULATING TOP X CUSTOMERS-------')
    topX_customers = topXSimpleLTVCustomers(x, dict_customers)

    # redirect print output to output file
    output_file = os.path.join(globals.output_path, 'output.txt')
    with open(output_file, 'a') as of:
        with redirect_stdout(of):
            print()
            print('Top {0} customers with the highest Simple Lifetime Value'.format(x))
            print()
            print_output(topX_customers)
    print('------OUTPUT available in /output/output.txt------')
    print()

    # print run time
    print('Run time: {0}'.format(round(time.time() - start, 3)))
    print()

    print('*****PROCESS COMPLETED SUCCESSFULLY*****')
else:
    print('INPUT file/files is/are empty or the input directory does not have any files')
    exit(1)
