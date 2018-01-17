"""
Script for table tennis rating calculation
"""

import sys
import getopt
import csv
from defaultlist import defaultlist

def delta_calculation(curr_rating, curr_opp_rating, score):
    """
        Calculate delta for rating using information about score
    """
    left, _, right = score.partition(":")
    delta = 0
    if left > right:
        if (curr_rating - curr_opp_rating) >= 100:
            return 0
        delta = (100 - (curr_rating - curr_opp_rating)) / 10
    else:
        if (curr_rating - curr_opp_rating) <= -100:
            return 0
        delta = -(100 - (curr_rating - curr_opp_rating)) / 20
    return delta

def update_rating(source_file, output_file):
    """
    Update rating using information from results table in csv format
    """
    row_count = 0
    results = defaultlist(list)
    with open(source_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            results[row_count] = row
            row_count += 1
    start_column = 3
    curr_rating_column = 1
    is_first_line = True
    for row in results:
        if is_first_line:
            is_first_line = False
            row.append("New rating")
            continue
        curr_rating = float(row[curr_rating_column])
        new_rating = curr_rating
        for i in range(start_column, row_count - 1 + start_column):
            if ':' not in row[i]:
                continue
            score = row[i]
            curr_opp_rating = float(results[i - start_column + 1][curr_rating_column])
            if '+' in row[i]:
                first, _, second = row[i].partition("+")
                new_rating += delta_calculation(curr_rating, curr_opp_rating, first)
                new_rating += delta_calculation(curr_rating, curr_opp_rating, second)
            else:
                new_rating += delta_calculation(curr_rating, curr_opp_rating, score)

        row.append("{:.1f}".format(new_rating))
    with open(output_file, 'w') as outfile:
        wr = csv.writer(outfile, delimiter=',')
        for row in results:
            wr.writerow(row)


def usage():
    """
    Print usage message
    """
    print('table_tennis_rating.py -s <results.csv> -o <results-rating.csv>')

def run_script():
    source_file = ""
    output_file = ""
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hs:o:", ["source=", "output="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-s", "--source"):
            source_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg
    update_rating(source_file, output_file)

if __name__ == "__main__":
    run_script()
