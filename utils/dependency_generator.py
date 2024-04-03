# Author: Harsh Kohli
# Date Created: 28-08-2023

import numpy as np
import random
from utils.condition import Condition


def get_airline_condition(flight_data):
    all_airlines = set()
    for one_route in flight_data:
        for one_airline in one_route['Airline'][1:-1].split(','):
            all_airlines.add(one_airline)
    num_airlines = len(all_airlines)
    num_to_avoid = random.choice(range(1, int(num_airlines / 2)))
    num_to_avoid = min(3, num_to_avoid)
    pos_text = 'I only want to travel '
    neg_text = 'I do not want to travel '
    imp_airlines = random.sample(all_airlines, num_to_avoid)
    rest_of_text = ''
    if num_to_avoid == 1:
        rest_of_text = rest_of_text + imp_airlines[0]
    else:
        for one_al in imp_airlines[:-1]:
            rest_of_text = rest_of_text + one_al + ', '
        rest_of_text = rest_of_text + 'and ' + imp_airlines[-1]
    rest_of_text = rest_of_text + ' airlines.'
    pos_text = pos_text + rest_of_text
    neg_text = neg_text + rest_of_text
    condition_obj = Condition('eq', imp_airlines, pos_text, neg_text)
    return condition_obj


def get_ticketclass_condition(flight_data):
    all_classes = set()
    for one_route in flight_data:
        all_classes.add(one_route['TicketClass'])
    pos_text = 'I only want to travel '
    neg_text = 'I do not want to travel '
    rest_of_text = ''

    imp_class = random.choice(list(all_classes))
    rest_of_text = rest_of_text + imp_class.lower()
    rest_of_text = rest_of_text + ' class'

    pos_text = pos_text + rest_of_text
    neg_text = neg_text + rest_of_text
    return Condition('eq', imp_class, pos_text, neg_text)


def get_departuretime_condition(flight_data):
    pos_text = 'I want to leave '
    neg_text = 'I cannot leave '

    rest_of_text = ''
    if random.randint(0, 1) == 0:
        rest_of_text = rest_of_text + 'before '
        cond_type = 'le'
    else:
        rest_of_text = rest_of_text + 'after '
        cond_type = 'ge'
    hours = [str(x) for x in range(10, 21)]
    minutes = ['00', '15', '30', '45']

    hr, min = random.choice(hours), random.choice(minutes)
    imp_time = hr + ':' + min
    rest_of_text = rest_of_text + imp_time
    pos_text = pos_text + rest_of_text
    neg_text = neg_text + rest_of_text
    return Condition(cond_type, imp_time, pos_text, neg_text)


def get_arrivaltime_condition(flight_data):
    pos_text = 'I want to arrive '
    neg_text = 'I do not want to arrive '
    rest_of_text = ''
    if random.randint(0, 1) == 0:
        rest_of_text = rest_of_text + 'before '
        cond_type = 'le'
    else:
        rest_of_text = rest_of_text + 'after '
        cond_type = 'ge'
    hours = [str(x) for x in range(10, 21)]
    minutes = ['00', '15', '30', '45']

    hr, min = random.choice(hours), random.choice(minutes)
    imp_time = hr + ':' + min
    rest_of_text = rest_of_text + imp_time
    pos_text = pos_text + rest_of_text
    neg_text = neg_text + rest_of_text
    return Condition(cond_type, imp_time, pos_text, neg_text)

def get_arrivaltime_between_condition(flight_data):
    pos_text = 'I want to arrive '
    neg_text = 'I do not want to arrive '
    rest_of_text = 'between '
    hours = [str(x) for x in range(6, 20)]
    minutes = ['00', '15', '30', '45']

    hr, min = random.choice(hours), random.choice(minutes)

    new_hours = [str(x) for x in range(int(hr) + 1, 23)]
    hr2, min2 = random.choice(new_hours), random.choice(minutes)


    start_time = hr + ':' + min
    end_time = hr2 + ':' + min2

    rest_of_text = rest_of_text + start_time + ' and ' + end_time
    pos_text = pos_text + rest_of_text
    neg_text = neg_text + rest_of_text
    return Condition('bw', [start_time, end_time], pos_text, neg_text)


