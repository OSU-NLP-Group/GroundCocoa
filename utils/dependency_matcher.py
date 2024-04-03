# Author: Harsh Kohli
# Date Created: 11-11-2023


def match_airline_dependency(flight_slot_value, required_value, condition_object, slot, is_not):
    flight_airlines = flight_slot_value.split(',')
    if len(flight_airlines) > 1:
        flight_airlines[0] = flight_airlines[0][1:]
        flight_airlines[-1] = flight_airlines[-1][:-1]
    if is_not:
        for airline in flight_airlines:
            if airline in required_value:
                return False
        return True
    else:
        for airline in flight_airlines:
            if airline not in required_value:
                return False
        return True


def match_ticket_class_dependency(flight_slot_value, required_value, condition_object, slot, is_not):
    if is_not:
        if required_value != flight_slot_value:
            return True
        return False
    else:
        if required_value == flight_slot_value:
            return True
        return False


def match_flight_time_condition(flight_slot_value, required_value, condition_object, slot, is_not):
    cond_type = condition_object.cond_type
    if is_not:
        if cond_type == 'le':
            cond_type = 'ge'
        else:
            cond_type = 'le'
    flight_time, am_pm = flight_slot_value.split(' ')
    flight_hr, flight_min = flight_time.split(':')
    required_hr, required_min = required_value.split(':')
    flight_hr, flight_min, required_hr, required_min = int(flight_hr), int(flight_min), int(required_hr), int(
        required_min)
    if 'PM' in am_pm and flight_hr < 12:
        flight_hr = flight_hr + 12
    if cond_type == 'le':
        if flight_hr < required_hr:
            return True
        if flight_hr == required_hr:
            if flight_min <= required_min:
                return True
        return False

    if cond_type == 'ge':
        if flight_hr > required_hr:
            return True
        if flight_hr == required_hr:
            if flight_min >= required_min:
                return True
        return False


def match_flight_time_between_condition(flight_slot_value, required_value, condition_object, slot, is_not):
    start_time, end_time = required_value[0], required_value[1]
    flight_time, am_pm = flight_slot_value.split(' ')
    flight_hr, flight_min = flight_time.split(':')
    start_hr, start_min = start_time.split(':')
    end_hr, end_min = end_time.split(':')
    flight_hr, flight_min, start_hr, start_min, end_hr, end_min = int(flight_hr), int(flight_min), int(start_hr), int(
        start_min), int(end_hr), int(end_min)
    if 'PM' in am_pm and flight_hr < 12:
        flight_hr = flight_hr + 12

    within_range = True
    if flight_hr < start_hr:
        within_range = False
    if flight_hr == start_hr:
        if flight_min < start_min:
            within_range = False

    if flight_hr > end_hr:
        within_range = False
    if flight_hr == end_hr:
        if flight_min > end_min:
            within_range = False

    if not is_not:
        return within_range
    else:
        return not within_range


def match_travel_time_condition(flight_slot_value, required_value, condition_object, slot, is_not):
    cond_type = condition_object.cond_type
    if is_not:
        if cond_type == 'le':
            cond_type = 'ge'
        else:
            cond_type = 'le'
    if 'hr' in flight_slot_value:
        info = flight_slot_value.split('hr')
        flight_hr = int(info[0])
        flight_min = 0
        if 'min' in info[1]:
            flight_min = int(info[1].strip().split(' ')[0])
    else:
        flight_hr = 0
        flight_min = 0
        if 'min' in flight_slot_value:
            flight_min = int(flight_slot_value.strip().split(' ')[0])

    required_hr, required_min = required_value.split(':')
    required_hr, required_min = int(required_hr), int(required_min)
    if cond_type == 'le':
        if flight_hr < required_hr:
            return True
        if flight_hr == required_hr:
            if flight_min <= required_min:
                return True
        return False

    if cond_type == 'ge':
        if flight_hr > required_hr:
            return True
        if flight_hr == required_hr:
            if flight_min >= required_min:
                return True
        return False


def match_num_layovers_condition(flight_slot_value, required_value, condition_object, slot, is_not):
    cond_type = condition_object.cond_type
    flight_layovers = int(flight_slot_value)

    if not is_not:
        if cond_type == 'le':
            if flight_layovers < required_value:
                return True, True
            return False, True
        if cond_type == 'ge':
            natural = True
            if required_value >= 2:
                natural = False
            if flight_layovers > required_value:
                return True, natural
            return False, natural
    else:
        if cond_type == 'le':
            natural = True
            if required_value > 2:
                natural = False
            if flight_layovers >= required_value:
                return True, natural
            return False, natural
        if cond_type == 'ge':
            if flight_layovers <= required_value:
                return True, True
            return False, True


def match_emission_diff_condition(flight_slot_value, required_value, condition_object, slot, is_not):
    flight_emission_diff = float(flight_slot_value)

    if not is_not:
        if flight_emission_diff < 0:
            return True, True
        return False, True
    else:
        if flight_emission_diff > 0:
            return True, False
        return False, False

    # cond_type = condition_object.cond_type
    # flight_emission_diff = float(flight_slot_value)
    #
    # if not is_not:
    #     if cond_type == 'le':
    #         if flight_emission_diff < required_value:
    #             return True
    #         return False
    #     if cond_type == 'ge':
    #         if flight_emission_diff > required_value:
    #             return True
    #         return False
    # else:
    #     if cond_type == 'le':
    #         if flight_emission_diff >= required_value:
    #             return True
    #         return False
    #     if cond_type == 'ge':
    #         if flight_emission_diff <= required_value:
    #             return True
    #         return False


