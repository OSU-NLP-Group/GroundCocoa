# Author: Harsh Kohli
# Date Created: 22-12-2023

import copy


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