def get_departuretime_between_condition(flight_data):
    pos_text = 'I want to depart '
    neg_text = 'I do not want to depart '
    rest_of_text = 'between '
    hours = [str(x) for x in range(6, 20)]
    minutes = ['00', '15', '30', '45']

    hr, min = random.choice(hours), random.choice(minutes)

    new_hours = [str(x) for x in range(int(hr) + 1, 23)]
    hr2, min2 = random.choice(new_hours), random.choice(minutes)

    start_time = hr + ':' + min
    end_time = hr2 + ':' + min2

    rest_of_text = rest_of_text + start_time + ' and ' + end_time
    pos_text = pos_text + rest_of_text
    neg_text = neg_text + rest_of_text
    return Condition('bw', [start_time, end_time], pos_text, neg_text)


def get_traveltime_condition(flight_data):
    all_times = []
    for one_route in flight_data:
        all_times.append(int(one_route['TravelTime'].split('hr')[0].strip()))
    med_time = str(int(np.median(all_times)))

    pos_text = 'Travel time should be '
    neg_text = 'Travel time should not be '

    minutes = random.choice(['00', '15', '30', '45'])

    rest_of_text = ''
    if random.randint(0, 1) == 0:
        rest_of_text = rest_of_text + 'less than '
        cond_type = 'le'
    else:
        rest_of_text = rest_of_text + 'more than '
        cond_type = 'ge'
    rest_of_text = rest_of_text + med_time + ' hours'
    if minutes != '00':
        rest_of_text = rest_of_text + ' and ' + minutes + ' minutes'
    pos_text = pos_text + rest_of_text
    neg_text = neg_text + rest_of_text
    travel_time = med_time + ':' + minutes
    return Condition(cond_type, travel_time, pos_text, neg_text)


def get_num_layovers_condition(flight_data):
    all_layovers = []
    for one_route in flight_data:
        all_layovers.append(int(one_route['NumberOfLayovers']))
    pos_text = 'I want '
    neg_text = 'I do not want '

    rest_of_text = ''
    if random.randint(0, 1) == 0:
        rest_of_text = rest_of_text + 'less than '
        cond_type = 'le'
    else:
        rest_of_text = rest_of_text + 'more than '
        cond_type = 'ge'

    layover_count = random.choice(all_layovers)
    if cond_type == 'le' and layover_count == 0:
        layover_count = 1
    rest_of_text = rest_of_text + str(layover_count) + ' layovers'
    pos_text = pos_text + rest_of_text
    neg_text = neg_text + rest_of_text
    return Condition(cond_type, layover_count, pos_text, neg_text)


def get_emission_diff_condition(flight_data):
    # all_emission_diffs = []
    # for one_route in flight_data:
    #     try:
    #         all_emission_diffs.append(int(one_route['CarbonEmissionAvgDiff(%)']))
    #     except:
    #         all_emission_diffs.append(0)
    #         one_route['CarbonEmissionAvgDiff(%)'] = '0'

    neg_text = 'The average carbon emissions difference should be strictly above average'
    pos_text = 'The average carbon emissions difference should be strictly below average'
    return Condition('eq', 0, pos_text, neg_text)

    # rest_of_text = ''
    # if random.randint(0, 1) == 0:
    #     rest_of_text = rest_of_text + 'less than '
    #     cond_type = 'le'
    # else:
    #     rest_of_text = rest_of_text + 'more than '
    #     cond_type = 'ge'
    # emission_diff = int(random.choice(all_emission_diffs))
    # rest_of_text = rest_of_text + str(emission_diff) + ' percent above average'
    # pos_text = pos_text + rest_of_text
    # neg_text = neg_text + rest_of_text
    # return Condition(cond_type, emission_diff, pos_text, neg_text)


def get_travel_date_condition(flight_data):
    all_travel_dates = []
    for one_route in flight_data:
        all_travel_dates.append(str(one_route['TravelDate']))
    pos_text = 'I want to travel on '
    neg_text = 'I do not want to travel on '
    focus_date = random.choice(all_travel_dates)
    pos_text = pos_text + focus_date
    neg_text = neg_text + focus_date
    return Condition('eq', focus_date, pos_text, neg_text)