def match_travel_date_condition(flight_slot_value, required_value, condition_object, slot, is_not):
    if is_not:
        if required_value.strip() != flight_slot_value.strip():
            return True
        return False
    else:
        if required_value.strip() == flight_slot_value.strip():
            return True
        return False


def match_price_condition(flight_slot_value, required_value, condition_object, slot, is_not):
    cond_type = condition_object.cond_type
    flight_price = float(flight_slot_value[1:])

    if not is_not:
        if cond_type == 'le':
            if flight_price < required_value:
                return True, True
            return False, True
        if cond_type == 'ge':
            if flight_price > required_value:
                return True, False
            return False, False
    else:
        if cond_type == 'le':
            if flight_price >= required_value:
                return True, False
            return False, False
        if cond_type == 'ge':
            if flight_price <= required_value:
                return True, True
            return False, True


def match_location_condition(flight_slot_value, required_value, condition_object, slot, is_not):
    layover_locations = flight_slot_value.split(',')
    if not is_not:
        for one_stop in layover_locations:
            if one_stop not in required_value:
                return False
    else:
        for one_stop in layover_locations:
            if one_stop in required_value:
                return False
    return True


def match_layover_time_condition(flight_slot_value, required_value, condition_object, slot, is_not):
    layover_times = flight_slot_value.split(',')
    cond_type = condition_object.cond_type
    required_hr, required_min = required_value.split(':')
    required_hr, required_min = int(required_hr), int(required_min)
    if not is_not:
        for one_time in layover_times:
            flight_hr = 0
            flight_min = 0
            if 'hr' in one_time:
                info = one_time.split('hr')
                flight_hr = int(info[0])
                if 'min' in info[1]:
                    flight_min = int(info[1].strip().split(' ')[0])
            else:
                if 'min' in one_time:
                    flight_min = int(one_time.strip().split(' ')[0])
            if cond_type == 'ge':
                if flight_hr < required_hr:
                    return False
                elif flight_hr == required_hr:
                    if flight_min < required_min:
                        return False
            if cond_type == 'le':
                if flight_hr > required_hr:
                    return False
                elif flight_hr == required_hr:
                    if flight_min > required_min:
                        return False

    else:
        for one_time in layover_times:
            flight_hr = 0
            flight_min = 0
            if 'hr' in one_time:
                info = one_time.split('hr')
                flight_hr = int(info[0])
                if 'min' in info[1]:
                    flight_min = int(info[1].strip().split(' ')[0])
            else:
                if 'min' in one_time:
                    flight_min = int(one_time.strip().split(' ')[0])
            if cond_type == 'ge':
                if flight_hr > required_hr:
                    return False
                elif flight_hr == required_hr:
                    if flight_min > required_min:
                        return False
            if cond_type == 'le':
                if flight_hr < required_hr:
                    return False
                elif flight_hr == required_hr:
                    if flight_min < required_min:
                        return False
    return True


def match_total_layover_time_condition(flight_slot_value, required_value, condition_object, slot, is_not):
    layover_times = flight_slot_value.split(',')
    cond_type = condition_object.cond_type
    required_hr, required_min = required_value.split(':')
    required_hr, required_min = int(required_hr), int(required_min)
    if not is_not:
        total_hours, total_minutes = 0, 0
        for one_time in layover_times:
            flight_hr = 0
            flight_min = 0
            if 'hr' in one_time:
                info = one_time.split('hr')
                flight_hr = int(info[0])
                if 'min' in info[1]:
                    flight_min = int(info[1].strip().split(' ')[0])
            else:
                if 'min' in one_time:
                    flight_min = int(one_time.strip().split(' ')[0])

            total_hours = total_hours + flight_hr
            total_minutes = total_minutes + flight_min
            if total_minutes > 60:
                total_hours = total_hours + 1
                total_minutes = total_minutes - 60

        if cond_type == 'ge':
            if total_hours < required_hr:
                return False
            elif total_hours == required_hr:
                if total_minutes < required_min:
                    return False
        if cond_type == 'le':
            if total_hours > required_hr:
                return False
            elif total_hours == required_hr:
                if total_minutes > required_min:
                    return False

    else:
        total_hours, total_minutes = 0, 0
        for one_time in layover_times:
            flight_hr = 0
            flight_min = 0
            if 'hr' in one_time:
                info = one_time.split('hr')
                flight_hr = int(info[0])
                if 'min' in info[1]:
                    flight_min = int(info[1].strip().split(' ')[0])
            else:
                if 'min' in one_time:
                    flight_min = int(one_time.strip().split(' ')[0])

            total_hours = total_hours + flight_hr
            total_minutes = total_minutes + flight_min
            if total_minutes > 60:
                total_hours = total_hours + 1
                total_minutes = total_minutes - 60

        if cond_type == 'ge':
            if total_hours > required_hr:
                return False
            elif total_hours == required_hr:
                if total_minutes > required_min:
                    return False
        if cond_type == 'le':
            if total_hours < required_hr:
                return False
            elif total_hours == required_hr:
                if total_minutes < required_min:
                    return False
    return True
