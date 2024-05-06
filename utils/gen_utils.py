# Author: Harsh Kohli
# Date Created: 22-12-2023

import copy
import numpy as np

char_to_index = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}


class ResponseInfo:
    def __init__(self, correct, total, acc, acc_by_complexity, ent_avg_info, ent_overall_info, ent_ans_info, acc_by_lcc,
                 acc_by_max_dependency, slots_dep_dict):
        self.correct = correct
        self.total = total
        self.acc = acc
        self.acc_by_complexity = acc_by_complexity
        self.ent_avg_info = ent_avg_info
        self.ent_overall_info = ent_overall_info
        self.ent_ans_info = ent_ans_info
        self.acc_by_lcc = acc_by_lcc
        self.acc_by_max_dependency = acc_by_max_dependency
        self.slots_dep_dict = slots_dep_dict


def initialize_acc_dicts(response_data):
    acc_by_lcc, acc_by_max_dependency, acc_by_complexity = {}, {}, {}
    slot_minterm_configs = [(2, 2), (3, 2), (4, 2), (4, 3), (5, 2), (6, 2)]
    for conf in slot_minterm_configs:
        acc_by_complexity[conf] = {'correct': 0, 'total': 0}
    for sample in response_data:
        lcc = sample['largest_connected_component']
        dep = sample['max_dependency']
        if lcc not in acc_by_lcc:
            acc_by_lcc[lcc] = {'correct': 0, 'total': 0}
        if dep not in acc_by_max_dependency:
            acc_by_max_dependency[dep] = {'correct': 0, 'total': 0}

    slots_dep_dict = {}
    for slot in range(2, 7):
        slots_dep_dict[slot] = {}

    for slot in range(2, 7):
        for dep in range(1, 4):
            slots_dep_dict[slot][dep] = {'correct': 0, 'total': 0}
    return acc_by_lcc, acc_by_max_dependency, acc_by_complexity, slots_dep_dict


def recursive_lcc_fn(dependency_dict, chain, last_node):
    diameter = len(chain)
    for child in dependency_dict[last_node]:
        if child not in chain:
            chain_copy = copy.deepcopy(chain)
            chain_copy.append(child)
            new_diam = recursive_lcc_fn(dependency_dict, chain_copy, child)
            if new_diam > diameter:
                diameter = new_diam
    return diameter


def get_graph_info(pos):
    dependency_dict = {}
    for node in pos.free_symbols:
        dependency_dict[node] = []
    for one_arg in pos.args:
        nodes = one_arg.free_symbols
        for node1 in nodes:
            for node2 in nodes:
                if node1 == node2:
                    continue
                if node2 not in dependency_dict[node1]:
                    dependency_dict[node1].append(node2)

    avg_dep, max_dep = 0, 0
    for node, deps in dependency_dict.items():
        num_deps = len(deps)
        if num_deps > max_dep:
            max_dep = num_deps
        avg_dep = avg_dep + num_deps

    avg_dep = avg_dep / len(dependency_dict)

    lcc = 0
    for node in pos.free_symbols:
        new_lcc = recursive_lcc_fn(dependency_dict, [node], node)
        if new_lcc > lcc:
            lcc = new_lcc

    width = 0
    for one_arg in pos.args:
        num_symbols = len(one_arg.free_symbols)
        if num_symbols >= 2:
            width = width + 1

    return avg_dep, max_dep, lcc, width


def get_ans(model_resp):
    loc = model_resp.find("answer is option")
    if loc != -1:
        pred = model_resp[loc + 17]
        return pred
    loc = model_resp.find("is the best match")
    if loc != -1:
        pred = model_resp[loc - 2]
        return pred
    loc = model_resp.find("is the most suitable")
    if loc != -1:
        pred = model_resp[loc - 2]
        return pred

    loc = model_resp.find("user should choose option")
    if loc != -1:
        pred = model_resp[loc + 26]
        return pred

    loc = model_resp.find(" thus matches all of the above conditions")
    if loc != -1:
        pred = model_resp[loc - 1]
        return pred

    if len(model_resp) == 8 and model_resp.startswith('option '):
        pred = model_resp[-1]
        return pred

    if model_resp.startswith('option ') and 'option ' not in model_resp[7:]:
        pred = model_resp[7]
        return pred

    return -1


def mark_correctness(response_data):
    correct, total = 0, 0

    skipped_count = 0
    acc_by_lcc, acc_by_max_dependency, acc_by_complexity, slots_dep_dict = initialize_acc_dicts(response_data)
    ent_avg_info, ent_overall_info, ent_ans_info = [], [], []

    for sample in response_data:
        conf = (sample['slots'], sample['minterms'])
        ans = sample['Answer'].lower()
        model_resp = sample['model_response'].lower()
        pred = get_ans(model_resp)

        lcc = sample['largest_connected_component']
        dep = sample['max_dependency']

        acc_by_complexity[conf]['total'] = acc_by_complexity[conf]['total'] + 1
        acc_by_lcc[lcc]['total'] = acc_by_lcc[lcc]['total'] + 1
        acc_by_max_dependency[dep]['total'] = acc_by_max_dependency[dep]['total'] + 1
        slots_dep_dict[sample['slots']][dep]['total'] = slots_dep_dict[sample['slots']][dep]['total'] + 1
        total = total + 1

        if pred == -1:
            skipped_count = skipped_count + 1
            continue
            # print("Answer not found")

        ent1, ent2 = np.mean(sample['entropy_avg']), np.mean(sample['entropy_overall'])
        ent3 = sample['entropy_overall'][char_to_index[sample['Answer']]]
        if ans == pred:
            correct = correct + 1
            ent_avg_info.append((ent1, 1))
            ent_overall_info.append((ent2, 1))
            ent_ans_info.append((ent3, 1))
            acc_by_complexity[conf]['correct'] = acc_by_complexity[conf]['correct'] + 1
            acc_by_lcc[lcc]['correct'] = acc_by_lcc[lcc]['correct'] + 1
            acc_by_max_dependency[dep]['correct'] = acc_by_max_dependency[dep]['correct'] + 1
            slots_dep_dict[sample['slots']][dep]['correct'] = slots_dep_dict[sample['slots']][dep]['correct'] + 1
        else:
            ent_avg_info.append((ent1, 0))
            ent_overall_info.append((ent2, 0))
            ent_ans_info.append((ent3, 0))

    calculate_accuracies([acc_by_lcc, acc_by_max_dependency, acc_by_complexity], slots_dep_dict)
    acc = correct / total
    response_info = ResponseInfo(correct, total, acc, acc_by_complexity, ent_avg_info, ent_overall_info, ent_ans_info,
                                 acc_by_lcc, acc_by_max_dependency, slots_dep_dict)
    # print(skipped_count)
    return response_info


def calculate_accuracies(dict_list, slots_dep_dict):
    for dict in dict_list:
        for key in dict:
            total = dict[key]['total']
            if total != 0:
                dict[key]['acc'] = float(dict[key]['correct']) / float(dict[key]['total'])
            else:
                dict[key]['acc'] = 0.0

    for slot in slots_dep_dict:
        for dep in slots_dep_dict[slot]:
            correct = slots_dep_dict[slot][dep]['correct']
            total = slots_dep_dict[slot][dep]['total']
            if total > 0:
                slots_dep_dict[slot][dep]['acc'] = correct / total
            else:
                slots_dep_dict[slot][dep]['acc'] = 0.0
