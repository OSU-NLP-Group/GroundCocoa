# Author: Harsh Kohli
# Date Created: 31-08-2023

from scipy.stats import entropy
from utils.dependency_generator import *
from utils.dependency_matcher import *
import sympy.core.symbol as symbol
import sympy.logic.boolalg as FuncType


def populate_condition(cond, condition_object, type_obj_to_condition):
    if cond in type_obj_to_condition:
        type_obj_to_condition[cond].append(condition_object)
    else:
        type_obj_to_condition[cond] = [condition_object]


def recursive_condition_generator(flight_data, cond, symbol_dict, is_not, type_obj_to_condition):
    if cond.func == symbol.Symbol:
        if 'Airline' in symbol_dict and cond == symbol_dict['Airline']:
            condition_object = get_airline_condition(flight_data)
            populate_condition(cond, condition_object, type_obj_to_condition)
        if 'TicketClass' in symbol_dict and cond == symbol_dict['TicketClass']:
            condition_object = get_ticketclass_condition(flight_data)
            populate_condition(cond, condition_object, type_obj_to_condition)
        if 'DepartureTime' in symbol_dict and cond == symbol_dict['DepartureTime']:
            condition_object = get_departuretime_condition(flight_data)
            populate_condition(cond, condition_object, type_obj_to_condition)
        if 'DepartureTimeBetween' in symbol_dict and cond == symbol_dict['DepartureTimeBetween']:
            condition_object = get_departuretime_between_condition(flight_data)
            populate_condition(cond, condition_object, type_obj_to_condition)
        if 'ArrivalTime' in symbol_dict and cond == symbol_dict['ArrivalTime']:
            condition_object = get_arrivaltime_condition(flight_data)
            populate_condition(cond, condition_object, type_obj_to_condition)
        if 'ArrivalTimeBetween' in symbol_dict and cond == symbol_dict['ArrivalTimeBetween']:
            condition_object = get_arrivaltime_between_condition(flight_data)
            populate_condition(cond, condition_object, type_obj_to_condition)
        if 'TravelTime' in symbol_dict and cond == symbol_dict['TravelTime']:
            condition_object = get_traveltime_condition(flight_data)
            populate_condition(cond, condition_object, type_obj_to_condition)
        if 'NumberOfLayovers' in symbol_dict and cond == symbol_dict['NumberOfLayovers']:
            condition_object = get_num_layovers_condition(flight_data)
            populate_condition(cond, condition_object, type_obj_to_condition)
        if 'CarbonEmissionAvgDiff(%)' in symbol_dict and cond == symbol_dict['CarbonEmissionAvgDiff(%)']:
            condition_object = get_emission_diff_condition(flight_data)
            populate_condition(cond, condition_object, type_obj_to_condition)
        if 'TravelDate' in symbol_dict and cond == symbol_dict['TravelDate']:
            condition_object = get_travel_date_condition(flight_data)
            populate_condition(cond, condition_object, type_obj_to_condition)
        if 'Price' in symbol_dict and cond == symbol_dict['Price']:
            condition_object = get_price_condition(flight_data)
            populate_condition(cond, condition_object, type_obj_to_condition)
        if 'LayoverLocations' in symbol_dict and cond == symbol_dict['LayoverLocations']:
            condition_object = get_location_condition(flight_data)
            populate_condition(cond, condition_object, type_obj_to_condition)
        if 'LayoverTimes' in symbol_dict and cond == symbol_dict['LayoverTimes']:
            condition_object = get_layover_time_condition(flight_data)
            populate_condition(cond, condition_object, type_obj_to_condition)
        if 'TotalLayoverTime' in symbol_dict and cond == symbol_dict['TotalLayoverTime']:
            condition_object = get_total_layover_time_condition(flight_data)
            populate_condition(cond, condition_object, type_obj_to_condition)
    else:
        for one_arg in cond.args:
            next_is_not = False
            if one_arg.func == FuncType.Not:
                next_is_not = True
            recursive_condition_generator(flight_data, one_arg, symbol_dict, next_is_not, type_obj_to_condition)