def get_price_condition(flight_data):
    all_prices = []
    for one_route in flight_data:
        all_prices.append(one_route['Price'])
    pos_text = 'The price should be '
    neg_text = 'The price should not be '

    rest_of_text = ''
    if random.randint(0, 1) == 0:
        rest_of_text = rest_of_text + 'less than '
        cond_type = 'le'
    else:
        rest_of_text = rest_of_text + 'more than '
        cond_type = 'ge'

    one_price = int(float(random.choice(all_prices)[1:]) / 100) * 100
    rest_of_text = rest_of_text + '$' + str(one_price)

    pos_text = pos_text + rest_of_text
    neg_text = neg_text + rest_of_text
    return Condition(cond_type, one_price, pos_text, neg_text)


def get_location_condition(flight_data):
    all_locations = set()
    for one_route in flight_data:
        num_layovers = int(one_route['NumberOfLayovers'])
        for stop_num in range(1, num_layovers + 1):
            k = 'Layover' + str(stop_num) + 'Location'
            all_locations.add(one_route[k])
    num_locations = len(all_locations)
    if num_locations >= 4:
        num_to_avoid = random.choice(range(1, 3))
        pos_text = 'I only want layovers in '
        neg_text = 'I do not want to have layovers in '
        imp_locations = random.sample(all_locations, num_to_avoid)
        rest_of_text = ''
        if num_to_avoid == 1:
            rest_of_text = rest_of_text + imp_locations[0]
        else:
            for one_al in imp_locations[:-1]:
                rest_of_text = rest_of_text + one_al + ', '
            rest_of_text = rest_of_text + 'and ' + imp_locations[-1] + '.'
        pos_text = pos_text + rest_of_text
        neg_text = neg_text + rest_of_text
        condition_obj = Condition('eq', imp_locations, pos_text, neg_text)
        return condition_obj
    return Condition('eq', num_locations, '', '')


# Each layover, add for total layover
def get_layover_time_condition(flight_data):
    all_times = []
    for one_route in flight_data:
        num_layovers = int(one_route['NumberOfLayovers'])
        for stop_num in range(1, num_layovers + 1):
            k = 'Layover' + str(stop_num) + 'Time'
            if 'hr' not in one_route[k]:
                all_times.append(0)
            else:
                all_times.append(int(one_route[k].split('hr')[0].strip()))

    pos_text = 'Each layover should be  '
    neg_text = 'Each layover should not be '
    rest_of_text = ''
    if random.randint(0, 1) == 0:
        rest_of_text = rest_of_text + 'less than '
        cond_type = 'le'
    else:
        rest_of_text = rest_of_text + 'more than '
        cond_type = 'ge'
    med_time = str(int(np.median(all_times)))
    rest_of_text = rest_of_text + med_time + ' hours'

    minutes = random.choice(['00', '15', '30', '45'])
    if minutes != '00':
        rest_of_text = rest_of_text + ' and ' + minutes + ' minutes'
    pos_text = pos_text + rest_of_text
    neg_text = neg_text + rest_of_text
    layover_time = med_time + ':' + minutes

    return Condition(cond_type, layover_time, pos_text, neg_text)


def get_total_layover_time_condition(flight_data):
    all_times = []
    for one_route in flight_data:
        num_layovers = int(one_route['NumberOfLayovers'])
        total_time = 1
        for stop_num in range(1, num_layovers + 1):
            k = 'Layover' + str(stop_num) + 'Time'
            if 'hr' not in one_route[k]:
                total_time = total_time + 1
            else:
                total_time = total_time + int(one_route[k].split('hr')[0].strip())
        all_times.append(total_time)

    pos_text = 'Total layover time across all my layovers should be  '
    neg_text = 'Total layover time across all my layovers should not be  '
    rest_of_text = ''
    if random.randint(0, 1) == 0:
        rest_of_text = rest_of_text + 'less than '
        cond_type = 'le'
    else:
        rest_of_text = rest_of_text + 'more than '
        cond_type = 'ge'
    med_time = str(random.choice(all_times))
    rest_of_text = rest_of_text + med_time + ' hours'

    minutes = random.choice(['00', '15', '30', '45'])
    if minutes != '00':
        rest_of_text = rest_of_text + ' and ' + minutes + ' minutes'
    pos_text = pos_text + rest_of_text
    neg_text = neg_text + rest_of_text
    layover_time = med_time + ':' + minutes

    return Condition(cond_type, layover_time, pos_text, neg_text)
