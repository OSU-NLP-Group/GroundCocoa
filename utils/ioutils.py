# Author: Harsh Kohli
# Date Created: 17-12-2023

import csv
import json
from constants import *


def get_busiest_airport_codes():
    busiest_airports, iata_to_country = [], {}
    with open(busiest_airport_file, 'r', encoding='utf8') as csvfile:
        airport_data = csv.reader(csvfile, delimiter=',', quotechar='"')
        for index, row in enumerate(airport_data):
            if index == 0:
                continue
            iata = row[5].split("/")[0]
            country = row[4]
            iata_to_country[iata] = country
            busiest_airports.append(iata)
    return busiest_airports, iata_to_country


def write_to_json(data, file_name):
    with open(file_name, "w", encoding='utf8') as outfile:
        json.dump(data, outfile)


def read_from_json(file_name):
    f = open(file_name, 'r', encoding='utf8')
    data = json.load(f)
    return data
