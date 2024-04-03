# Author: Harsh Kohli
# Date Created: 17-12-2023

busiest_airport_file = 'flight_data/busiest_airports.csv'
airport_file = 'flight_data/airports.csv'
flight_options_file = 'flight_data/flight_options.json'
conditions_file = 'flight_data/conditions.json'
data_file = 'flight_data/compositional_dataset.json'
cocoa_dataset_file = 'flight_data/grounded_cocoa.json'
response_dir = 'images'

slot_minterm_configs = [(2, 2), (3, 2), (4, 2), (4, 3), (5, 2), (6, 2)]

slots = ['Airline', 'TicketClass', 'DepartureTime', 'ArrivalTime', 'TravelTime', 'NumberOfLayovers',
         'CarbonEmissionAvgDiff(%)', 'TravelDate', 'Price', 'LayoverLocations', 'LayoverTimes', 'TotalLayoverTime',
         'DepartureTimeBetween', 'ArrivalTimeBetween']

prompt1 = 'The sentence below describes a condition of user requirements. Please note that this is like an OR condition like the logical or and not an AND condition. For example, for a user requirement - "I want to depart before 05:30 or the flight must be Lufthansa" and good paraphrase might be "If I am departing after 5:30 pm, I want to only fly Lufthansa airlines". Paraphrase the sentence. Make sure the language sounds natural and human-like. Avoid using "they" or "the user" and use "I" instead as if you were describing your own requirements. Please note that if the user is requesting carbon emissions above average, then it is not a cleaner flight as the user specifically asks for a flight that emits more carbon than the average. On the other hand, a request for a below average carbon emissions implies a request for a greener flight that is good for the environment. If the user does not explicitly mention emissions, please do not include it in your paraphrase: '

prompt2 = 'Can you paraphrase and simplify these user requirements to make them sound more natural and human-like. These should be in a single paragraph form. Make sure the meaning is not altered and no requirement is missed. Please note that if the user is requesting carbon emissions above average, then it is not a cleaner flight as the user specifically asks for a flight that emits more carbon than the average. On the other hand, a request for a below average carbon emissions implies a request for a greener flight that is good for the environment. If the user does not explicitly mention emissions, please do not include it in your paraphrase: '

num_options_per_mcq = 5
