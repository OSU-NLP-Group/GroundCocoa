# Author: Harsh Kohli
# Date Created: 19-12-2023

import copy
import random
from constants import slot_minterm_configs, slots, flight_options_file, conditions_file
from utils.ioutils import read_from_json, write_to_json
from sympy.logic import POSform
from sympy import symbols
from utils.gen_utils import get_graph_info
from utils.dependency_parser import recursive_condition_generator, compose_conditions, match_conditions
import sympy.logic.boolalg as FuncType

flight_options = read_from_json(flight_options_file)

num_questions_per_route = 4

all_condition_data = []
for key, flight_data in flight_options.items():
    src_city, dest_city = flight_data[0]['SourceCity'], flight_data[0]['DestinationCity']
    print(key)
    for num_features, num_minterms in slot_minterm_configs:

        for _ in range(num_questions_per_route):
            data_dict = {}
            while True:
                relevant_slots = random.sample(slots, num_features)
                all_symbols = symbols(" ".join(relevant_slots))
                symbol_dict = {}
                for slot, sym in zip(relevant_slots, all_symbols):
                    symbol_dict[slot] = sym
                minterms = []
                for _ in range(num_minterms):
                    minterm = []
                    for _ in range(num_features):
                        minterm.append(random.randint(0, 1))
                    minterms.append(minterm)
                ans = POSform(all_symbols, minterms)
                if len(ans.args) < 2:
                    continue

                contains_or = False
                for one_arg in ans.args:
                    if one_arg.func == FuncType.Or:
                        contains_or = True
                        break

                if not contains_or:
                    continue

                type_obj_to_conditions = {}
                for one_cond in ans.args:
                    is_not = False
                    if one_cond.func == FuncType.Not:
                        is_not = True
                    recursive_condition_generator(flight_data, one_cond, symbol_dict, is_not, type_obj_to_conditions)

                flight_data_copy = copy.deepcopy(flight_data)
                flight_matching_results, all_failures, is_natural = match_conditions(flight_data_copy, ans,
                                                                         type_obj_to_conditions)
                if True in flight_matching_results and False in flight_matching_results:
                    avg_dep, max_dep, lcc, width = get_graph_info(ans)
                    data_dict['average_dependency'] = avg_dep
                    data_dict['max_dependency'] = max_dep
                    data_dict['largest_connected_component'] = lcc
                    data_dict['reasoning_width'] = width
                    data_dict["flight_options"] = flight_data_copy
                    data_dict["slots"] = num_features
                    data_dict["minterms"] = num_minterms
                    data_dict["is_natural"] = is_natural
                    data_dict["pos_condition"] = str(ans)
                    labels = []
                    for label in flight_matching_results:
                        if label:
                            labels.append("1")
                        else:
                            labels.append("0")

                    data_dict["labels"] = labels
                    data_dict["violated_propositions"] = all_failures
                    all_conditions, type_to_index = [], {}
                    for cond_type in type_obj_to_conditions:
                        type_to_index[cond_type] = 0
                    for one_cond in ans.args:
                        all_conditions.append(compose_conditions(one_cond, type_obj_to_conditions, type_to_index))

                    data_dict["condition_templates"] = all_conditions
                    all_condition_data.append(data_dict)
                    break

write_to_json(all_condition_data, conditions_file)
