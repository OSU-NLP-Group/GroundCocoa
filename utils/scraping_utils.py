# Author: Harsh Kohli
# Date Created: 27-08-2023

import csv
import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from constants import airport_file


def scrape_data(origin, dest, date_leave, date_return, flight_class):
    url = make_url(origin=origin, dest=dest, date_leave=date_leave, date_return=date_return)
    data = get_results(url, date_leave, date_return, flight_class)
    return data


def make_url(origin, dest, date_leave, date_return):
    base = 'https://www.google.com/travel/flights?q=Flights%20to%20{}%20from%20{}%20on%20{}%20through%20{}'
    return base.format(dest, origin, date_leave, date_return)


def get_results(url, date_leave, date_return, flight_class):
    results, features, layovers = make_url_request(url, flight_class)
    flight_info = get_info(results)
    partition = partition_info(flight_info)
    old_features = parse_columns(partition, date_leave, date_return)
    return features, old_features, layovers


def get_info(res):
    info = []
    collect = False
    for r in res:
        if 'more flights' in r:
            collect = False
        if collect and 'price' not in r.lower() and 'prices' not in r.lower() and 'other' not in r.lower() and ' – ' not in r.lower():
            info += [r]
        if r == 'Sort by:':
            collect = True
    return info


def make_url_request(url, flight_class):
    driver = webdriver.Chrome('chromedriver')
    driver.get(url)
    WebDriverWait(driver, timeout=10).until(lambda d: len(get_flight_elements(d)) > 100)
    driver.maximize_window()
    time.sleep(2)
    if flight_class != "Economy":
        driver.find_element(By.XPATH,
                            '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[1]/div[3]/div/div/div/div[1]').click()
        time.sleep(2)
        if flight_class == "Business":
            driver.find_element(By.XPATH,
                                '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[1]/div[3]/div/div/div/div[2]/ul/li[3]').click()
        if flight_class == "First":
            driver.find_element(By.XPATH,
                                '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[1]/div[3]/div/div/div/div[2]/ul/li[4]').click()
    time.sleep(2)
    try:
        dynamic_id = 'c' + str(
            int(driver.find_element("xpath", "//*[starts-with(@id, 'c')]").get_attribute("id")[1:]))
        dynamic_path = '//*[@id="{}"]/span[2]/div/div/div/div[3]'.format(dynamic_id)
        driver.find_element("xpath", dynamic_path).click()
    except:
        print('did not find popup')
    time.sleep(1)
    driver.find_element(By.XPATH,
                        '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div/div/div[1]/div/button').click()
    time.sleep(1)
    driver.find_element(By.XPATH,
                        '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div/div/div[2]/div/ul/li[2]/span[3]').click()
    time.sleep(2)
    results = get_flight_elements(driver)
    result_count_info = results[21]
    count = int(result_count_info.split(' of')[0])
    button_path_1 = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul/li['
    button_path_2 = ']/div/div[3]/div/div/button/div[3]'
    info_path_1 = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul/li['
    info_path_2 = ']/div/div[4]'
    button_path_3 = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul/li['
    button_path_4 = ']/div/div[3]/div/div/button'
    all_flight_features, all_layovers = [], []
    for index in range(1, count + 1):
        button_xpath = button_path_1 + str(index) + button_path_2
        time.sleep(2)
        driver.find_element(By.XPATH, button_xpath).click()
        time.sleep(1)
        info_path = info_path_1 + str(index) + info_path_2
        flights_info = driver.find_element(By.XPATH, info_path).text.split('\n')
        features, layovers = get_features(flights_info)
        all_layovers.append(layovers)
        all_flight_features.append(features)
        button_xpath = button_path_3 + str(index) + button_path_4
        driver.find_element(By.XPATH, button_xpath).click()
    driver.quit()
    return results, all_flight_features, all_layovers


def get_features(flights_info):
    features = []
    starts, ends, layovers = [], [], []
    count = 0
    for index, line in enumerate(flights_info):
        if "AM" in line or "PM" in line:
            count = count + 1
            if count % 2 == 0:
                starts.append(index + 2)
        if "layover" in line and "Overnight" not in line:
            ends.append(index)
            layover_time = line.split('layover')[0]
            layovers.append(layover_time)

    ends.append(len(flights_info))
    for start, end in zip(starts, ends):
        one_flight_feature = []
        for index in range(start, end):
            if 'Ticket also sold by' in flights_info[index]:
                continue
            one_flight_feature.append(flights_info[index])
        features.append(one_flight_feature)
    return features, layovers


def get_flight_elements(d):
    return d.find_element(by=By.XPATH, value='//body[@id = "yDmH0d"]').text.split('\n')


def partition_info(info):
    i = 0
    grouped = []
    while i < len(info) - 1:
        j = i + 2
        end = -1
        while j < len(info):
            if end_condition(info[j]):
                end = j
                break
            j += 1
        if end == -1:
            break
        grouped += [info[i:end]]
        i = end
    return grouped


def end_condition(x):
    if len(x) < 2:
        return False
    if x[-2] == '+':
        x = x[:-2]
    if x[-2:] == 'AM' or x[-2:] == 'PM':
        return True
    return False


def parse_columns(grouped, date_leave, date_return):
    depart_time = []
    arrival_time = []
    airline = []
    travel_time = []
    origin = []
    dest = []
    stops = []
    stop_time = []
    stop_location = []
    co2_emission = []
    emission = []
    price = []
    trip_type = []
    access_date = [date.today().strftime('%Y-%m-%d')] * len(grouped)
    for g in grouped:
        i_diff = 0
        depart_time += [g[0]]
        arrival_time += [g[1]]
        i_diff += 1 if 'Separate tickets booked together' in g[2] else 0
        airline += [g[2 + i_diff]]
        travel_time += [g[3 + i_diff]]
        origin += [g[4 + i_diff].split('–')[0]]
        dest += [g[4 + i_diff].split('–')[1]]
        num_stops = 0 if 'Nonstop' in g[5 + i_diff] else int(g[5 + i_diff].split('stop')[0])
        stops += [num_stops]
        stop_time += [None if num_stops == 0 else (g[6 + i_diff].split('min')[0] if num_stops == 1 else None)]
        stop_location += [None if num_stops == 0 else (
            g[6 + i_diff].split('min')[1] if num_stops == 1 and 'min' in g[6 + i_diff] else [
                g[6 + i_diff].split('hr')[1] if 'hr' in g[6 + i_diff] and num_stops == 1 else g[6 + i_diff]])]
        i_diff += 0 if num_stops == 0 else 1
        if g[6 + i_diff] != '–':
            co2_emission += [float(g[6 + i_diff].replace(',', '').split(' kg')[0])]
            emission += [0 if g[7 + i_diff] == 'Avg emissions' else int(g[7 + i_diff].split('%')[0])]

            price += [float(g[8 + i_diff][1:].replace(',', ''))]
            trip_type += [g[9 + i_diff]]
        else:
            co2_emission += [None]
            emission += [None]
            price += [float(g[7 + i_diff][1:].replace(',', ''))]
            trip_type += [g[8 + i_diff]]

    return {
        'Leave Date': [date_leave] * len(grouped),
        'Return Date': [date_return] * len(grouped),
        'Depart Time (Leg 1)': depart_time,
        'Arrival Time (Leg 1)': arrival_time,
        'Airline(s)': airline,
        'Travel Time': travel_time,
        'Origin': origin,
        'Destination': dest,
        'Num Stops': stops,
        'Layover Time': stop_time,
        'Stop Location': stop_location,
        'CO2 Emission': co2_emission,
        'Emission Avg Diff (%)': emission,
        'Price ($)': price,
        'Trip Type': trip_type,
        'Access Date': access_date
    }


def stitch_together(new_features, old_features, layovers, ticket_class, src, dest, travel_date):
    num_flights = len(old_features['Leave Date'])
    all_flights_info = []

    airports = open(airport_file, 'r', encoding='utf8')
    csvreader = csv.reader(airports)

    iata_lookup = {}
    for row in csvreader:
        code = row[13]
        city = row[10]
        iata_lookup[code] = city

    for flight_num in range(num_flights):
        dept_time = old_features['Depart Time (Leg 1)'][flight_num]
        arr_time = old_features['Arrival Time (Leg 1)'][flight_num]
        airline = old_features['Airline(s)'][flight_num]
        travel_time = old_features['Travel Time'][flight_num]
        num_stops = old_features['Num Stops'][flight_num]
        emission_dif = old_features['Emission Avg Diff (%)'][flight_num]
        price = old_features['Price ($)'][flight_num]
        stop_loc = old_features['Stop Location'][flight_num]
        stop_location = ''
        if isinstance(stop_loc, list):
            for index, one_loc in enumerate(stop_loc):
                if index == len(stop_loc) - 1:
                    stop_location = stop_location + one_loc
                else:
                    stop_location = stop_location + one_loc + ', '
        else:
            stop_location = stop_loc

        all_part_features = []
        all_layovers = []
        for part in range(num_stops + 1):
            part_features = '['
            for index, feature in enumerate(new_features[flight_num][part]):
                if index != (len(new_features[flight_num][part]) - 1):
                    part_features = part_features + feature + ', '
                else:
                    part_features = part_features + feature
            part_features = part_features + ']'
            all_part_features.append(part_features)

        for layover_time in layovers[flight_num]:
            all_layovers.append(layover_time)
        one_flight_info = {}
        one_flight_info['Airline'] = '[' + airline + ']'
        one_flight_info['TicketClass'] = ticket_class
        one_flight_info['DepartureTime'] = dept_time.replace("\u202f", " ")
        one_flight_info['ArrivalTime'] = arr_time.replace("\u202f", " ")
        one_flight_info['TravelTime'] = travel_time.replace("\u202f", " ")
        one_flight_info['NumberOfLayovers'] = str(num_stops)
        one_flight_info['CarbonEmissionAvgDiff(%)'] = str(emission_dif)
        one_flight_info['Price'] = '$' + str(price)
        one_flight_info['TravelDate'] = travel_date
        if src in iata_lookup:
            one_flight_info['SourceCity'] = iata_lookup[src]
        else:
            one_flight_info['SourceCity'] = src

        if dest in iata_lookup:
            one_flight_info['DestinationCity'] = iata_lookup[dest]
        else:
            one_flight_info['DestinationCity'] = dest

        one_flight_info['LayoverLocations'] = ''
        one_flight_info['LayoverTimes'] = ''
        for stop_num in range(num_stops):

            airport_code = stop_location.split(',')[stop_num].strip()
            stop_loc = airport_code
            if airport_code in iata_lookup:
                stop_loc = iata_lookup[airport_code]
            if stop_num != num_stops - 1:
                one_flight_info['LayoverLocations'] = one_flight_info['LayoverLocations'] + stop_loc + ', '
                one_flight_info['LayoverTimes'] = one_flight_info['LayoverTimes'] + all_layovers[stop_num] + ', '
            else:
                one_flight_info['LayoverLocations'] = one_flight_info['LayoverLocations'] + stop_loc
                one_flight_info['LayoverTimes'] = one_flight_info['LayoverTimes'] + all_layovers[stop_num]
            one_flight_info['Layover' + str(stop_num + 1) + 'Location'] = stop_loc
            one_flight_info['Layover' + str(stop_num + 1) + 'Time'] = all_layovers[stop_num]

        for part in range(num_stops + 1):
            one_flight_info['Flight' + str(part + 1) + 'Features'] = all_part_features[part]

        all_flights_info.append(one_flight_info)

    return all_flights_info
