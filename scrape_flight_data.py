# Author: Harsh Kohli
# Date Created: 17-12-2023

import random
from constants import flight_options_file
from utils.scraping_utils import scrape_data, stitch_together
from utils.ioutils import get_busiest_airport_codes, write_to_json

date, return_date = '2024-06-17', '2024-06-28'

classes = ['Economy', 'Business', 'First']
busiest_codes, iata_to_country = get_busiest_airport_codes()
num_pairs = 50
flight_options = {}

while len(flight_options) < num_pairs:
    src, dest = random.choice(busiest_codes), random.choice(busiest_codes)
    if src == dest:
        continue
    c1, c2 = iata_to_country[src], iata_to_country[dest]
    if c1 == c2:
        continue

    print('Flights scraped for ' + str(len(flight_options)) + ' src-dest pairs')
    try:
        all_class_flights = []
        for flight_class in classes:
            new_features, old_features, layovers = scrape_data(src, dest, date, return_date, flight_class)
            all_flights_info = stitch_together(new_features, old_features, layovers, flight_class, src, dest, date)
            all_class_flights.extend(all_flights_info)

        if len(all_class_flights) < 10:
            continue

        flight_options[src + '_' + dest] = all_class_flights
    except:
        print('Something went wrong for pair: ' + src + '-' + dest)

write_to_json(flight_options, flight_options_file)