def compose_conditions(cond, type_obj_to_condition, type_to_index):
    if cond.func == symbol.Symbol:
        index = type_to_index[cond]
        type_to_index[cond] = type_to_index[cond] + 1
        condition_obj = type_obj_to_condition[cond][index]
        return [condition_obj.pos_text]

    if cond.func == FuncType.Not:
        index = type_to_index[cond.args[0]]
        type_to_index[cond.args[0]] = type_to_index[cond.args[0]] + 1
        condition_obj = type_obj_to_condition[cond.args[0]][index]
        return [condition_obj.neg_text]

    if cond.func == FuncType.Or:
        all_conditions = []
        for one_cond in cond.args:

            if one_cond.func == symbol.Symbol:
                index = type_to_index[one_cond]
                type_to_index[one_cond] = type_to_index[one_cond] + 1
                condition_obj = type_obj_to_condition[one_cond][index]
                all_conditions.append(condition_obj.pos_text)

            if one_cond.func == FuncType.Not:
                index = type_to_index[one_cond.args[0]]
                type_to_index[one_cond.args[0]] = type_to_index[one_cond.args[0]] + 1
                condition_obj = type_obj_to_condition[one_cond.args[0]][index]
                all_conditions.append(condition_obj.neg_text)

        return all_conditions

    print('Invalid condition type')


def add_label(dict, key, value):
    label = 0
    if value:
        label = 1
    if key in dict:
        dict[key].append(label)
    else:
        dict[key] = [label]


def match_single_condition(one_arg, type_to_index, type_obj_to_condition, one_flight, primitive_by_slot,
                           primitive_tags, is_not):
    # is_not = False
    # if one_arg.func == FuncType.Not:
    #     actual_arg = one_arg.args[0]
    #     index = type_to_index[one_arg.args[0]]
    #     type_to_index[one_arg.args[0]] = type_to_index[one_arg.args[0]] + 1
    #     condition_object = type_obj_to_condition[one_arg.args[0]][index]
    #     is_not = True
    # else:
    actual_arg = one_arg
    index = type_to_index[one_arg]
    type_to_index[one_arg] = type_to_index[one_arg] + 1
    condition_object = type_obj_to_condition[one_arg][index]

    required_value = condition_object.value1
    slot = actual_arg.name

    if slot == 'TotalLayoverTime':
        flight_slot_value = one_flight['LayoverTimes']
    elif slot == 'DepartureTimeBetween':
        flight_slot_value = one_flight['DepartureTime']
    elif slot == 'ArrivalTimeBetween':
        flight_slot_value = one_flight['ArrivalTime']
    else:
        flight_slot_value = one_flight[slot]

    if slot == 'CarbonEmissionAvgDiff(%)' and flight_slot_value == 'None':
        flight_slot_value = 0
        one_flight['CarbonEmissionAvgDiff(%)'] = 0
    satisfies = False
    is_natural = True
    if actual_arg.name == 'Airline':
        satisfies = match_airline_dependency(flight_slot_value, required_value, condition_object, slot,
                                             is_not)
        add_label(primitive_by_slot, actual_arg.name, satisfies)
    if actual_arg.name == 'TicketClass':
        satisfies = match_ticket_class_dependency(flight_slot_value, required_value, condition_object, slot,
                                                  is_not)
        add_label(primitive_by_slot, actual_arg.name, satisfies)
    if actual_arg.name == 'DepartureTime':
        satisfies = match_flight_time_condition(flight_slot_value, required_value, condition_object, slot,
                                                is_not)
        add_label(primitive_by_slot, actual_arg.name, satisfies)
    if actual_arg.name == 'DepartureTimeBetween':
        satisfies = match_flight_time_between_condition(flight_slot_value, required_value, condition_object, slot,
                                                is_not)
        add_label(primitive_by_slot, actual_arg.name, satisfies)
    if actual_arg.name == 'ArrivalTime':
        satisfies = match_flight_time_condition(flight_slot_value, required_value, condition_object, slot,
                                                is_not)
        add_label(primitive_by_slot, actual_arg.name, satisfies)
    if actual_arg.name == 'ArrivalTimeBetween':
        satisfies = match_flight_time_between_condition(flight_slot_value, required_value, condition_object, slot,
                                                is_not)
        add_label(primitive_by_slot, actual_arg.name, satisfies)
    if actual_arg.name == 'TravelTime':
        satisfies = match_travel_time_condition(flight_slot_value, required_value, condition_object, slot,
                                                is_not)
        add_label(primitive_by_slot, actual_arg.name, satisfies)
    if actual_arg.name == 'NumberOfLayovers':
        satisfies, natural = match_num_layovers_condition(flight_slot_value, required_value, condition_object, slot,
                                                 is_not)
        if not natural:
            is_natural = False
        add_label(primitive_by_slot, actual_arg.name, satisfies)
    if actual_arg.name == 'CarbonEmissionAvgDiff(%)':
        satisfies, natural = match_emission_diff_condition(flight_slot_value, required_value, condition_object, slot,
                                                  is_not)
        if not natural:
            is_natural = False
        add_label(primitive_by_slot, actual_arg.name, satisfies)
    if actual_arg.name == 'TravelDate':
        satisfies = match_travel_date_condition(flight_slot_value, required_value, condition_object, slot,
                                                is_not)
        add_label(primitive_by_slot, actual_arg.name, satisfies)
    if actual_arg.name == 'Price':
        satisfies, natural = match_price_condition(flight_slot_value, required_value, condition_object, slot, is_not)
        if not natural:
            is_natural = False
        add_label(primitive_by_slot, actual_arg.name, satisfies)
    if actual_arg.name == 'LayoverLocations':
        satisfies = match_location_condition(flight_slot_value, required_value, condition_object, slot,
                                             is_not)
        add_label(primitive_by_slot, actual_arg.name, satisfies)
    if actual_arg.name == 'LayoverTimes':
        satisfies = match_layover_time_condition(flight_slot_value, required_value, condition_object, slot,
                                                 is_not)
        add_label(primitive_by_slot, actual_arg.name, satisfies)
    if actual_arg.name == 'TotalLayoverTime':
        satisfies = match_total_layover_time_condition(flight_slot_value, required_value, condition_object, slot,
                                                       is_not)
        add_label(primitive_by_slot, actual_arg.name, satisfies)

    if satisfies:
        primitive_tags.append(1)
    else:
        primitive_tags.append(0)
    return satisfies, is_natural


