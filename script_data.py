import csv
from collections import defaultdict

def read_filters_from_csv(file_path):
    filters_dict = defaultdict(list)
    
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            center = row['center']
            filter_value = row['filter']
            filters_dict[center].append(filter_value)
    
    return dict(filters_dict)

# Read data from data.csv
filters_dict = read_filters_from_csv('data.csv')
print(filters_dict)