def match_conditions(flight_data, pos_condition, type_obj_to_condition):
    results = []
    all_failures = []
    is_natural = True
    for one_flight in flight_data:
        is_valid = True
        failing_conditions = []
        type_to_index = {}

        primitive_tags = []
        primitive_by_slot = {}

        for cond_type in type_obj_to_condition:
            type_to_index[cond_type] = 0
        for one_cond in pos_condition.args:
            one_pos_satisfies = False

            if one_cond.func == symbol.Symbol:
                satisfies, nat = match_single_condition(one_cond, type_to_index, type_obj_to_condition, one_flight,
                                                        primitive_by_slot, primitive_tags, False)
                if satisfies:
                    one_pos_satisfies = True
                if not nat:
                    is_natural = False

            if one_cond.func == FuncType.Not:
                satisfies, nat = match_single_condition(one_cond.args[0], type_to_index, type_obj_to_condition, one_flight,
                                                        primitive_by_slot, primitive_tags, True)
                if satisfies:
                    one_pos_satisfies = True
                if not nat:
                    is_natural = False

            if one_cond.func == FuncType.Or:
                for one_arg in one_cond.args:
                    if one_arg.func == symbol.Symbol:
                        satisfies, nat = match_single_condition(one_arg, type_to_index, type_obj_to_condition,
                                                                one_flight,
                                                                primitive_by_slot, primitive_tags, False)
                        if satisfies:
                            one_pos_satisfies = True
                        if not nat:
                            is_natural = False

                    if one_arg.func == FuncType.Not:
                        satisfies, nat = match_single_condition(one_arg.args[0], type_to_index, type_obj_to_condition,
                                                                one_flight,
                                                                primitive_by_slot, primitive_tags, True)
                        if satisfies:
                            one_pos_satisfies = True
                        if not nat:
                            is_natural = False


            # if len(one_cond.args) > 0:
            #     for one_arg in one_cond.args:
            #         satisfies, nat = match_single_condition(one_arg, type_to_index, type_obj_to_condition, one_flight,
            #                                            primitive_by_slot, primitive_tags)
            #         if satisfies:
            #             one_pos_satisfies = True
            #         if not nat:
            #             is_natural = False
            # else:
            #     satisfies, nat = match_single_condition(one_cond, type_to_index, type_obj_to_condition, one_flight,
            #                                        primitive_by_slot, primitive_tags)
            #     if satisfies:
            #         one_pos_satisfies = True
            #     if not nat:
            #         is_natural = False
            if not one_pos_satisfies:
                failing_conditions.append(str(one_cond))
                is_valid = False

        value, counts = np.unique(primitive_tags, return_counts=True)
        flight_ent = entropy(counts, base=2)

        ent_avg, ent_max = 0, float('-inf')
        for slot, tags in primitive_by_slot.items():
            value, counts = np.unique(tags, return_counts=True)
            slot_ent = entropy(counts, base=2)
            if slot_ent > ent_max:
                ent_max = slot_ent
            ent_avg = ent_avg + slot_ent
        ent_avg = ent_avg / len(primitive_by_slot)

        one_flight['entropy_overall'] = flight_ent
        one_flight['entropy_avg'] = ent_avg
        one_flight['entropy_max'] = ent_max

        all_failures.append(failing_conditions)
        results.append(is_valid)
    return results, all_failures, is_natural
